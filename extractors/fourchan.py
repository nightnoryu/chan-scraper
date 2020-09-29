import requests


class Fourchan():
    """This extractor supports 4chan threads on https://boards.4channel.org"""
    def __init__(self, url):
        # Basic properties
        self.url = url
        self.NAME = "fourchan"
        self.THREAD_BASE_URL = "https://a.4cdn.org/"
        self.MEDIA_BASE_URL  = "https://i.4cdn.org/"
        # Set up thread for processing
        self.get_thread_json()
        self.get_thread_number()
        self.get_board_name()

    def get_thread_json(self):
        """Sets self.thread_json according to self.url"""
        # Get the JSON response
        api_url = self.get_api_url(self.url)
        response = requests.get(api_url)
        # Check response status
        response.raise_for_status()
        # Parse it down
        self.thread_json = response.json()

    def get_thread_number(self):
        """Sets self.thread_number according to self.url"""
        self.thread_number = int(self.thread_json["posts"][0]["no"])

    def get_api_url(self, url):
        """Returns an API URL for a thread"""
        # We're grabbing only board/thread/number
        return self.THREAD_BASE_URL + "/".join(url.split("/")[3:6]) + ".json"

    def get_board_name(self):
        """Sets self.board_name according to self.url"""
        self.board_name = self.url.split("/")[3]

    def get_file_url(self, post):
        """Returns a ready-to-download URL to an image in the post"""
        return self.MEDIA_BASE_URL + self.board_name + "/" + str(post["tim"]) + post["ext"]

    def get_files_urls_names(self):
        """Returns a list of tuples (file URL, file name) in thread"""
        posts = self.thread_json["posts"]
        # Create a list of URLs
        file_list = []
        for post in posts:
            # Not all posts have files, so we'd better check
            if "tim" in post.keys():
                name = str(post["tim"]) + post["ext"]
                file_list.append((self.get_file_url(post), name))
        return tuple(file_list)
