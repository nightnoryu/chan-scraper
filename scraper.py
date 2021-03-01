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

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Constants
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

EXTRACTORS = (
    Dvach,
    Fourchan,
)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Scraper class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Scraper:
    """The main scraper class"""
    def __init__(self, urls, mode, output, pause):
        self.urls = urls
        self.mode = mode
        self.output = output
        self.pause = pause

    def scrap(self):
        """Fires the scraping according to the URL amount"""
        if self.is_single_url():
            self.scrap_thread(self.urls[0])
        else:
            self.scrap_multiple_threads()

    def is_single_url(self):
        """Checks if only one URL was provided"""
        return len(self.urls) == 1

    def scrap_thread(self, url):
        """Scraps the thread according to self params and URL"""
        pass

    def scrap_multiple_threads(self):
        """Batch scraps the threads according to self params"""
        pass
