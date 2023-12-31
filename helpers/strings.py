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


def remove_words(input_string: str, words_to_remove: list) -> str:
    """Removes the specified words from the given string.

    Args:
        input_string (str): The string from which words are to be removed.
        words_to_remove (str): A list of the words to remove from the string.

    Returns:
        str: The modified string with the specified words removed.
    """
    return " ".join(
        [word for word in input_string.split() if word not in words_to_remove]
    ).strip()


def to_boolean(input_value: str | int | bool) -> bool:
    """Convert string or integer to boolean.

    Args:
        input_value (str | int | bool): The input string to convert to boolean.
    Returns:
        bool: True or False.
    """
    if input_value is not None:
        if isinstance(input_value, bool):
            return input_value
        elif str(input_value).lower() in ("true", "1", "t", "y", "yes"):
            return True
        elif str(input_value).lower() in ("false", "0", "f", "n", "no"):
            return False
        else:
            return False
    else:
        return False
