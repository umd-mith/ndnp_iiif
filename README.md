# ndnp_iiif

[![Build Status](https://travis-ci.org/umd-mith/ndnp_iiif.svg)](http://travis-ci.org/umd-mith/ndnp_iiif)

ndnp_iiif is a command line tool for creating [IIIF] manifests for [National Digital Newspaper Program] data. It is a work in progress. Check back soon!

The basic idea is you point `ndnp_iiif.py` at a path where you have an NDNP
batch directory, and a directory where you would like to store your IIIF manifest data, and it does its thing:

    % ndnp_iiif.py /vol/ndnp/batch_mdu_kale/ /var/www/ndnp/

[IIIF]: http://iiif.io
[National Digital Newspaper Program]: http://www.loc.gov/ndnp/