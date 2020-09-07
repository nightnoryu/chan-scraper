# Thread parser
This program is capable of downloading attachments from threads on [2ch](https://2ch.hk) and [4chan](https://4channel.org). You can select what to download: images, videos or all files.

## Requirements
* Python 3
* [requests](https://pypi.org/project/requests/)

## Usage
```
usage: thread-parser.py [-h] [-o DIR] {all,images,videos} [URLS [URLS ...]]

positional arguments:
  {all,images,videos}  parse mode, e.g. what files to download
    URLS                 thread urls

    optional arguments:
      -h, --help           show this help message and exit
        -o DIR               output directory (default: current)
```

For example:

```
py thread-parser.py images https://2ch.hk/s/res/2127464.html -o img
```

This will download all images from the 2127464 thread on /s/ in the `img` folder.

Another one:

```
py thread-parser.py all https://boards.4channel.org/g/thread/77369090 https://boards.4channel.org/g/thread/77368911 -o threads
```

This will download all files from both threads and place them into separate folders with their thread number in the `threads` folder.

__Attention__: by default, if the directory you have selected with `-o` option
exists and there was an image with the conflicting name it won't be replaced.

## Extending
If you want to add support for another imageboard, there is a simple scheme for an 'extractor'. It must contain the following properties:

  - `NAME` - a string representing imageboard's name. For example: `NAME = "fourchan"`;
  - `get_thread_number(url)` - a function that returns thread's number int according to the URL;
  - `get_files_urls_names(url)` - a function that returns a list of tuples, each containing file's URL and name;

Background implementation is up to you, but I suggest reading the documentation on imageboard's API.
