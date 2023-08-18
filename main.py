from pathlib import Path

import pytz

from helpers.strings import to_boolean
from utilities.organize import rename_and_organize_media_files


def main() -> None:
    print("Welcome to the Media File Organizer!")
    directory_path: str = input(
        "Please enter the path to the directory containing your media files: "
    ).strip()
    time_zone: str = (
        input(
            "Please enter your time zone (e.g., Europe/Athens) or leave empty"
            " for local time zone: "
        ).strip()
        or None
    )
    naming_datetime_format: str = (
        input(
            "Please enter the desired naming datetime format (e.g., %Y-%m-%d"
            " %H:%M:%S) or leave empty for default (%d_%m_%YT%H_%M_%S): "
        ).strip()
        or None
    )

    # Default to "n" if nothing is entered.
    location_searching: str = (
        input("Would you like to enable location searching? (y/N): ").strip()
        or "N"
    )

    # Check if time zone is valid.
    if time_zone and time_zone not in pytz.all_timezones:
        print("Invalid time zone entered!")
        print("Exiting...")
        return

    # Check if directory exists.
    if not Path(directory_path).is_dir():
        print("Invalid directory path entered!")
        print("Exiting...")
        return

    if location_searching.lower() not in ["y", "n"]:
        print("Invalid input for location searching!")
        print("Please enter 'y' or 'n'.")
        print("Exiting...")
        return

    # Start processing the files
    rename_and_organize_media_files(
        directory_path=directory_path,
        location_searching=to_boolean(location_searching),
        naming_datetime_format=naming_datetime_format,
        time_zone=time_zone,
    )
    print("Processing complete!")


if __name__ == "__main__":
    main()
