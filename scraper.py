import os
import sys
import time

try:
    import requests
except ImportError:
    print("'requests' module is not installed", file=sys.stderr)
    sys.exit(1)

from extractors.dvach import Dvach
from extractors.fourchan import Fourchan


class Scraper:
    """The main scraper class"""
    def __init__(self, urls, mode, output, pause):
        self.urls = urls
        self.mode = mode
        self.output = output
        self.pause = pause

        self.urls_len = len(self.urls)
        self.is_single_mode = self.urls_len == 1

        self.extractors = (
            Dvach,
            Fourchan,
        )

    def scrap(self):
        """Fires the scraping according to the URL amount"""
        if self.is_single_mode:
            self.scrap_thread(self.urls[0])
        else:
            self.scrap_multiple_threads()

    def scrap_thread(self, url):
        """Scraps the thread according to self params and URL"""
        print(f"Scraping '{url}'")
        #  Select the extractor
        #  Get the files' urls and names
        #  Count files, print a message if there are no files and finish
        #  Create a separate directory if not single-mode
        #  Download the files

    def scrap_multiple_threads(self):
        """Batch scraps the threads according to self params"""
        for i, url in enumerate(self.urls, start=1):
            print(f"\n[{i}/{self.urls_len}]")
            self.scrap_thread(url)
