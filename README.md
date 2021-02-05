# Chan scraper
This program is capable of downloading attachments from threads on [2ch](https://2ch.hk) and [4chan](https://4channel.org). You can select what to download: images, videos or all files.


## Requirements
- [Python 3](https://www.python.org/)
- [requests](https://pypi.org/project/requests/)
- (optional for downloading and updating) [git](https://git-scm.com/)


## Installation
Clone the repo using this command:

```
git clone https://github.com/m3tro1d/chan-scraper
```

Or just download the [zip](https://github.com/m3tro1d/chan-scraper/archive/master.zip).

Master branch is usually stable, so there won't be any issues.


## Usage
```
Usage: chan-scraper.py [OPTIONS] URL [URL]...

URL:
  Thread's URL

Options:
  -h,  --help     show help
  -m,  --mode     specify content for downloading:
                  all, images, videos (def: all)
  -p,  --pause    make a pause after each download
                  useful if the server throttles (def: False)
  -o,  --output   output directory (def: current)

For more information visit:
https://github.com/m3tro1d/chan-scraper
```

For example:

```
py chan-scraper.py -o img -m images https://2ch.hk/s/res/2127464.html
```

This will download all images from the 2127464 thread on /s/ in the `img` folder.

Another one:

```
py chan-scraper.py -o threads https://boards.4channel.org/g/thread/77369090 https://boards.4channel.org/g/thread/77368911
```

This will download all files from both threads and place them into separate folders with their thread number in the `threads` folder.

**Attention**: by default, if the directory you have selected with `-o` option exists and there was an image with the conflicting name it **won't** be replaced.


## Extending
If you want to add support for another imageboard, there is a simple scheme for an 'extractor'. It is a class containing the following properties:

- `name` - string representing imageboard's name. For example: `self.name = "fourchan"`. This is used for naming the directories when dowloading multiple threads;
- `match()` - a **static** method ([docs](https://docs.python.org/3/library/functions.html#staticmethod)) that returns a `re.match` object. Determines which links the extractor supports;
- `thread_number` - `int` with thread's number according to the URL;
- `get_files_urls_names()` - function that returns a tuple (or list) of tuples, each containing files' URL and name.

The constructor (e.g. `__init__`) **must** trow an error if a network error is encountered. All handling is done in `parse_thread()` in the utils.

Also make sure to modify the `select_extractor()` function in the utils: import your extractor and add it to the list.

Background implementation is up to you, but I suggest reading the documentation on imageboard's API and use it if possible. Also refer to the existing extractors for more practical info.


## TODO
- [x] Pass the thread if it yields an HTTP error and continue to other threads (and files)
- [x] Option to pause after each download to prevent server throttling
- [ ] Print the full information (summary) at the end of the downloading (make it an option?)
