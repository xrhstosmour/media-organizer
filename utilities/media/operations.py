import shutil
from pathlib import Path


def move_without_overwrite(media_path: Path, new_media_path: Path) -> None:
    """Moves a file from one location to another, without overwriting
    possible existing file at the destination.
    If a file with the same name exists at the destination,
    the letter C from copy and a number is appended to the filename.

    Args:
        media_path (Path): Path to the source file that needs to be moved.
        new_media_path (Path):
            Path to the destination where the file should be moved.
    """

    # Check if the file exists at the target location.
    counter = 1
    while new_media_path.exists():
        # Append a number to the end of the filename and increase the counter.
        new_media_path = new_media_path.with_name(
            new_media_path.stem + f"C{counter}" + new_media_path.suffix.lower()
        )
        counter += 1

    # Move the file to the new (and possibly modified) path.
    shutil.move(str(media_path), new_media_path)


def delete_empty_directories(directory_path: Path) -> None:
    """Deletes empty directories recursively.

    Args:
        directory_path (Path): The directory path.
    """

    # Flag to indicate if a directory was deleted.
    deleted = True

    # Repeat until no more empty directories are found.
    while deleted:
        deleted = False
        # Iterate through subdirectories, from the deepest to the shallowest.
        for path in reversed(list(directory_path.rglob("*"))):
            if path.is_dir() and not any(path.iterdir()):
                print(f"Deleting empty directory {path}...")
                path.rmdir()
                deleted = True
