# ndnp_iiif

[![Build Status](https://travis-ci.org/umd-mith/ndnp_iiif.svg)](http://travis-ci.org/umd-mith/ndnp_iiif)

`ndnp_iiif` is a command line tool for creating [IIIF] manifests for
[National Digital Newspaper Program] data. This IIIF data can then be mounted
on the Web and viewed using a IIIF compatible viewer.

For example, [here] is an example of viewing a single issue in Mirador. The 
manifests and generated tiles are published here on GitHub using GitHub Pages.

## Model

The [mapping] between NDNP's METS model and IIIF has been developed by the IIIF
Newspaper Interest Group.

| NDNP         | IIIF            |
| -----------  | --------------- |
| Page         | Canvas          |
| Issue        | Manifest        |
| Title        | Sub-Collection  |
| All Titles   | Collection      |

Note: The NDNP standard does not contain Article, Section or Volume information so those are not included.

## Install

Soon you'll be able to `pip install ndnp_iiif` but for now you'll have to:

    % git clone https://github.com/umd-mith/ndnp_iiif
    % cd ndnp_iiif
    % pip install -r requirements.txt
    % python setup.py install

## Usage:

### Static Images

The simplest usage is to point `ndnp_iiif` at a path where you have an NDNP
batch stored, and a web accessible directory where you would like to build your
IIIF data, as well as an absolute base URL where your data will be mounted on
the web:

    % ndnp_iiif /vol/ndnp/batch_mdu_kale/ /var/www/newspapers --base-url http://example.edu/newspapers/

This will cut static tiles for the page images that will be referenced in the
manifests.  The `--base-url` parameter is optional but strongly encouraged 
since it will result in absolute URLs being cooked into your IIIF data. 
Absolute URLs are preferred to relative URLs since they seem to work more 
predictably in IIIF viewers.

The resulting IIIF data will be laid out on the filesystem as a static site. The
[LCCN] for the newspaper is used for the top level directory, each issue is
placed into a sub-directory using the issue date, and then each page is placed
in a sub-directory of the issue. For each image encountered static tiles are cut
and placed inside the page directory.  Here's what a four page issue would look
like (some of the tile filenames are ellided):

```
/var/www
├── newspapers.json
└── sn83009569
    ├── 1865-10-04
    │   ├── 1
    │   │   ├── 0,0,1024,1024
    │   │   ├── 0,0,2048,2048
    │   │   ├── 0,0,4096,4096
                ...
    │   │   ├── 6144,6144,595,2048
    │   │   ├── 6144,7168,595,1024
    │   │   ├── 6144,8192,595,876
    │   │   ├── full
    │   │   └── info.json
    │   ├── 2
    │   │   ├── 0,0,1024,1024
    │   │   ├── 0,0,2048,2048
    │   │   ├── 0,0,4096,4096
                ...
    │   │   ├── 6144,6144,595,2048
    │   │   ├── 6144,7168,595,1024
    │   │   ├── 6144,8192,595,876
    │   │   ├── full
    │   │   └── info.json
    │   ├── 3
    │   │   ├── 0,0,1024,1024
    │   │   ├── 0,0,2048,2048
    │   │   ├── 0,0,4096,4096
                ...
    │   │   ├── 6144,6144,628,2048
    │   │   ├── 6144,7168,628,1024
    │   │   ├── 6144,8192,628,863
    │   │   ├── full
    │   │   └── info.json
    │   ├── 4
    │   │   ├── 0,0,1024,1024
    │   │   ├── 0,0,2048,2048
    │   │   ├── 0,0,4096,4096
                ...
    │   │   ├── 6144,6144,595,2048
    │   │   ├── 6144,7168,595,1024
    │   │   ├── 6144,8192,595,876
    │   │   ├── full
    │   │   └── info.json
    │   └── issue.json
    └── newspaper.json

```

### IIIF Image Server

If you are using an external IIIF Image Server then `ndnp_iiif` will write out
the IIIF Presentation API data to the filesystem and then reference the TIFF or
JPEG2000 file using the given IIIF Image Server and Prefix. For example:


    % ndnp_iiif /vol/ndnp/batch_mdu_kale/ /var/www/ --image-server http://images.example.edu/

will create the following files:

```
/var/www
├── newspapers.json
└── sn83009569
    ├── 1865-10-04
    │   └── issue.json
    └── newspaper.json
```

The images referenced in `issue.json` will target http://images.example.edu/
using the path for a TIFF file in the batch, for example:

    http://images.example.edu/batch_mdu_lilac/sn83009569/00296026165/1865100401/0013.tif

You will need to make sure that the images have been made available on the IIIF
image server.


## Test

You can run the tests, such as they are like so:

    % python setup test

The resulting IIIF data will be left in `test-data/iiif`. If you want you can
run a simple webserver pointed at that directory, and use the Mirador viewer
to display the result:

    % cd test-data/iiif
    % python -m SimpleHTTPServer

and then open [http://localhost:8000](http://localhost:8000) in your browser, at
which point you should see something like this:

![Mirador Screenshot](/test-data/screenshot.png?raw=true)

[IIIF]: http://iiif.io
[National Digital Newspaper Program]: http://www.loc.gov/ndnp/
[here]: http://umd-mith.github.io/ndnp_iiif/
[LCCN]: https://en.wikipedia.org/wiki/Library_of_Congress_Control_Number
[mapping]: https://en.wikipedia.org/wiki/Library_of_Congress_Control_Number
