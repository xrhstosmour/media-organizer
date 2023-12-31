from pathlib import Path

import exifread

from enumerations.media_type import MediaType
from utilities.media.datetime import get_datetime_taken
from utilities.media.location import get_location_taken
from utilities.media.operations import (
    delete_empty_directories,
    move_without_overwrite,
)


def rename_media_files(
    base_directory: Path,
    media_path: Path,
    media_type: MediaType,
    location_searching: bool,
    naming_datetime_format: str = None,
    time_zone: str = None,
) -> Path:
    """Rename the media file.

    Args:
        base_directory (Path):
            The base directory where the media files are stored.
        media_path (Path): The path to the media file.
        media_type (MediaType): The type of the media file.
        location_searching (bool):
            If True, the location will be used for organizing the media files.
        naming_datetime_format (str, optional):
            The format to use for converting. Defaults to None.
        time_zone (str, optional):
            The time zone to use for converting. Defaults to None.

    Returns:
        Path: The new media file path.
    """

    try:
        # Get the metadata.
        metadata: dict | None = None
        if media_type is MediaType.IMAGE:
            try:
                with media_path.open("rb") as media_file:
                    metadata = exifread.process_file(media_file)
            except Exception as exception:
                print(f"Error processing {media_path}: {exception}")
                metadata = None

        # TODO: Check if media file has already been organized, via database.

        # Extract the formatted datetime the picture was taken.
        formatted_datetime: str = get_datetime_taken(
            metadata=metadata,
            media_type=media_type,
            media_path=media_path,
            naming_datetime_format=naming_datetime_format,
            time_zone=time_zone,
        )

        # Variable to store the formatted location the picture was taken.
        formatted_city: str | None = None
        formatted_municipality: str | None = None
        formatted_region: str | None = None
        formatted_country: str | None = None

        # Check if location searching is enabled.
        if location_searching:
            # Extract the formatted location the picture was taken.
            (
                formatted_city,
                formatted_municipality,
                formatted_region,
                formatted_country,
            ) = get_location_taken(metadata=metadata, media_type=media_type)

        # Determine the new media file name and destination directory
        nea_media_file_name: str = (
            f"{formatted_datetime}{media_path.suffix.lower()}"
        )
        destination_directory: Path = media_path.parent

        # Create a potential destination path based on the country, region
        # and city.
        potential_destination_directory: Path = base_directory

        # Flag to keep track if the media file should be moved,
        # according to location metadata.
        should_be_moved: bool = False

        # If the country is valid, then add it to the potential destination.
        if formatted_country:
            should_be_moved = True
            potential_destination_directory = (
                potential_destination_directory / formatted_country
            )

        # If the region is valid and different to country, add it to the
        # potential destination.
        if formatted_region and formatted_region != formatted_country:
            should_be_moved = True
            potential_destination_directory = (
                potential_destination_directory / formatted_region
            )

        # TODO: Do not create folder if it's the same as formatted_country too.
        # If the municipality is valid and different to region, add it to the
        # potential destination.
        if (
            formatted_municipality
            and formatted_municipality != formatted_region
        ):
            should_be_moved = True
            potential_destination_directory = (
                potential_destination_directory / formatted_municipality
            )

        # If the city is valid and different to the municipality, add it to the
        # potential destination.
        if formatted_city and formatted_city != formatted_municipality:
            should_be_moved = True
            potential_destination_directory = (
                potential_destination_directory / formatted_city
            )

        # Check if the media file should be moved to non existing destination.
        if (
            potential_destination_directory != media_path.parent
            and should_be_moved
            and location_searching
        ):
            # If not, update the destination.
            destination_directory = potential_destination_directory

            # Finally, create the destination if it does not exist,
            # including any necessary parent directories.
            if not destination_directory.exists():
                destination_directory.mkdir(parents=True, exist_ok=True)

        # Construct the new media path.
        new_media_path: Path = destination_directory / nea_media_file_name

        # Move the media media file to the new path only if it's not there.
        if new_media_path != media_path:
            move_without_overwrite(
                media_path=media_path, new_media_path=new_media_path
            )

        # Finally return the new media path.
        return new_media_path
    except Exception as exception:
        print(f"Error processing {media_path}: {exception}")


def rename_and_organize_media_files(
    directory_path: str,
    location_searching: bool,
    naming_datetime_format: str = None,
    time_zone: str = None,
) -> None:
    """Rename and organize the media files in the specified directory.

    Args:
        directory_path (str):
            The path to the directory containing the media files.
        location_searching (bool):
            If True, the location will be used for organizing the media files.
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

    # Create a set to track processed files.
    processed_files: set = set()

    # TODO: Do not process the same media file twice after moving them.
    # Iterate through all media files in the directory and its subdirectories.
    for media_path in directory.rglob("*"):
        # Check if the media file has one of the media extensions.
        if media_path.suffix.lower() in image_extensions | video_extensions:
            # TODO: Use a database to check for already processed files.
            # Check if this file has already been processed.
            if media_path.resolve() in processed_files:
                continue

            # Get the media type.
            media_type: MediaType = (
                MediaType.IMAGE
                if media_path.suffix.lower() in image_extensions
                else MediaType.VIDEO
            )

            # Print the media file we are processing.
            print(f"Processing {media_path}...")

            # Rename the media file.
            new_media_path: Path = rename_media_files(
                base_directory=directory,
                media_path=media_path,
                media_type=media_type,
                location_searching=location_searching,
                naming_datetime_format=naming_datetime_format,
                time_zone=time_zone,
            )

            # Add this path to the set of processed files.
            processed_files.add(new_media_path.resolve())

    # Delete empty folders recursively.
    delete_empty_directories(directory_path=directory)
