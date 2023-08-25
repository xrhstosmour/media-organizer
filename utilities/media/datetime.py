from datetime import datetime

from exifread.classes import IfdTag

from enumerations.media_type import MediaType
from helpers.datetime import get_oldest_datetime


def extract_metadata_datetime(metadata: dict, media_path: str) -> datetime:
    """Extract the datetime the picture was taken.
    If the datetime is not available, return the current one.

    Args:
        metadata (dict): The media file metadata.
        media_path (str): The path to the media file.

    Returns:
        datetime: The datetime object when the image was taken.
    """

    # Declare the variable that will hold the datetime when the image was taken.
    datetime_taken: datetime

    # Extract the datetime the picture was taken.
    metadata_datetime_taken: IfdTag | None = metadata.get(
        "EXIF DateTimeOriginal", None
    )

    # If the datetime is available, proceed.
    if metadata_datetime_taken:
        try:
            # Convert the metadata datetime to a datetime object.
            datetime_taken = datetime.strptime(
                str(metadata_datetime_taken), "%Y:%m:%d %H:%M:%S"
            )
        except ValueError:
            # Otherwise, get the oldest datetime when the image was created.
            datetime_taken = get_oldest_datetime(media_path=media_path)
    else:
        # Otherwise, get the oldest datetime when the image was created.
        datetime_taken = get_oldest_datetime(media_path=media_path)

    # Finally, return the datetime when the image was generated.
    return datetime_taken


def format_datetime(
    datetime_taken: datetime,
    naming_datetime_format: str = None,
    time_zone: str = None,
) -> str:
    """Format the datetime to a preferred format.

    Args:
        datetime_taken (datetime): The datetime object when the image was taken.
        naming_datetime_format (str, optional):
            The format to use for converting. Defaults to None.
        time_zone (str, optional):
            The time zone to use for converting. Defaults to None.

    Returns:
        str: The formatted datetime.
    """

    # Convert the datetime using the provided time zone.
    if time_zone:
        datetime_taken = datetime_taken.astimezone(time_zone)
    else:
        datetime_taken = datetime_taken.astimezone()

    # Convert the datetime to preferred format, otherwise to the default.
    if naming_datetime_format:
        return datetime_taken.strftime(naming_datetime_format)
    else:
        return datetime_taken.strftime("%Y_%m_%d_T%H_%M_%S")


def get_datetime_taken(
    metadata: dict,
    media_type: MediaType,
    media_path: str,
    naming_datetime_format: str = None,
    time_zone: str = None,
) -> datetime:
    """Get the datetime the picture was taken.

    Args:
        metadata (dict): The media file metadata.
        media_type (MediaType): The type of the media file.
        media_path (str): The path to the media file.
        naming_datetime_format (str, optional):
            The format to use for converting. Defaults to None.
        time_zone (str, optional):
            The time zone to use for converting. Defaults to None.

    Returns:
        datetime: The datetime object when the image was taken.
    """

    # Extract the datetime if available.
    # TODO: Check if there is a valid tool to get video datetime metadata.
    datetime_taken: datetime = (
        extract_metadata_datetime(metadata=metadata, media_path=media_path)
        if media_type is MediaType.IMAGE
        else get_oldest_datetime(media_path=media_path)
    )

    # Finally, return the formatted datetime.
    return format_datetime(
        datetime_taken=datetime_taken,
        naming_datetime_format=naming_datetime_format,
        time_zone=time_zone,
    )
