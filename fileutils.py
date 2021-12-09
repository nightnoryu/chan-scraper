def get_and_check_amount(file_list):
    """Raises an exception if the list is empty, otherwise returns length"""
    if not file_list:
        raise Exception("There are no files")
    return len(file_list)


def get_extension(file_name):
    """Returns files extension"""
    return file_name.split(".")[-1]


def is_image(ext):
    """Returns true if ext is an image type"""
    return ext in ("jpg", "jpeg", "png", "gif")


def is_video(ext):
    """Returns true if ext is a video type"""
    return ext in ("webm", "mp4")
