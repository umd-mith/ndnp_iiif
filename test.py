import os
import json
import pytest
import shutil
import logging
import datetime

from ndnp_iiif import load_batch
from os.path import dirname, isdir, join, relpath

test_data = join(dirname(__file__), 'test-data')
test_iiif= join(test_data, 'iiif')
kale = join(test_data, 'batch_mdu_kale')

logging.basicConfig(filename="test.log", level=logging.INFO)

def setup_module(module):
    # clean up any existing data from previous test run
    if isdir(test_iiif):
        shutil.rmtree(test_iiif)
    os.mkdir(test_iiif)
    module.batch = load_batch(kale, test_iiif)

def test_ok():
    assert isdir(test_data)
    assert isdir(kale)
    assert isdir(test_iiif)

def test_batch():
    assert batch

def test_issue():
    assert len(batch.issues) == 1
    i = batch.issues[0]
    assert i.volume == "1"
    assert i.number == "3"
    assert i.edition == 1
    assert i.edition_label == ""
    assert i.date_issued_str == "1865-10-04"

def test_page():
    assert len(batch.issues[0].pages) == 4
    p = batch.issues[0].pages[3]
    assert p.sequence == 4
    assert p.number == ""
    assert relpath(p.tiff_filename, kale) == "sn83009569/00296026165/1865100401/0016.tif"
    assert relpath(p.jp2_filename, kale) == "sn83009569/00296026165/1865100401/0016.jp2"
    assert relpath(p.pdf_filename, kale) == "sn83009569/00296026165/1865100401/0016.pdf"
    assert relpath(p.ocr_filename, kale) == "sn83009569/00296026165/1865100401/0016.xml"
    assert p.width == 6739
    assert p.height == 9068

def test_newspaper():
    n = batch.issues[0].newspaper
    assert n.lccn == "sn83009569"
    assert n.title == 'Baltimore daily commercial.'
    assert n.publisher == 'W. Wales & Co.'
    assert n.place_of_publication == 'Baltimore, Md.'
    assert n.start_year == '1865'
    assert n.end_year == '1867'

    assert len(n.issues) == 1

def test_iiif_data():
    shutil.copytree("test-data/demo/mirador", "test-data/iiif/mirador")
    shutil.copyfile("test-data/demo/index.html", "test-data/iiif/index.html")
    collection = json.load(open(join(test_iiif, "newspapers.json")))
    assert collection['@id'] == "newspapers.json"
    assert len(collection['collections']) == 1

    subcollection = json.load(open(join(test_iiif, "sn83009569", "newspaper.json")))
    assert subcollection['@id'] == "sn83009569/newspaper.json"
    assert subcollection['metadata'][0]['label'] == 'lccn'
    assert subcollection['metadata'][0]['value'] == 'sn83009569'
    assert len(subcollection['manifests']) == 1

    manifest = json.load(open(join(test_iiif, "sn83009569", "1865-10-04", "issue.json")))
    assert manifest['@id'] == 'sn83009569/1865-10-04/issue.json'
    assert len(manifest['sequences'][0]['canvases']), 4

    canvas = manifest['sequences'][0]['canvases'][0]
    assert canvas['@id'] == 'sn83009569/1865-10-04/1'
    assert canvas['images'][0]['resource']['service']['@id'] == 'sn83009569/1865-10-04/1'

def test_overlay():
    # loading lilac should result in two issues being present in the newspaper
    # collection

    lilac = join(test_data, 'batch_mdu_lilac')
    load_batch(lilac, test_iiif)

    newspaper = json.load(open(join(test_iiif, "sn83009569", "newspaper.json")))
    assert len(newspaper['manifests']) == 2

def atest_new_newspaper():
    # loading melon should result in two items in the newspapers collection
    melon = join(test_data, 'batch_mdu_melon')
    load_batch(melon, test_iiif)

    newspapers = json.load(open(join(test_iiif, "newspapers.json")))
    assert len(newspapers['collections']) == 2
