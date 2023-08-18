import shutil
from pathlib import Path

import exifread

from enumerations.media_type import MediaType
from utilities.media.datetime import get_datetime_taken
from utilities.media.location import get_location_taken


def rename_media_files(
    base_directory: Path,
    media_path: Path,
    media_type: MediaType,
    naming_datetime_format: str = None,
    time_zone: str = None,
) -> None:
    """Rename the media file.

    Args:
        base_directory (Path):
            The base directory where the media files are stored.
        media_path (Path): The path to the media file.
        media_type (MediaType): The type of the media file.
        naming_datetime_format (str, optional):
            The format to use for converting. Defaults to None.
        time_zone (str, optional):
            The time zone to use for converting. Defaults to None.
    """

    try:
        # Get the metadata.
        metadata: dict | None = None
        if media_type is MediaType.IMAGE:
            with media_path.open("rb") as media_file:
                metadata = exifread.process_file(media_file)

        # TODO: Check if the media file has already been organized,
        # TODO: without using the metadata, and corrupt the image.

        # TODO: Check if there is a valid tool to get video datetime metadata.
        # Extract the formatted datetime the picture was taken.
        formatted_datetime: str = get_datetime_taken(
            metadata=metadata,
            media_type=media_type,
            media_path=media_path,
            naming_datetime_format=naming_datetime_format,
            time_zone=time_zone,
        )

        # TODO: Check if there is a valid tool to get video location metadata.
        # Extract the formatted location the picture was taken.
        formatted_city, formatted_country = get_location_taken(
            metadata=metadata, media_type=media_type
        )

        # Determine the new media file name and destination directory
        nea_media_file_name: str = f"{formatted_datetime}{media_path.suffix}"
        destination_directory: Path = media_path.parent

        # Create a potential destination path based on the country and city.
        potential_destination_directory: Path = base_directory
        # If the country is valid, then add it to the potential destination.
        if formatted_country:
            potential_destination_directory = (
                potential_destination_directory / formatted_country
            )
            # If the city is valid, add it to the potential destination.
            if formatted_city:
                potential_destination_directory = (
                    potential_destination_directory / formatted_city
                )

        # Check if the media file is already in the desired location.
        if potential_destination_directory != media_path.parent:
            # If not, update the destination.
            destination_directory = potential_destination_directory

            # Finally, create the destination if it does not exist,
            # including any necessary parent directories.
            if not destination_directory.exists():
                destination_directory.mkdir(parents=True, exist_ok=True)

        # TODO: Do not move to other parent directory.
        # Construct the new media path.
        new_media_path: Path = destination_directory / nea_media_file_name

        # TODO: Handle duplicate media files via their datetime.
        # Move the media media file to the new path only if it's not there.
        if new_media_path != media_path:
            shutil.move(media_path, new_media_path)
    except Exception as exception:
        print(f"Error processing {media_path}: {exception}")


def rename_and_organize_media_files(
    directory_path: str,
    naming_datetime_format: str = None,
    time_zone: str = None,
) -> None:
    """Rename and organize the media files in the specified directory.

    Args:
        directory_path (str):
            The path to the directory containing the media files.
        naming_datetime_format (str, optional):
            The format to use for converting. Defaults to None.
        time_zone (str, optional):
            The time zone to use for converting. Defaults to None.
    """
    # The media file extensions that you want to process.
    image_extensions: set = {
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".tiff",
        ".bmp",
        ".webp",
        ".heic",
        ".heif",
        ".svg",
        ".ico",
        ".raw",
    }
    video_extensions: set = {".mp4", ".avi", ".mkv", ".flv", ".wmv"}

    # Initialize the directory path as a Path object.
    directory = Path(directory_path)

    # Iterate through all media files in the directory and its subdirectories.
    for media_path in directory.rglob("*"):
        # Check if the media file has one of the media extensions.
        if media_path.suffix.lower() in image_extensions | video_extensions:
            # Get the media type.
            media_type: MediaType = (
                MediaType.IMAGE
                if media_path.suffix.lower() in image_extensions
                else MediaType.VIDEO
            )

            # Rename the media file.
            rename_media_files(
                base_directory=directory,
                media_path=media_path,
                media_type=media_type,
                naming_datetime_format=naming_datetime_format,
                time_zone=time_zone,
            )
