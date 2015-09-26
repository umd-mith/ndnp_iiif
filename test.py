import os
import json
import pytest
import shutil

from ndnp_iiif import load_batch
from os.path import dirname, isdir, join, relpath

test_data = join(dirname(__file__), 'test-data')
test_ndnp = join(test_data, 'batch_mdu_kale')
test_iiif= join(test_data, 'iiif')

def setup_module(module):
    if isdir(test_iiif):
        shutil.rmtree(test_iiif)
    os.mkdir(test_iiif)
    module.batch = load_batch(test_ndnp, test_iiif)

def test_ok():
    assert isdir(test_data)
    assert isdir(test_ndnp)
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

def test_page():
    assert len(batch.issues[0].pages) == 4
    p = batch.issues[0].pages[3]
    assert relpath(p.tiff_filename, test_ndnp) == "sn83009569/00296026165/1865100401/0016.tif"
    assert relpath(p.jp2_filename, test_ndnp) == "sn83009569/00296026165/1865100401/0016.jp2"
    assert relpath(p.pdf_filename, test_ndnp) == "sn83009569/00296026165/1865100401/0016.pdf"
    assert relpath(p.ocr_filename, test_ndnp) == "sn83009569/00296026165/1865100401/0016.xml"
    assert p.width == 6739
    assert p.height == 9068

def test_newspaper():
    n = batch.issues[0].newspaper
    assert n.lccn == "sn83009569"
    assert len(n.issues) == 1

def test_collection():
    collection = json.load(open(join(test_iiif, "newspapers.json")))
    assert len(collection['collections']) == 1
    subcollection = json.load(open(join(test_iiif, "sn83009569", "newspaper.json")))
    assert len(subcollection['manifests']) == 1
