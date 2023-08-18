import datetime
from os import stat
from os.path import getatime, getctime, getmtime


def get_oldest_datetime(media_path: str) -> datetime:
    """Get the oldest datetime possible from a media file.

    Args:
        media_path (str): The path to the media file.

    Returns:
        datetime: The oldest datetime possible.
    """

    # Get creation time if available, according to the OS.
    creation_time: float | None = None
    try:
        # For Unix.
        creation_time = stat(media_path).st_birthtime
    except AttributeError:
        # For Windows.
        creation_time = getctime(media_path)

    modification_time: float = getmtime(media_path)
    access_time: float = getatime(media_path)

    # Find the oldest time among the three.
    return datetime.datetime.fromtimestamp(
        min(creation_time, modification_time, access_time)
    )
