import argparse
import os
import sys

# Check if the module is installed
try:
    # Change imports...
    import requests
except ImportError:
    print("Please install requests module.")
    sys.exit(1)

import utils


def parse_arguments():
    """Process input arguments"""
    parser = argparse.ArgumentParser(
        description="""Downloads all files, images or videos from one
        or several threads on 2ch or 4chan.""")

    # Change arguments...
    parser.add_argument("MODE", choices=["all", "images", "videos"],
        help="parse mode, e.g. what files to download")

    parser.add_argument("URLS", nargs="*",
        help="thread urls")

    parser.add_argument("--output", "-o", metavar="DIR", default=".",
        help="output directory (default: current)")

    args = parser.parse_args()
    return args


def check_arguments(urls, directory):
    """Checks if the arguments are valid"""
    # Check input URLs
    if not len(urls):
        print("Error: no URL provided.")
        sys.exit(1)
    # Check output directory
    if not os.path.isdir(directory):
        os.mkdir(directory)


def main():
    """Entry point of the script"""
    # Get the input arguments
    args = parse_arguments()
    mode = args.MODE
    urls = args.URLS
    directory = os.path.abspath(args.output)

    # Check the input arguments
    check_arguments(urls, directory)

    # Parse single thread
    if len(urls) == 1:
        utils.parse_thread(urls[0], mode, directory, True)
    # Parse multiple threads
    else:
        utils.parse_multiple_threads(urls, mode, directory)


# Entry point
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        utils.err("\nUser interrupt")
        sys.exit(1)
