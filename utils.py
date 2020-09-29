# This module provides general functions


import os

import requests

from extractors.dvach import Dvach
from extractors.fourchan import Fourchan


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


def what_board_is_this(url):
    """Returns a name of the board depending on the thread URL"""
    board = None
    if url.startswith("https://2ch."):
        board = "2ch"
    elif (url.startswith("https://boards.4channel.org") or
          url.startswith("https://boards.4chan.org")):
        board = "4chan"
    return board


def parse_thread(url, mode, directory, single=False):
    """Does the job on one thread"""
    # Log current thread
    print("Parsing '{}'".format(url))

    # Select the extractor
    extractor = None
    if what_board_is_this(url) == "2ch":
        extractor = Dvach(url)
    elif what_board_is_this(url) == "4chan":
        extractor = Fourchan(url)
    else:
        print("URL '{}' is not supported.".format(url))
        return

    try:
        # Get all the information
        file_list = extractor.get_files_urls_names()
        amount = count_files(file_list, mode)
    except Exception as ex:
        # Handle requests exceptions
        print("Request error: {}".format(ex))
        print("Download failed for '{}'.".format(url))
        return

    # Check if there are any files
    if amount == 0:
        print("There are no files in this thread: {}".format(url))
        return

    # Create a separate directory for this thread if there are many
    if not single:
        number = extractor.thread_number
        # Create a new directory for this thread
        directory = os.path.join(directory,
                                 "{}_{}".format(extractor.name, number))
        # Check if the directory already exists
        if not os.path.isdir(directory):
            os.mkdir(directory)

    # Actual downloading is happening here
    print("Downloading...")
    # Posts loop
    n = 1
    for file_url, file_name in file_list:
        ext = get_extension(file_url)
        # Save the files according to the mode
        if ((mode == "images" and is_image(ext)) or
            (mode == "videos" and is_video(ext)) or
            (mode == "all")):
            # Save the file
            save_file(file_url, directory, file_name)
            # Log the action
            print("{:>3}/{} - {}".format(n, amount, file_name))
            # Update counter
            n += 1
