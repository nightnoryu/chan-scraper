#!/usr/bin/env python3

import argparse
import os
import sys
from textwrap import dedent

import utils

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CustomArgumentParser(argparse.ArgumentParser):
    """Override ArgumentParser's help message"""
    def format_help(self):
        help_text = dedent(f"""\
        Chan scraper is a script for downloading attachments from one or several
        threads on 2ch or 4chan.

        Usage: {self.prog} [OPTIONS] URL [URL]...

        URL:
          Thread's URL

        Options:
          -h,  --help     show help
          -m,  --mode     specify content for downloading:
                          all, images, videos (def: {self.get_default("mode")})
          -o,  --output   output directory (def: current)

        For more information visit:
        https://github.com/m3tro1d/chan-scraper
        """)
        return help_text

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def valid_dir(string):
    """Checks and returns the output directory path"""
    path = os.path.abspath(string)
    if not os.path.isdir(path):
        os.mkdir(path)
    return path


def parse_arguments():
    """Process input arguments"""
    parser = CustomArgumentParser(usage="%(prog)s [OPTIONS] URL [URL]...")

    parser.add_argument("-m", "--mode", choices=["all", "images", "videos"],
                        default="all")

    parser.add_argument("-o", "--output", default=".", type=valid_dir)

    parser.add_argument("urls", nargs="+")

    return parser.parse_args()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main script
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    """Entry point of the script"""
    if len(args.urls) == 1:
        utils.parse_thread(args.urls[0], args.mode, args.output, True)
    else:
        utils.parse_multiple_threads(args.urls, args.mode, args.output)


# Entry point
if __name__ == "__main__":
    args = parse_arguments()

    try:
        main()
    except KeyboardInterrupt:
        print("\nUser interrupt", file=sys.stderr)
        sys.exit(1)
