import os
import pytest
import shutil

from ndnp_iiif import load_batch
from os.path import join, dirname, isdir

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
    assert batch

def test_issue():
    assert len(batch.issues) == 1

def test_page():
    assert len(batch.issues[0].pages) == 4

