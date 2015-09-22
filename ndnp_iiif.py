#!/usr/bin/env python

import json
import lxml

class Batch:
    def __init__(self):
        self.newspapers = []

class Newspaper:
    def __init__(self):
        self.issues = []

class Issue:
    def __init__(self):
        self.pages = []

class Page:
    def __init__(self):
        pass

def load_batch(batch_dir, iiif_dir):
    batch = Batch()
    newspaper = Newspaper()
    issue = Issue()
    page = Page()

    batch.newspapers.append(newspaper)
    newspaper.issues.append(issue)
    issue.pages.append(page)

    return batch
    
