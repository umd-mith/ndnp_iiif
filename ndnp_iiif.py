#!/usr/bin/env python

import json
import datetime

from os import mkdir
from PIL import Image
from lxml import etree
from os.path import abspath, dirname, isdir, isfile, join

# some xml namespaces used in NDNP data

ns = {
    'ndnp'  : 'http://www.loc.gov/ndnp',
    'mods'  : 'http://www.loc.gov/mods/v3',
    'mets'  : 'http://www.loc.gov/METS/',
    'np'    : 'urn:library-of-congress:ndnp:mets:newspaper',
    'xlink' : 'http://www.w3.org/1999/xlink',
}


def load_batch(batch_dir, iiif_dir):
    batch = Batch(batch_dir)
    batch.write_iiif(iiif_dir)
    return batch


class Batch:

    def __init__(self, batch_dir):
        if not isdir(batch_dir):
            raise Exception("no such directory: %s" % batch_dir)
        self.dir = abspath(batch_dir) + "/"
        self.issues = []
        self._read()

    @property
    def newspapers(self):
        n = set()
        for issue in self.issues:
            n.add(issue.newspaper)
        return list(n)

    def write_iiif(self, iiif_dir):
        path = join(iiif_dir, "newspapers.json")
        json.dump(self.iiif(), open(path, "w"), indent=2)
        for newspaper in self.newspapers:
            newspaper.write_iiif(iiif_dir)

    def iiif(self):
        collections = []
        for newspaper in self.newspapers:
            collections.append({
                "@id": newspaper.id,
                "@type": "sc:Collection",
                # TODO: put the newspaper title here
                "label": newspaper.lccn
            })

        return {
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@id": "newspapers.json",
            "@type": "sc:Collection",
            "label": "Top Level Collection for Example Organization",
            "description": "Description of Collection",
            "attribution": "Provided by Example Organization",
            "collections": collections,
        }

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
    def id(self):
        return "%s/%s.json" % (self.newspaper.lccn, self.date_issued_str)

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
        self.tiff_filename = None
        self.jp2_filename = None
        self.pdf_filename = None
        self.ocr_filename = None
        self.tiff_filename = None
        self.width = None
        self.height = None

        self._read(doc, div)

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
    def id(self):
        return "%s/newspaper.json" % self.lccn

    def write_iiif(self, iiif_dir):
        path = join(iiif_dir, self.id)
        dir = dirname(path)
        if not isdir(dir):
            mkdir(dir)
        json.dump(self.iiif(), open(path, "w"), indent=2)

    def iiif(self):
        manifests = []
        for issue in self.issues:
            manifests.append({
                "@id": issue.id,
                "@type": "sc:Manifest",
                "label": issue.date_issued_str
            })

        return {
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@id": self.id,
            "@type": "sc:Collection",
            "label": "Newspaper",
            "attribution": "Provided by Example Organization",
            "manifests": manifests
        }

    def add_issue(self, issue):
        "link the newspaper to an issue and vice-versa"
        self.issues.append(issue)
        issue.newspaper = self


def _dmd_mods(doc, dmdid):
    """a helper that returns mods inside a dmdSec with a given ID
    """
    xpath ='.//mets:dmdSec[@ID="%s"]/descendant::mods:mods' % dmdid
    return doc.xpath(xpath, namespaces=ns)[0]