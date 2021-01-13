# This module provides general functions for thread parsing
import os
import re
import sys

try:
    import requests
except ImportError:
    print("'requests' module is not installed", file=sys.stderr)
    sys.exit(1)

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


def select_extractor(url):
    """Returns a corresponding extractor depending on the thread URL"""
    # Set up regexps
    dvach_re = re.compile(r"""https://
                              2ch\.hk/
                              \w{1,4}/
                              res/
                              \d+\.html
                              (\#\d+)?""", re.X)
    fourchan_re = re.compile(r"""https://
                                 boards\.4chan(nel)?\.org/
                                 \w{1,4}/
                                 thread/
                                 \d+/
                                 [a-zA-Z0-9\-]+
                                 (\#p\d+)?""", re.X)
    extractor = None
    if dvach_re.match(url):
        extractor = Dvach(url)
    elif fourchan_re.match(url):
        extractor = Fourchan(url)
    return extractor


def download_files(file_list, mode, directory, amount):
    """Loops through the files in the file_list & downloads them"""
    # Set up the counter
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
            print("{:>4}/{} - {}".format(n, amount, file_name))
            # Update the counter
            n += 1


def parse_multiple_threads(urls, mode, directory):
    """Loops through the links & calls parse_thread() on each"""
    # Set up the counter
    n = 1
    total = len(urls)
    # Parse multiple threads
    for url in urls:
        # Log
        print("\n[{} out of {}]".format(n, total))
        parse_thread(url, mode, directory)
        n += 1


def create_thread_directory(directory, name, number):
    """Creates & returns the thread-specific directory path"""
    new_dir = os.path.join(directory, "{}_{}".format(name, number))
    # Create the directory if it does not exist
    if not os.path.isdir(new_dir):
        os.mkdir(new_dir)
    return new_dir


def parse_thread(url, mode, directory, single=False):
    """Does the job on one thread"""
    # Log current thread
    print("Parsing '{}'".format(url))

    # Select the extractor
    extractor = select_extractor(url)
    # Check if it's valid
    if extractor is None:
        print("URL '{}' is not supported.")
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
        directory = create_thread_directory(directory, extractor.name,
                                            extractor.thread_number)

    # Download the files
    print("Downloading...")
    download_files(file_list, mode, directory, amount)
