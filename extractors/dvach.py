# This extractor supports dvach threads on https://2ch.hk


import requests


BASE_URL = "https://2ch.hk"


def get_api_url(url):
    """Returns an API url (html -> json)"""
    array = url.split(".")
    api_url = ".".join(array[:-1])
    return api_url + ".json"


def get_file_url(file):
    """Returns a ready-to-download file URL"""
    return BASE_URL + file["path"]


def get_files_urls(url):
    """Returns a list of file URLs in thread"""
    # Get the JSON response
    api_url = get_api_url(url)
    try:
        response = requests.get(api_url)
    except Exception as ex:
        # Handle all requests exceptions
        print("Request error: {}".format(ex))
        print("Download failed, exiting.")
        sys.exit(1)
    # Parse it down
    res_json = response.json()
    posts = res_json["threads"][0]["posts"]
    # Create a list of URLs
    urls = []
    for post in posts:
        for file in post["files"]:
            urls.append(get_file_url(file))


def count_files(posts, mode="all"):
    """Counts all files according to the mode"""
    n = 0
    for post in posts:
        for file in post["files"]:
            ext = get_extension(file["name"])
            if mode == "images" and is_image(ext):
                n += 1
            elif mode == "videos" and is_video(ext):
                n += 1
            elif mode == "all":
                n += 1
    return n
