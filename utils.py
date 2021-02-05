# This module provides general functions for thread parsing
import os
import sys
import time

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
    """Returns true if ext is image type"""
    return ext in ("jpg", "jpeg", "png", "gif")


def is_video(ext):
    """Returns true if ext is video type"""
    return ext in ("webm", "mp4")


def count_files(files_list, mode="all"):
    """Returns files amount according to the specified mode"""
    count = 0
    for _, file_name in files_list:
        ext = get_extension(file_name)
        if ((mode == "images" and is_image(ext)) or
            (mode == "videos" and is_video(ext)) or
            (mode == "all")):
            count += 1
    return count


def req_get(url):
    """Makes a proper GET request and returns the response object"""
    response = requests.get(url)
    response.raise_for_status()
    return response


def save_file(url, directory, name):
    """Save a file into the specified directory
    Returns False if file already exists, True otherwise"""
    # Check if the image already exists
    full_name = os.path.join(directory, name)
    # Do not replace files
    if not os.path.isfile(full_name):
        with open(full_name, "wb") as file:
            for chunk in req_get(url):
                file.write(chunk)
        return True
    return False


def select_extractor(url):
    """Returns a corresponding extractor depending on the thread URL"""
    # Modify this to add a new extractor
    extractors = (
        Dvach,
        Fourchan,
    )
    # Go through the extractors to find the needed one
    for ex in extractors:
        match = ex.match(url)
        if match:
            return ex(match.group(0))
    return None


def download_files(file_list, mode, directory, amount, pause):
    """Loops through the files in the file_list & downloads them"""
    for i, (file_url, file_name) in enumerate(file_list, start=1):
        ext = get_extension(file_url)
        # Save the files according to the mode
        if ((mode == "images" and is_image(ext)) or
            (mode == "videos" and is_video(ext)) or
            (mode == "all")):
            try:
                # Save the file
                if save_file(file_url, directory, file_name) and pause:
                    # If pause is True, sleep to prevent server throttling
                    time.sleep(0.5)
            except Exception as err:
                print(f"Error! {i:>4}/{amount} - {file_name}: {err}",
                      file=sys.stderr)
            else:
                print(f"{i:>4}/{amount} - {file_name}")


def parse_multiple_threads(urls, mode, directory, pause):
    """Loops through the links & calls parse_thread() on each"""
    for i, url in enumerate(urls, start=1):
        print(f"\n[{i}/{len(urls)}]")
        parse_thread(url, mode, directory, pause)


def create_thread_directory(directory, name, number):
    """Creates & returns the thread-specific directory path"""
    new_dir = os.path.join(directory, f"{name}_{number}")
    # Create the directory if it does not exist
    if not os.path.isdir(new_dir):
        os.mkdir(new_dir)
    return new_dir


def parse_thread(url, mode, directory, pause, single=False):
    """Does the job on one thread"""
    # Log current thread
    print(f"Parsing '{url}'")

    # Select the extractor and handle request errors
    try:
        extractor = select_extractor(url)
        # Check if it's valid
        if extractor is None:
            raise Exception("URL is not supported.")
    except Exception as err:
        print(f"Error while selecting extractor for {url}: {err}",
              file=sys.stderr)
        return

    # Get all the information
    file_list = extractor.get_files_urls_names()
    amount = count_files(file_list, mode)
    # Check if there are any files
    if amount == 0:
        print(f"There are no specified files in this thread: {extractor.url}")
        return

    # Create a separate directory for this thread if there are many
    if not single:
        directory = create_thread_directory(directory, extractor.name,
                                            extractor.thread_number)
    # Download the files
    download_files(file_list, mode, directory, amount, pause)
