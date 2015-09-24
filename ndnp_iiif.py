#!/usr/bin/env python

import json
import datetime

from lxml import etree
from os.path import join, isdir, abspath

# some xml namespaces used in NDNP data

ns = {
    'ndnp'  : 'http://www.loc.gov/ndnp',
    'mods'  : 'http://www.loc.gov/mods/v3',
    'mets'  : 'http://www.loc.gov/METS/',
    'np'    : 'urn:library-of-congress:ndnp:mets:newspaper',
    'xlink' : 'http://www.w3.org/1999/xlink',
    'mix'   : 'http://www.loc.gov/mix/',
    'xhtml' : 'http://www.w3.org/1999/xhtml'
}


class Batch:

    def __init__(self, batch_dir):
        if not isdir(batch_dir):
            raise Exception("no such directory: %s" % batch_dir)
        self.dir = abspath(batch_dir) + "/"
        self.issues = []
        self._read()

    def _read(self):
        batch_file = join(self.dir, "batch.xml")
        doc = etree.parse(batch_file)
        for e in doc.xpath('ndnp:issue', namespaces=ns):
            mets_file = join(self.dir, e.text)
            self.issues.append(Issue(mets_file))


class Issue:

    def __init__(self, mets_file):
        self.mets_file = mets_file
        self.pages = []
        self._read()

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

        for page_div in div.xpath('.//mets:div[@TYPE="np:page"]', namespaces=ns):
            self.pages.append(Page())


class Page:

    def __init__(self):
        pass


class Newspaper:

    def __init__(self):
        self.issues = []


def load_batch(batch_dir, iiif_dir):
    return Batch(batch_dir)

def _dmd_mods(doc, dmdid):
    """a helper that returns mods inside a dmdSec with a given ID
    """
    xpath ='.//mets:dmdSec[@ID="%s"]/descendant::mods:mods' % dmdid
    return doc.xpath(xpath, namespaces=ns)[0]