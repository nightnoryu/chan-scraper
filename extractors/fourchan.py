# This extractor supports 4chan threads on https://boards.4channel.org


import requests


THREAD_BASE_URL = "https://a.4cdn.org/"
MEDIA_BASE_URL  = "https://i.4cdn.org/"


def get_thread_number(url):
    """Returns thread's number"""
    # Get the JSON response
    api_url = get_thread_api_url(url)
    response = requests.get(api_url)
    # Check response status
    response.raise_for_status()
    # Parse it down
    res_json = response.json()
    return int(res_json["posts"][0]["no"])


def get_thread_api_url(url):
    """Returns an API URL for a thread"""
    # We're grabbing only board/thread/number
    return THREAD_BASE_URL + "/".join(url.split("/")[3:6]) + ".json"


def get_board_name(url):
    """Returns board's name of the thread URL"""
    return url.split("/")[3]


def get_file_url(post, board_name):
    """Returns a ready-to-download URL to an image in the post"""
    return MEDIA_BASE_URL + board_name + "/" + str(post["tim"]) + post["ext"]


def get_files_urls_names(url):
    """Returns a list of tuples (file URL, file name) in thread"""
    # Get the name of the board
    board_name = get_board_name(url)
    # Get the JSON response
    api_url = get_thread_api_url(url)
    response = requests.get(api_url)
    # Check response status
    response.raise_for_status()
    # Parse it down
    res_json = response.json()
    posts = res_json["posts"]
    # Create a list of URLs
    file_list = []
    for post in posts:
        # Not all posts have files, so we'd better check
        if "tim" in post.keys():
            name = str(post["tim"]) + post["ext"]
            file_list.append((get_file_url(post, board_name), name))
    return file_list
