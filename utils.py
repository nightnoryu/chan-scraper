# This module provides general functions


import os

import requests


def get_extension(name):
    """Returns file's extension without dot"""
    return name.split(".")[-1]


def is_image(ext):
    return (ext == "jpg" or ext == "jpeg" or
        ext == "png" or ext =="gif")


def is_video(ext):
    return ext == "webm" or ext == "mp4"


def count_files(files_list, mode="all"):
    """Returns files amount according to the specified mode"""
    n = 0
    for _, file_name in files_list:
        ext = get_extension(file_name)
        if ((mode == "images" and is_image(ext)) or
            (mode == "videos" and is_video(ext)) or
            (mode == "all")):
            n += 1
    return n


def save_file(url, directory, name):
    """Save a file into the specified directory"""
    # Check if the image already exists
    full_name = os.path.join(directory, name)
    # Do not replace files
    if not os.path.isfile(full_name):
        with open(full_name, "wb") as file:
            for chunk in requests.get(url):
                file.write(chunk)
