# Thread parser
This program is capable of downloading attachments from threads on [2ch](https://2ch.hk). You can select what to download: images, videos or all files.

## Usage
```
thread-parser.py [-h] [-o DIR] {all,images,videos} URL

positional arguments:
  {all,images,videos}  parse mode, e.g. what files to download
  URL                  thread url

optional arguments:
  -h, --help           show this help message and exit
  -o DIR               output directory (default: current)
```
