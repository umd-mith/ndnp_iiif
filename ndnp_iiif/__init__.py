import logging

from . import reader
from . import writer

def load_batch(batch_dir, iiif_dir, base_uri="", image_server=""):
    logging.info("loading ndnp batch %s into %s", batch_dir, iiif_dir)

    batch = reader.Batch(batch_dir)

    wr = writer.Writer(iiif_dir, base_uri, image_server)
    wr.write(batch)

    return batch


