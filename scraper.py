class Scraper:
    """The main scraper class"""
    def __init__(self, urls, mode, output, pause):
        self.urls = urls;
        self.mode = mode;
        self.output = output;
        self.pause = pause;

        self.single = len(self.urls) == 1

    def scrap(self):
        """Performs the downloading"""
        pass
