from exifread.classes import IfdTag
from exifread.utils import Ratio


def convert_metadata_location_to_degrees(metadata_location: IfdTag) -> float:
    """Convert the metadata GPS coordinates to degrees.

    Args:
        metadata_location (IfdTag): The metadata location, either latitude or longitude.

    Returns:
        float: The decimal degrees.
    """

    # Get the degrees, minutes, and seconds from the metadata.
    degrees_ratio: Ratio = metadata_location.values[0]
    minutes_ratio: Ratio = metadata_location.values[1]
    seconds_ratio: Ratio = metadata_location.values[2]

    # Get the degrees', minutes', and seconds' numerator and denominator.
    degrees_numerator: float = float(degrees_ratio.num)
    degrees_denominator: float = float(degrees_ratio.den)
    minutes_numerator: float = float(minutes_ratio.num)
    minutes_denominator: float = float(minutes_ratio.den)
    seconds_numerator: float = float(seconds_ratio.num)
    seconds_denominator: float = float(seconds_ratio.den)

    # Calculate the decimal degrees.
    degrees: float = degrees_numerator / degrees_denominator

    # Calculate the decimal minutes.
    minutes: float = minutes_numerator / minutes_denominator

    # Calculate the decimal seconds.
    seconds: float = seconds_numerator / seconds_denominator

    # Return the calculated decimal degrees.
    return degrees + (minutes / 60.0) + (seconds / 3600.0)
