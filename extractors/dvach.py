import requests


class Dvach():
    """This extractor supports dvach threads on https://2ch.hk"""
    def __init__(self, url):
        # Basic properties
        self.url = url
        self.NAME = "dvach"
        self.BASE_URL = "https://2ch.hk"
        # Set up thread for processing
        self.get_thread_json()
        self.get_thread_number()

    def get_thread_json(self):
        """Sets self.thread_json according to self.url"""
        # Get the JSON response
        api_url = self.get_api_url(self.url)
        response = requests.get(api_url)
        # Check response status
        response.raise_for_status()
        # Parse the JSON
        self.thread_json = response.json()

    def get_thread_number(self):
        """Sets self.thread_number according to self.url"""
        self.thread_number = int(self.thread_json["current_thread"])

    def get_api_url(self, url):
        """Returns an API url (html -> json)"""
        array = url.split(".")
        api_url = ".".join(array[:-1])
        return api_url + ".json"

    def get_file_url(self, file):
        """Returns a ready-to-download file URL"""
        return self.BASE_URL + file["path"]

    def get_files_urls_names(self):
        """Returns a list of tuples (file URL, file name) in thread"""
        # Get the posts
        posts = self.thread_json["threads"][0]["posts"]
        # Create a list of URLs
        file_list = []
        for post in posts:
            for file in post["files"]:
                file_list.append((self.get_file_url(file), file["name"]))
        return tuple(file_list)
