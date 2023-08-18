from exifread.classes import IfdTag
from geopy.exc import GeocoderTimedOut
from geopy.geocoders.nominatim import Nominatim
from geopy.location import Location
from unidecode import unidecode

from enumerations.media_type import MediaType
from helpers.degrees import convert_metadata_location_to_degrees
from helpers.strings import remove_special_characters, remove_words


def extract_metadata_latitude_longitude(
    metadata: dict,
) -> tuple[float | None, float | None]:
    """Extract the latitude and longitude from the media file metadata.

    Args:
        metadata (dict): The media file metadata.

    Returns:
        tuple[float | None, float | None] : The latitude and longitude.
    """

    # Extract the latitude and longitude and their references, if available.
    latitude_reference: IfdTag | None = metadata.get("GPS GPSLatitudeRef", None)
    latitude: IfdTag | None = metadata.get("GPS GPSLatitude", None)
    longitude_reference: IfdTag | None = metadata.get(
        "GPS GPSLongitudeRef", None
    )
    longitude: IfdTag | None = metadata.get("GPS GPSLongitude", None)

    # If latitude and longitude are available, proceed, otherwise return None.
    if latitude and longitude:
        # Convert the latitude to degrees.
        latitude = convert_metadata_location_to_degrees(latitude)

        # Reverse the latitude if the reference is South.
        if latitude_reference.values != "N":
            latitude = -latitude

        # Convert the longitude to degrees.
        longitude = convert_metadata_location_to_degrees(longitude)

        # Reverse the longitude if the reference is West.
        if longitude_reference.values != "E":
            longitude = -longitude

        # Return the latitude and longitude.
        return latitude, longitude
    else:
        return None, None


def convert_metadata_latitude_longitude_to_location(
    latitude: float | None, longitude: float | None, retries: int = 0
) -> tuple[str | None, str | None]:
    """Convert the latitude and longitude to a location.

    Args:
        latitude (float | None): The latitude.
        longitude (float | None): The longitude.
        retries (int, optional): The retried attempts counter. Defaults to 0.

    Returns:
        tuple[str | None, str | None, str | None, str | None]:
            The city, municipality, region and country.
    """

    # Proceed if the latitude and longitude are valid, otherwise return None.
    if latitude is None or longitude is None:
        return None, None, None, None

    # Initialize the geolocator.
    geo_locator: Nominatim = Nominatim(user_agent="geoapiExercises", timeout=10)
    try:
        # Get the location from the coordinates.
        location: Location = geo_locator.reverse(
            (latitude, longitude), language="en"
        )
    except GeocoderTimedOut:
        # Recursive retry up to 3 times.
        if retries < 3:
            return convert_metadata_latitude_longitude_to_location(
                latitude=latitude, longitude=longitude, retries=retries + 1
            )
        else:
            return None, None, None, None

    # Proceed if the location is available, otherwise return None.
    if location:
        # Keep the address metadata.
        address: dict = location.raw["address"]

        # Proceed if the address is available, otherwise return None.
        if address:
            # Keep the approximate country.
            country: str = address.get("country", None)

            # Initialize the region, the municipality and the city.
            region: str | None = None
            municipality: str | None = None
            city: str | None = None

            # Try different fields for city in corresponding order.
            for location_type in ["village", "town", "city"]:
                city = address.get(location_type, None)
                if city:
                    break

            # Try different fields for municipality in corresponding order.
            for location_type in ["suburb", "municipal", "municipality"]:
                municipality = address.get(location_type, None)
                if municipality:
                    break

            # Try different fields for region in corresponding order.
            for location_type in ["state", "state_district", "county"]:
                region = address.get(location_type, None)
                if region:
                    break

            # Finally, return the city, municipality, region and country.
            return city, municipality, region, country

    # Otherwise, return None.
    return None, None, None, None


def format_location(location: str | None) -> str | None:
    """Format the location.

    Args:
        location (str | None): The location.

    Returns:
        str | None: The formatted location.
    """

    # Proceed if it is valid, otherwise return None.
    if location:
        # Trim all leading and trailing whitespaces.
        location = location.strip()

        # Convert to lowercase.
        location = location.lower()

        # Convert all letters to english.
        location = unidecode(location)

        # Remove not needed words.
        location = remove_words(
            location,
            [
                "village",
                "town",
                "city",
                "suburb",
                "municipal",
                "unit",
                "of",
                "municipality",
                "country",
                "state",
                "state_district",
                "region",
                "regional",
                "country",
            ],
        )

        # Replace all whitespaces, dashes and slashes with underscore.
        location = location.replace(" ", "_")
        location = location.replace("-", "_")
        location = location.replace("/", "_")

        # Replace special characters with "".
        location = remove_special_characters(input_string=location, exclude="_")
        # Finally, return the location.
        return location
    else:
        return None


def get_location_taken(
    metadata: dict, media_type: MediaType
) -> tuple[str | None, str | None]:
    """Get the location the picture was taken.
    We will return the location and the country.

    Args:
        metadata (dict): The media file metadata.
        media_type (MediaType): The type of the media file.

    Returns:
        tuple[str | None, str | None, str | None]:
            The city, the municipality, the region and the country
            the picture was taken.
    """

    # Proceed if the media type is image, otherwise return None.
    if media_type is MediaType.IMAGE:
        # Extract the latitude and longitude if available.
        latitude, longitude = extract_metadata_latitude_longitude(
            metadata=metadata
        )

        # Convert the latitude and longitude to a location if available.
        city, municipality, region, country = (
            convert_metadata_latitude_longitude_to_location(
                latitude=latitude, longitude=longitude
            )
        )

        # Finally, return the formatted city, municipality, region and country.
        return (
            format_location(location=city),
            format_location(location=municipality),
            format_location(location=region),
            format_location(location=country),
        )
    else:
        # TODO: Check if there is a valid tool to get video location metadata.
        return None, None
