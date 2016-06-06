import json
import logging
import iiif.static

from os import mkdir, listdir
from six.moves.urllib.parse import urljoin
from os.path import dirname, isdir, isfile, join, relpath


class Writer:
    """
    Writer is responsible for figuring out how to write a batch
    of NDNP data to disk as IIIF.
    """

    def __init__(self, iiif_dir, base_url="", image_server=""):
        self.iiif_dir = iiif_dir
        self.base_url = base_url
        self.image_server = image_server
        if not isdir(iiif_dir):
            mkdir(iiif_dir)


    def write(self, batch):
        logging.info("writing batch %s to %s", batch, self.iiif_dir)
        self.write_newspapers(batch)

        for newspaper in batch.newspapers:
            self.write_newspaper(newspaper)

        for issue in batch.issues:
            self.write_issue(issue)


    def uri(self, path):
        return urljoin(self.base_url, path)


    def abspath(self, path):
        return join(self.iiif_dir, path)


    def write_newspapers(self, batch):
        path = self.abspath('newspapers.json')
        url = self.uri('newspapers.json')

        if isfile(path):
            iiif = json.load(open(path))
        else:
            # TODO: allow label, description, attribution to be passed in?
            iiif = {
                "@context": "http://iiif.io/api/presentation/2/context.json",
                "@id": url,
                "@type": "sc:Collection",
                "label": "Top Level Collection for Example Organization",
                "description": "Description of Collection",
                "attribution": "Provided by Example Organization",
                "collections": []
            }

        # get existing newspaper identifiers
        ids = set([n['@id'] for n in iiif['collections']])

        # add newspaper titles that aren't already there
        for newspaper in batch.newspapers:
            np_uri = self.uri(newspaper.uri)
            if np_uri not in ids:
                ids.add(np_uri)
                iiif['collections'].append({
                    "@id": np_uri,
                    "@type": "sc:Collection",
                    # TODO: put the newspaper title here
                    "label": newspaper.lccn
                })

        # write iiif data to disk 
        logging.info("writing newspaper collection to %s", path)
        json.dump(iiif, open(path, "w"), indent=2)


    def write_newspaper(self, newspaper):
        path = self.abspath(newspaper.uri)
        dir = dirname(path)
        if not isdir(dir):
            logging.info("making %s", dir)
            mkdir(dir)

        # load any existing iiif from previous batch
        if isfile(path):
            logging.info("reading existing newspaper data at %s", path)
            iiif = json.load(open(path))
        else:
            # TODO: pull label and attribution from somewhere
            iiif = {
                "@context": "http://iiif.io/api/presentation/2/context.json",
                "@id": self.uri(newspaper.uri),
                "@type": "sc:Collection",
                "label": "Newspaper",
                "attribution": "Provided by Example Organization",
                "manifests": []
            }

        for issue in newspaper.issues:
            iiif['manifests'].append({
                "@id": self.uri(issue.uri),
                "@type": "sc:Manifest",
                "label": issue.date_issued_str
            })

        logging.info("writing newspaper data to %s", path)
        json.dump(iiif, open(path, "w"), indent=2)


    def write_issue(self, issue):
        path = self.abspath(issue.uri)
        dir = dirname(path)
        if not isdir(dir):
            mkdir(dir)

        canvases = []
        for page in issue.pages:

            # some pages can be blank and have no image
            if not page.tiff_filename:
                continue

            page_uri = self.uri(page.uri)
            
            if self.image_server:
                tiff_filename = relpath(page.tiff_filename, dirname(issue.batch.dir.rstrip("/")))
                print("Joining %s and %s" % (self.image_server, tiff_filename))
                service_uri = urljoin(self.image_server, tiff_filename)
                thumbnail_url = join(service_uri, "full", '400,', '0', 'default.jpg')
            else:
                tiles_dir = self.abspath(page.uri)
                # TODO: have generate tiles return the thumbnail?
                self.generate_tiles(page, tiles_dir)
                service_uri = page_uri
                thumbnail_url = self.thumbnail_url(page)

            canvases.append({
                "@id": page_uri,
                "@type": "sc:Canvas",
                "label": "page %s" % page.sequence,
                "height": page.height,
                "width": page.width,
                "thumbnail": thumbnail_url,
                "images": [{
                    "@id": page_uri,
                    "@type": "oa:Annotation",
                    "motivation": "sc:painting",
                    "resource": {
                        "@id": page_uri,
                        "@type": "dctypes:Image",
                        "format": "image/jpeg",
                        "height": page.height,
                        "width": page.width,
                        "service": {
                            "@id": service_uri,
                            "@context": "http://iiif.io/api/image/2/context.json",
                            "profile": "http://iiif.io/api/image/2/level0.json"
                        }
                    }
                }]
            })

        sequence = {
            # TODO: better @id?
            "@id": "normal",
            "@type": "sc:Sequence",
            "label": "page order",
            "canvases": canvases,
        }

        iiif = {
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@id": self.uri(issue.uri),
            "@type": "sc:Manifest",
            "label": issue.date_issued_str,
            "sequences": [sequence]
        }

        logging.info("writing issue data %s", path)
        json.dump(iiif, open(path, "w"), indent=2)


    def generate_tiles(self, page, dest):
        tiles_dest = dirname(dest)
        sg = iiif.static.IIIFStatic(src=page.tiff_filename, dst=tiles_dest, tilesize=1024, api_version="2.0")
        sg.generate(page.tiff_filename, str(page.sequence))
        info_path = join(dest, "info.json")
        info = json.load(open(info_path))
        info['@id'] = self.uri(page.uri)
        json.dump(info, open(info_path, 'w'), indent=2)


    def thumbnail_url(self, page):
        """
        Get the widest thumbnail generated in the tiles_dir.
        """
        tiles_dir = self.abspath(page.uri)
        width_dirs = listdir(join(tiles_dir, "full"))
        widths = [int(s.split(",")[0]) for s in width_dirs]
        widths.sort()
        max_width = "%s," % widths.pop()
        path = join(page.uri, "full", max_width, '0', 'default.jpg')
        return self.uri(path)
