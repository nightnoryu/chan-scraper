# Thread parser
This program is capable of downloading attachments from threads on [2ch](https://2ch.hk). You can select what to download: images, videos or all files.

## Requirements
* Python 3
* [requests](https://pypi.org/project/requests/)

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

For example:

```
py thread-parser.py images https://2ch.hk/s/res/2127464.html -o img
```

This will download all images from the 2127464 thread on /s/ in the `img` folder.

__Attention__: by default, if the directory you have selected with `-o` option
exists and there was an image with the conflicting name it won't be replaced.
