import re


def remove_special_characters(
    input_string: str, exclude: str = ""
) -> str | None:
    """Remove special characters from the given string.

    Args:
        input_string (str): The string to remove special characters from.
        exclude (str):
            A string containing characters that should be excluded from removal.
            Defaults to "".

    Returns:
        str | None: The string without special characters.
    """

    # Proceed if the input string is not empty, otherwise return None.
    if input_string:
        # Add the characters to exclude to the regex pattern.
        pattern: str = f"[^a-zA-Z0-9\s{exclude}]"

        # Return the modified string.
        return re.sub(pattern, "", input_string)
    else:
        return None
