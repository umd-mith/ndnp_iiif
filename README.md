# ndnp_iiif

[![Build Status](https://travis-ci.org/umd-mith/ndnp_iiif.svg)](http://travis-ci.org/umd-mith/ndnp_iiif)

ndnp_iiif is a command line tool for creating [IIIF] manifests for [National Digital Newspaper Program] data. This is a work in progress, so check back soon! Please feel free to submit issues if you have questions or ideas.

The basic idea is you point `ndnp_iiif.py` at a path where you have an NDNP
batch stored, and a directory where you would like to build your IIIF data.

    % ndnp_iiif.py /vol/ndnp/batch_mdu_kale/ /var/www

The resulting IIIF data will be laid out on the filesystem like this:

```
/var/www
├── newspapers.json
└── sn83009569
    ├── 1865-10-04
    │   ├── 1
    │   │   ├── 0,0,1024,1024
    │   │   ├── 0,0,2048,2048
    │   │   ├── 0,0,4096,4096
    │   │   ├── 0,0,6739,8192
    │   │   ├── 0,1024,1024,1024
    │   │   ├── 0,2048,1024,1024
    │   │   ├── 0,2048,2048,2048
    │   │   ├── 0,3072,1024,1024
    │   │   ├── 0,4096,1024,1024
    │   │   ├── 0,4096,2048,2048
    │   │   ├── 0,4096,4096,4096
    │   │   ├── 0,5120,1024,1024
    │   │   ├── 0,6144,1024,1024
    │   │   ├── 0,6144,2048,2048
    │   │   ├── 0,7168,1024,1024
    │   │   ├── 0,8192,1024,876
    │   │   ├── 0,8192,2048,876
    │   │   ├── 0,8192,4096,876
    │   │   ├── 0,8192,6739,876
    │   │   ├── 1024,0,1024,1024
    │   │   ├── 1024,1024,1024,1024
    │   │   ├── 1024,2048,1024,1024
    │   │   ├── 1024,3072,1024,1024
    │   │   ├── 1024,4096,1024,1024
    │   │   ├── 1024,5120,1024,1024
    │   │   ├── 1024,6144,1024,1024
    │   │   ├── 1024,7168,1024,1024
    │   │   ├── 1024,8192,1024,876
    │   │   ├── 2048,0,1024,1024
    │   │   ├── 2048,0,2048,2048
    │   │   ├── 2048,1024,1024,1024
    │   │   ├── 2048,2048,1024,1024
    │   │   ├── 2048,2048,2048,2048
    │   │   ├── 2048,3072,1024,1024
    │   │   ├── 2048,4096,1024,1024
    │   │   ├── 2048,4096,2048,2048
    │   │   ├── 2048,5120,1024,1024
    │   │   ├── 2048,6144,1024,1024
    │   │   ├── 2048,6144,2048,2048
    │   │   ├── 2048,7168,1024,1024
    │   │   ├── 2048,8192,1024,876
    │   │   ├── 2048,8192,2048,876
    │   │   ├── 3072,0,1024,1024
    │   │   ├── 3072,1024,1024,1024
    │   │   ├── 3072,2048,1024,1024
    │   │   ├── 3072,3072,1024,1024
    │   │   ├── 3072,4096,1024,1024
    │   │   ├── 3072,5120,1024,1024
    │   │   ├── 3072,6144,1024,1024
    │   │   ├── 3072,7168,1024,1024
    │   │   ├── 3072,8192,1024,876
    │   │   ├── 4096,0,1024,1024
    │   │   ├── 4096,0,2048,2048
    │   │   ├── 4096,0,2643,4096
    │   │   ├── 4096,1024,1024,1024
    │   │   ├── 4096,2048,1024,1024
    │   │   ├── 4096,2048,2048,2048
    │   │   ├── 4096,3072,1024,1024
    │   │   ├── 4096,4096,1024,1024
    │   │   ├── 4096,4096,2048,2048
    │   │   ├── 4096,4096,2643,4096
    │   │   ├── 4096,5120,1024,1024
    │   │   ├── 4096,6144,1024,1024
    │   │   ├── 4096,6144,2048,2048
    │   │   ├── 4096,7168,1024,1024
    │   │   ├── 4096,8192,1024,876
    │   │   ├── 4096,8192,2048,876
    │   │   ├── 4096,8192,2643,876
    │   │   ├── 5120,0,1024,1024
    │   │   ├── 5120,1024,1024,1024
    │   │   ├── 5120,2048,1024,1024
    │   │   ├── 5120,3072,1024,1024
    │   │   ├── 5120,4096,1024,1024
    │   │   ├── 5120,5120,1024,1024
    │   │   ├── 5120,6144,1024,1024
    │   │   ├── 5120,7168,1024,1024
    │   │   ├── 5120,8192,1024,876
    │   │   ├── 6144,0,595,1024
    │   │   ├── 6144,0,595,2048
    │   │   ├── 6144,1024,595,1024
    │   │   ├── 6144,2048,595,1024
    │   │   ├── 6144,2048,595,2048
    │   │   ├── 6144,3072,595,1024
    │   │   ├── 6144,4096,595,1024
    │   │   ├── 6144,4096,595,2048
    │   │   ├── 6144,5120,595,1024
    │   │   ├── 6144,6144,595,1024
    │   │   ├── 6144,6144,595,2048
    │   │   ├── 6144,7168,595,1024
    │   │   ├── 6144,8192,595,876
    │   │   ├── full
    │   │   └── info.json
    │   ├── 2
    │   │   ├── 0,0,1024,1024
    │   │   ├── 0,0,2048,2048
    │   │   ├── 0,0,4096,4096
    │   │   ├── 0,0,6739,8192
    │   │   ├── 0,1024,1024,1024
    │   │   ├── 0,2048,1024,1024
    │   │   ├── 0,2048,2048,2048
    │   │   ├── 0,3072,1024,1024
    │   │   ├── 0,4096,1024,1024
    │   │   ├── 0,4096,2048,2048
    │   │   ├── 0,4096,4096,4096
    │   │   ├── 0,5120,1024,1024
    │   │   ├── 0,6144,1024,1024
    │   │   ├── 0,6144,2048,2048
    │   │   ├── 0,7168,1024,1024
    │   │   ├── 0,8192,1024,876
    │   │   ├── 0,8192,2048,876
    │   │   ├── 0,8192,4096,876
    │   │   ├── 0,8192,6739,876
    │   │   ├── 1024,0,1024,1024
    │   │   ├── 1024,1024,1024,1024
    │   │   ├── 1024,2048,1024,1024
    │   │   ├── 1024,3072,1024,1024
    │   │   ├── 1024,4096,1024,1024
    │   │   ├── 1024,5120,1024,1024
    │   │   ├── 1024,6144,1024,1024
    │   │   ├── 1024,7168,1024,1024
    │   │   ├── 1024,8192,1024,876
    │   │   ├── 2048,0,1024,1024
    │   │   ├── 2048,0,2048,2048
    │   │   ├── 2048,1024,1024,1024
    │   │   ├── 2048,2048,1024,1024
    │   │   ├── 2048,2048,2048,2048
    │   │   ├── 2048,3072,1024,1024
    │   │   ├── 2048,4096,1024,1024
    │   │   ├── 2048,4096,2048,2048
    │   │   ├── 2048,5120,1024,1024
    │   │   ├── 2048,6144,1024,1024
    │   │   ├── 2048,6144,2048,2048
    │   │   ├── 2048,7168,1024,1024
    │   │   ├── 2048,8192,1024,876
    │   │   ├── 2048,8192,2048,876
    │   │   ├── 3072,0,1024,1024
    │   │   ├── 3072,1024,1024,1024
    │   │   ├── 3072,2048,1024,1024
    │   │   ├── 3072,3072,1024,1024
    │   │   ├── 3072,4096,1024,1024
    │   │   ├── 3072,5120,1024,1024
    │   │   ├── 3072,6144,1024,1024
    │   │   ├── 3072,7168,1024,1024
    │   │   ├── 3072,8192,1024,876
    │   │   ├── 4096,0,1024,1024
    │   │   ├── 4096,0,2048,2048
    │   │   ├── 4096,0,2643,4096
    │   │   ├── 4096,1024,1024,1024
    │   │   ├── 4096,2048,1024,1024
    │   │   ├── 4096,2048,2048,2048
    │   │   ├── 4096,3072,1024,1024
    │   │   ├── 4096,4096,1024,1024
    │   │   ├── 4096,4096,2048,2048
    │   │   ├── 4096,4096,2643,4096
    │   │   ├── 4096,5120,1024,1024
    │   │   ├── 4096,6144,1024,1024
    │   │   ├── 4096,6144,2048,2048
    │   │   ├── 4096,7168,1024,1024
    │   │   ├── 4096,8192,1024,876
    │   │   ├── 4096,8192,2048,876
    │   │   ├── 4096,8192,2643,876
    │   │   ├── 5120,0,1024,1024
    │   │   ├── 5120,1024,1024,1024
    │   │   ├── 5120,2048,1024,1024
    │   │   ├── 5120,3072,1024,1024
    │   │   ├── 5120,4096,1024,1024
    │   │   ├── 5120,5120,1024,1024
    │   │   ├── 5120,6144,1024,1024
    │   │   ├── 5120,7168,1024,1024
    │   │   ├── 5120,8192,1024,876
    │   │   ├── 6144,0,595,1024
    │   │   ├── 6144,0,595,2048
    │   │   ├── 6144,1024,595,1024
    │   │   ├── 6144,2048,595,1024
    │   │   ├── 6144,2048,595,2048
    │   │   ├── 6144,3072,595,1024
    │   │   ├── 6144,4096,595,1024
    │   │   ├── 6144,4096,595,2048
    │   │   ├── 6144,5120,595,1024
    │   │   ├── 6144,6144,595,1024
    │   │   ├── 6144,6144,595,2048
    │   │   ├── 6144,7168,595,1024
    │   │   ├── 6144,8192,595,876
    │   │   ├── full
    │   │   └── info.json
    │   ├── 3
    │   │   ├── 0,0,1024,1024
    │   │   ├── 0,0,2048,2048
    │   │   ├── 0,0,4096,4096
    │   │   ├── 0,0,6772,8192
    │   │   ├── 0,1024,1024,1024
    │   │   ├── 0,2048,1024,1024
    │   │   ├── 0,2048,2048,2048
    │   │   ├── 0,3072,1024,1024
    │   │   ├── 0,4096,1024,1024
    │   │   ├── 0,4096,2048,2048
    │   │   ├── 0,4096,4096,4096
    │   │   ├── 0,5120,1024,1024
    │   │   ├── 0,6144,1024,1024
    │   │   ├── 0,6144,2048,2048
    │   │   ├── 0,7168,1024,1024
    │   │   ├── 0,8192,1024,863
    │   │   ├── 0,8192,2048,863
    │   │   ├── 0,8192,4096,863
    │   │   ├── 0,8192,6772,863
    │   │   ├── 1024,0,1024,1024
    │   │   ├── 1024,1024,1024,1024
    │   │   ├── 1024,2048,1024,1024
    │   │   ├── 1024,3072,1024,1024
    │   │   ├── 1024,4096,1024,1024
    │   │   ├── 1024,5120,1024,1024
    │   │   ├── 1024,6144,1024,1024
    │   │   ├── 1024,7168,1024,1024
    │   │   ├── 1024,8192,1024,863
    │   │   ├── 2048,0,1024,1024
    │   │   ├── 2048,0,2048,2048
    │   │   ├── 2048,1024,1024,1024
    │   │   ├── 2048,2048,1024,1024
    │   │   ├── 2048,2048,2048,2048
    │   │   ├── 2048,3072,1024,1024
    │   │   ├── 2048,4096,1024,1024
    │   │   ├── 2048,4096,2048,2048
    │   │   ├── 2048,5120,1024,1024
    │   │   ├── 2048,6144,1024,1024
    │   │   ├── 2048,6144,2048,2048
    │   │   ├── 2048,7168,1024,1024
    │   │   ├── 2048,8192,1024,863
    │   │   ├── 2048,8192,2048,863
    │   │   ├── 3072,0,1024,1024
    │   │   ├── 3072,1024,1024,1024
    │   │   ├── 3072,2048,1024,1024
    │   │   ├── 3072,3072,1024,1024
    │   │   ├── 3072,4096,1024,1024
    │   │   ├── 3072,5120,1024,1024
    │   │   ├── 3072,6144,1024,1024
    │   │   ├── 3072,7168,1024,1024
    │   │   ├── 3072,8192,1024,863
    │   │   ├── 4096,0,1024,1024
    │   │   ├── 4096,0,2048,2048
    │   │   ├── 4096,0,2676,4096
    │   │   ├── 4096,1024,1024,1024
    │   │   ├── 4096,2048,1024,1024
    │   │   ├── 4096,2048,2048,2048
    │   │   ├── 4096,3072,1024,1024
    │   │   ├── 4096,4096,1024,1024
    │   │   ├── 4096,4096,2048,2048
    │   │   ├── 4096,4096,2676,4096
    │   │   ├── 4096,5120,1024,1024
    │   │   ├── 4096,6144,1024,1024
    │   │   ├── 4096,6144,2048,2048
    │   │   ├── 4096,7168,1024,1024
    │   │   ├── 4096,8192,1024,863
    │   │   ├── 4096,8192,2048,863
    │   │   ├── 4096,8192,2676,863
    │   │   ├── 5120,0,1024,1024
    │   │   ├── 5120,1024,1024,1024
    │   │   ├── 5120,2048,1024,1024
    │   │   ├── 5120,3072,1024,1024
    │   │   ├── 5120,4096,1024,1024
    │   │   ├── 5120,5120,1024,1024
    │   │   ├── 5120,6144,1024,1024
    │   │   ├── 5120,7168,1024,1024
    │   │   ├── 5120,8192,1024,863
    │   │   ├── 6144,0,628,1024
    │   │   ├── 6144,0,628,2048
    │   │   ├── 6144,1024,628,1024
    │   │   ├── 6144,2048,628,1024
    │   │   ├── 6144,2048,628,2048
    │   │   ├── 6144,3072,628,1024
    │   │   ├── 6144,4096,628,1024
    │   │   ├── 6144,4096,628,2048
    │   │   ├── 6144,5120,628,1024
    │   │   ├── 6144,6144,628,1024
    │   │   ├── 6144,6144,628,2048
    │   │   ├── 6144,7168,628,1024
    │   │   ├── 6144,8192,628,863
    │   │   ├── full
    │   │   └── info.json
    │   ├── 4
    │   │   ├── 0,0,1024,1024
    │   │   ├── 0,0,2048,2048
    │   │   ├── 0,0,4096,4096
    │   │   ├── 0,0,6739,8192
    │   │   ├── 0,1024,1024,1024
    │   │   ├── 0,2048,1024,1024
    │   │   ├── 0,2048,2048,2048
    │   │   ├── 0,3072,1024,1024
    │   │   ├── 0,4096,1024,1024
    │   │   ├── 0,4096,2048,2048
    │   │   ├── 0,4096,4096,4096
    │   │   ├── 0,5120,1024,1024
    │   │   ├── 0,6144,1024,1024
    │   │   ├── 0,6144,2048,2048
    │   │   ├── 0,7168,1024,1024
    │   │   ├── 0,8192,1024,876
    │   │   ├── 0,8192,2048,876
    │   │   ├── 0,8192,4096,876
    │   │   ├── 0,8192,6739,876
    │   │   ├── 1024,0,1024,1024
    │   │   ├── 1024,1024,1024,1024
    │   │   ├── 1024,2048,1024,1024
    │   │   ├── 1024,3072,1024,1024
    │   │   ├── 1024,4096,1024,1024
    │   │   ├── 1024,5120,1024,1024
    │   │   ├── 1024,6144,1024,1024
    │   │   ├── 1024,7168,1024,1024
    │   │   ├── 1024,8192,1024,876
    │   │   ├── 2048,0,1024,1024
    │   │   ├── 2048,0,2048,2048
    │   │   ├── 2048,1024,1024,1024
    │   │   ├── 2048,2048,1024,1024
    │   │   ├── 2048,2048,2048,2048
    │   │   ├── 2048,3072,1024,1024
    │   │   ├── 2048,4096,1024,1024
    │   │   ├── 2048,4096,2048,2048
    │   │   ├── 2048,5120,1024,1024
    │   │   ├── 2048,6144,1024,1024
    │   │   ├── 2048,6144,2048,2048
    │   │   ├── 2048,7168,1024,1024
    │   │   ├── 2048,8192,1024,876
    │   │   ├── 2048,8192,2048,876
    │   │   ├── 3072,0,1024,1024
    │   │   ├── 3072,1024,1024,1024
    │   │   ├── 3072,2048,1024,1024
    │   │   ├── 3072,3072,1024,1024
    │   │   ├── 3072,4096,1024,1024
    │   │   ├── 3072,5120,1024,1024
    │   │   ├── 3072,6144,1024,1024
    │   │   ├── 3072,7168,1024,1024
    │   │   ├── 3072,8192,1024,876
    │   │   ├── 4096,0,1024,1024
    │   │   ├── 4096,0,2048,2048
    │   │   ├── 4096,0,2643,4096
    │   │   ├── 4096,1024,1024,1024
    │   │   ├── 4096,2048,1024,1024
    │   │   ├── 4096,2048,2048,2048
    │   │   ├── 4096,3072,1024,1024
    │   │   ├── 4096,4096,1024,1024
    │   │   ├── 4096,4096,2048,2048
    │   │   ├── 4096,4096,2643,4096
    │   │   ├── 4096,5120,1024,1024
    │   │   ├── 4096,6144,1024,1024
    │   │   ├── 4096,6144,2048,2048
    │   │   ├── 4096,7168,1024,1024
    │   │   ├── 4096,8192,1024,876
    │   │   ├── 4096,8192,2048,876
    │   │   ├── 4096,8192,2643,876
    │   │   ├── 5120,0,1024,1024
    │   │   ├── 5120,1024,1024,1024
    │   │   ├── 5120,2048,1024,1024
    │   │   ├── 5120,3072,1024,1024
    │   │   ├── 5120,4096,1024,1024
    │   │   ├── 5120,5120,1024,1024
    │   │   ├── 5120,6144,1024,1024
    │   │   ├── 5120,7168,1024,1024
    │   │   ├── 5120,8192,1024,876
    │   │   ├── 6144,0,595,1024
    │   │   ├── 6144,0,595,2048
    │   │   ├── 6144,1024,595,1024
    │   │   ├── 6144,2048,595,1024
    │   │   ├── 6144,2048,595,2048
    │   │   ├── 6144,3072,595,1024
    │   │   ├── 6144,4096,595,1024
    │   │   ├── 6144,4096,595,2048
    │   │   ├── 6144,5120,595,1024
    │   │   ├── 6144,6144,595,1024
    │   │   ├── 6144,6144,595,2048
    │   │   ├── 6144,7168,595,1024
    │   │   ├── 6144,8192,595,876
    │   │   ├── full
    │   │   └── info.json
    │   └── issue.json
    └── newspaper.json

```

[IIIF]: http://iiif.io
[National Digital Newspaper Program]: http://www.loc.gov/ndnp/
