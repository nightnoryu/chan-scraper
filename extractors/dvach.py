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


def get_files_urls_names(url):
    """Returns a list of tuples (file URL, file name) in thread"""
    # Get the JSON response
    api_url = get_api_url(url)
    response = requests.get(api_url)
    # Parse it down
    res_json = response.json()
    posts = res_json["threads"][0]["posts"]
    # Create a list of URLs
    file_list = []
    for post in posts:
        for file in post["files"]:
            file_list.append((get_file_url(file), file["name"]))
    return file_list
