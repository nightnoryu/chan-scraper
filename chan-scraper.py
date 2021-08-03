#!/usr/bin/env python3

import sys

from args import parse_arguments
from scraper import Scraper


def main(args):
    scraper = Scraper(args.urls, args.mode, args.output, args.pause)
    scraper.scrap()


if __name__ == "__main__":
    args = parse_arguments()
    try:
        main(args)
    except KeyboardInterrupt:
        print("\nUser interrupt", file=sys.stderr)
        sys.exit(1)
