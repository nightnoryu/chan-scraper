import argparse
import os
import sys

# Check if the module is installed
try:
    import requests
except ImportError:
    print("Please install requests module.")
    sys.exit(1)

import utils
import extractors.dvach as dvach
import extractors.fourchan as fourchan


def main():
    """Entry point of the script"""
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="""Downloads all files, images or videos from one
        or several threads on 2ch or 4chan.""")

    parser.add_argument("MODE", choices=["all", "images", "videos"],
        help="parse mode, e.g. what files to download")

    parser.add_argument("URLS", nargs="*",
        help="thread urls")

    parser.add_argument("-o", metavar="DIR", default=".",
        help="output directory (default: current)")

    args = parser.parse_args()
    mode = args.MODE
    urls = args.URLS
    directory = os.path.abspath(args.o)


    # Check input URLS
    if not len(urls):
        print("Error: no URL provided.")
        sys.exit(1)
    # Check output directory
    if not os.path.isdir(directory):
        os.mkdir(directory)

    if len(urls) == 1:
        # Parse single thread
        utils.parse_thread(urls[0], mode, directory, True)
    else:
        # Set up counter
        n = 1
        total = len(urls)
        # Parse multiple threads
        for url in urls:
            # Log
            print("\n[{} out of {}]".format(n, total))
            utils.parse_thread(url, mode, directory)
            n += 1


# Entry point
if __name__ == "__main__":
    main()
