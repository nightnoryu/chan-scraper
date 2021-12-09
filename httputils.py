import os

import requests


def request_get(url):
    """Sends a properly structured GET request and returns the response"""
    response = requests.get(url)
    response.raise_for_status()
    return response


def save_file(url, name):
    """Save the file on the URL; returns True if the file was downloaded"""
    if not os.path.isfile(name):
        with open(name, "wb") as file:
            for chunk in request_get(url):
                file.write(chunk)
        return True
    return False
