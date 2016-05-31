#!/usr/bin/env python

import os
import json
import logging
import argparse
import datetime

from os import mkdir
from PIL import Image
from lxml import etree
from iiif.static import IIIFStatic
from six.moves.urllib.parse import urljoin
from os.path import abspath, dirname, isdir, isfile, join

# some xml namespaces used in NDNP data

ns = {
    'ndnp'  : 'http://www.loc.gov/ndnp',
    'mods'  : 'http://www.loc.gov/mods/v3',
    'mets'  : 'http://www.loc.gov/METS/',
    'np'    : 'urn:library-of-congress:ndnp:mets:newspaper',
    'xlink' : 'http://www.w3.org/1999/xlink',
}


def main():
    parser = argparse.ArgumentParser(description='convert NDNP to IIIF')
    parser.add_argument('batch_dir', type=str, help='NDNP batch directory')
    parser.add_argument('iiif_dir', type=str, help='where to write IIIF')
    parser.add_argument('--base_uri', type=str, default='/', help='base URI for IIIF data') 
    parser.add_argument('--image_dir', type=str, default=None, help='where to write images')
    parser.add_argument('--image_base_uri', type=str, default=None, help='base URI for IIIF images')
    args = parser.parse_args()
    if not isdir(args.batch_dir):
        print('no such directory %s' % args.batch_dir)
        return
    batch = load_batch(args.batch_dir, args.iiif_dir, args.base_uri)
    # TODO: print out stats


def load_batch(batch_dir, iiif_dir, base_uri="/"):
    if not isdir(iiif_dir):
        mkdir(iiif_dir)
    batch = Batch(batch_dir, base_uri)
    batch.write_iiif(iiif_dir)
    return batch


class Batch:

    def __init__(self, batch_dir, base_uri):
        if not isdir(batch_dir):
            raise Exception("no such directory: %s" % batch_dir)
        self.dir = abspath(batch_dir) + "/"
        self.base_uri = base_uri
        self.issues = []
        self._read()

    @property
    def newspapers(self):
        n = set()
        for issue in self.issues:
            n.add(issue.newspaper)
        return list(n)

    @property
    def uri(self):
        return urljoin(self.base_uri, "newspapers.json")

    def write_iiif(self, iiif_dir):
        path = join(iiif_dir, "newspapers.json")
        if isfile(path):
            iiif = json.load(open(path))
        else:
            iiif = None

        if not isdir(dirname(path)):
            os.mkdir(dirname(path))
        logging.info("writing newspaper collection to %s", path)
        json.dump(self.iiif(iiif), open(path, "w"), indent=2)
        for newspaper in self.newspapers:
            newspaper.write_iiif(iiif_dir)
            for issue in self.issues:
                issue.write_iiif(iiif_dir)

    def iiif(self, iiif=None):
        if iiif is None:
            iiif = {
                "@context": "http://iiif.io/api/presentation/2/context.json",
                "@id": self.uri,
                "@type": "sc:Collection",
                "label": "Top Level Collection for Example Organization",
                "description": "Description of Collection",
                "attribution": "Provided by Example Organization",
                "collections": []
            }

        ids = [n['@id'] for n in iiif['collections']]

        for newspaper in self.newspapers:
            # no need to add the newspaper if it is already there
            if newspaper.uri in ids:
                continue
            iiif['collections'].append({
                "@id": newspaper.uri,
                "@type": "sc:Collection",
                # TODO: put the newspaper title here
                "label": newspaper.lccn
            })

        return iiif

    def _read(self):
        batch_file = self._find_batch_file()
        doc = etree.parse(batch_file)
        for e in doc.xpath('ndnp:issue', namespaces=ns):
            mets_file = join(self.dir, e.text)
            self.issues.append(Issue(self, mets_file))

    def _find_batch_file(self):
        # look for the weird places people put the validated batch file
        for alias in ["batch_1.xml", "BATCH_1.xml", "batchfile_1.xml", "batch_2.xml", "BATCH_2.xml", "batch.xml"]:
            path = join(self.dir, alias)
            if isfile(path):
                return path
        return None


class Issue:

    def __init__(self, batch, mets_file):
        self.batch = batch
        self.mets_file = mets_file
        self.volumne = None
        self.number = None
        self.edition = None
        self.edition_label = None
        self.date_issued = None
        self.pages = []
        self._read()

    @property
    def date_issued_str(self):
        "pre-1900 dates don't format on python 2.7"
        d = self.date_issued
        return "%4i-%02i-%02i" % (d.year, d.month, d.day)

    @property
    def uri(self):
        return urljoin(self.newspaper.uri, join(self.date_issued_str, "issue.json"))

    def write_iiif(self, iiif_dir):
        path = join(iiif_dir, self.uri.lstrip("/"))
        dir = dirname(path)
        if not isdir(dir):
            mkdir(dir)
        logging.info("writing issue data %s", path)
        json.dump(self.iiif(iiif_dir), open(path, "w"), indent=2)

    def iiif(self, iiif_dir):
        canvases = []
        for page in self.pages:
            tiles_dir = join(iiif_dir, page.uri.lstrip("/"))
            page.generate_tiles(tiles_dir)
            canvases.append({
                "@id": page.uri,
                "@type": "sc:Canvas",
                "label": "page %s" % page.sequence,
                "height": page.height,
                "width": page.width,
                "thumbnail": page.thumbnail(tiles_dir),
                "images": [{
                    "@id": page.uri,
                    "@type": "oa:Annotation",
                    "motivation": "sc:painting",
                    "resource": {
                        "@id": page.uri,
                        "@type": "dctypes:Image",
                        "format": "image/jpeg",
                        "height": page.height,
                        "width": page.width,
                        "service": {
                            "@id": page.service_uri,
                            "@context": "http://iiif.io/api/image/2/context.json",
                            "profile": "http://iiif.io/api/image/2/level0.json"
                        }
                    }
                }]
            })

        sequence = {
            "@id": "normal",
            "@type": "sc:Sequence",
            "label": "page order",
            "canvases": canvases,
        }

        return {
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@id": self.uri,
            "@type": "sc:Manifest",
            "label": self.date_issued_str,
            "sequences": [sequence]
        }

    def _read(self):
        doc = etree.parse(self.mets_file)

        # get mods metadata for the issue
        div = doc.xpath('.//mets:div[@TYPE="np:issue"]', namespaces=ns)[0]
        dmdid = div.attrib["DMDID"]
        mods = _dmd_mods(doc, dmdid)

        # set up new issue
        self.volume = mods.xpath('string(.//mods:detail[@type="volume"]/mods:number[1])', namespaces=ns).strip()
        self.number = mods.xpath('string(.//mods:detail[@type="issue"]/mods:number[1])', namespaces=ns).strip()
        self.edition = int(mods.xpath('string(.//mods:detail[@type="edition"]/mods:number[1])', namespaces=ns))
        self.edition_label = mods.xpath('string(.//mods:detail[@type="edition"]/mods:caption[1])', namespaces=ns).strip()

        # parse issue date
        self.date_issued = datetime.datetime.strptime(mods.xpath('string(.//mods:dateIssued)', namespaces=ns), '%Y-%m-%d')

        # attach pages
        for page_div in div.xpath('.//mets:div[@TYPE="np:page"]', namespaces=ns):
            self.pages.append(Page(self, doc, page_div))

        # find the newspaper the issue belongs to
        lccn = mods.xpath('string(.//mods:identifier[@type="lccn"])', namespaces=ns).strip()
        newspaper = Newspaper.find_or_create(lccn)
        newspaper.add_issue(self)


class Page:

    def __init__(self, issue, doc, div):
        self.issue = issue
        self.sequence = None
        self.number = None
        self.tiff_filename = None
        self.jp2_filename = None
        self.pdf_filename = None
        self.ocr_filename = None
        self.width = None
        self.height = None

        self._read(doc, div)

    @property
    def uri(self):
        return urljoin(self.issue.uri, str(self.sequence))

    def thumbnail(self, tiles_dir):
        """
        Get the widest thumbnail generated in the tiles_dir.
        """
        width_dirs = os.listdir(join(tiles_dir, "full"))
        widths = [int(s.split(",")[0]) for s in width_dirs]
        widths.sort()
        max_width = "%s," % widths.pop()
        return join(self.uri, "full", max_width, '0', 'default.jpg')

    @property
    def service_uri(self):
        return self.uri

    def generate_tiles(self, dest):
        tiles_dest = dirname(dest)
        sg = IIIFStatic(src=self.tiff_filename, dst=tiles_dest, tilesize=1024, api_version="2.0")
        sg.generate(self.tiff_filename, str(self.sequence))
        info_path = join(dest, "info.json")
        info = json.load(open(info_path))
        info['@id'] = self.service_uri
        json.dump(info, open(info_path, 'w'), indent=2)

    def _read(self, doc, div):
        dmdid = div.attrib['DMDID']
        mods = _dmd_mods(doc, dmdid)
        self.sequence = int(mods.xpath('string(.//mods:extent/mods:start)', namespaces=ns))
        self.number = mods.xpath('string(.//mods:detail[@type="page number"])', namespaces=ns).strip()

        # there's a level indirection between the METS structmap and the
        # details about specific files in this package. so we have to
        # first get the FILEID from the issue div in the structmap and
        # then use it to look up the file details in the larger document
        # &sigh;

        for fptr in div.xpath('./mets:fptr', namespaces=ns):
            file_id = fptr.attrib['FILEID']
            file_el = doc.xpath('.//mets:file[@ID="%s"]' % file_id, namespaces=ns)[0]
            file_type = file_el.attrib['USE']

            # get the absolute path to the file
            file_name = file_el.xpath('string(./mets:FLocat/@xlink:href)', namespaces=ns)
            file_name = abspath(join(dirname(doc.docinfo.URL), file_name))

            # record the path and image height/width depending on file type
            if file_type == 'master':
                self.tiff_filename = file_name
                i = Image.open(file_name)
                self.width, self.height = i.size
            elif file_type == 'service':
                self.jp2_filename = file_name
            elif file_type == 'derivative':
                self.pdf_filename = file_name
            elif file_type == 'ocr':
                self.ocr_filename = file_name


class Newspaper:
    _cache = {}

    @classmethod
    def find_or_create(cls, lccn):
        if lccn in cls._cache:
            return cls._cache[lccn]
        else:
            return Newspaper(lccn)

    def __init__(self, lccn):
        self.lccn = lccn
        self.issues = []
        # TODO: get needed metadata from somewhere :)

    @property
    def uri(self):
        return urljoin(self.issues[0].batch.uri, join(self.lccn, "newspaper.json"))

    def write_iiif(self, iiif_dir):
        path = join(iiif_dir, self.uri.lstrip("/"))

        # load any existing iiif from previous batch
        if isfile(path):
            logging.info("reading existing newspaper data at %s", path)
            iiif = json.load(open(path))
        else:
            iiif = None

        dir = dirname(path)
        if not isdir(dir):
            logging.info("making %s", dir)
            mkdir(dir)

        logging.info("writing newspaper data to %s", path)
        json.dump(self.iiif(iiif), open(path, "w"), indent=2)

    def iiif(self, iiif=None):
        if iiif is None:
            iiif = {
                "@context": "http://iiif.io/api/presentation/2/context.json",
                "@id": self.uri,
                "@type": "sc:Collection",
                "label": "Newspaper",
                "attribution": "Provided by Example Organization",
                "manifests": []
            }

        for issue in self.issues:
            iiif['manifests'].append({
                "@id": issue.uri,
                "@type": "sc:Manifest",
                "label": issue.date_issued_str
            })

        return iiif

    def add_issue(self, issue):
        "link the newspaper to an issue and vice-versa"
        self.issues.append(issue)
        issue.newspaper = self


def _dmd_mods(doc, dmdid):
    """a helper that returns mods inside a dmdSec with a given ID
    """
    xpath ='.//mets:dmdSec[@ID="%s"]/descendant::mods:mods' % dmdid
    return doc.xpath(xpath, namespaces=ns)[0]


if __name__ == "__main__":
    main()
