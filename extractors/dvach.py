import re
import sys

try:
    import requests
except ImportError:
    print("'requests' module is not installed", file=sys.stderr)
    sys.exit(1)


class Dvach():
    """This extractor supports dvach threads on https://2ch.hk"""
    def __init__(self, url):
        # Basic properties
        self.url = url
        self.name = "dvach"
        self.base_url = "https://2ch.hk"
        # Set up thread for processing
        self.get_api_url()
        self.get_thread_json()
        self.get_thread_number()

    @staticmethod
    def match(url):
        pattern = re.compile(r"""https://
            2ch\.hk/
            \w{1,4}/
            res/
            \d+\.html
            (\#\d+)?/?""", re.X)
        return pattern.match(url)

    def get_thread_json(self):
        """Sets self.thread_json according to self.url"""
        response = requests.get(self.api_url)
        response.raise_for_status()
        self.thread_json = response.json()

    def get_thread_number(self):
        """Sets self.thread_number according to self.thread_json"""
        self.thread_number = int(self.thread_json["current_thread"])

    def get_api_url(self):
        """Sets self.thread_json according to self.url"""
        array = self.url.split(".")
        self.api_url = ".".join(array[:-1]) + ".json"

    def get_file_url(self, file):
        """Returns a ready-to-download file URL"""
        return self.base_url + file["path"]

    def get_files_urls_names(self):
        """Returns a tuple of tuples (file URL, file name) in thread"""
        # Get the posts
        posts = self.thread_json["threads"][0]["posts"]
        # Create a list of URLs
        file_list = []
        for post in posts:
            for file in post["files"]:
                file_list.append((self.get_file_url(file), file["name"]))
        return tuple(file_list)
