import re


def remove_special_characters(input_string: str) -> str | None:
    """Remove special characters from a string.

    Args:
        input_string (str): The string to remove special characters from.

    Returns:
        str | None: The string without special characters.
    """

    # Proceed if the input string is not empty, otherwise return None.
    if input_string:
        return re.sub(r"[^a-zA-Z0-9\s]", "", input_string)
    else:
        return None
