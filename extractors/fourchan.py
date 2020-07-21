# This extractor supports 4chan threads on https://boards.4channel.org


THREAD_BASE_URL = "https://a.4cdn.org/"
MEDIA_BASE_URL  = "https://i.4cdn.org/"


def get_thread_api_url(url):
    """Returns an API URL for a thread"""
    # We're grabbing only board/thread/number
    return THREAD_BASE_URL + "/".join(url.split("/")[3:6]) + ".json"
