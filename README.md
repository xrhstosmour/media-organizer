# Media Organizer

Media Organizer is a tool designed to rename and categorize your media files based on their metadata.

When you initiate the program, you will be prompted to provide:

1. The path to the folder containing the media files you want to organize.
2. The desired datetime naming format for the newly named media files.
3. The specific time zone to apply for datetime conversions.

---

## Handling Image Media Type

If the media file is an image, the following actions will be taken:

* **Renaming**: The image will be renamed to the datetime it was taken, using the EXIF metadata.
  * If the metadata is not available, it will be renamed using the oldest datetime from the creation, modification, or access time.

* **Organization**: The image will be moved to corresponding folders, named after the country and the approximate location, as identified from the GPS EXIF metadata.
  * If this metadata is unavailable, the file will simply be renamed without additional categorization.

---

## Handling Video Media Type

If the media file is a video, it will be handled in the following way:

* **Renaming**: The video will be renamed using the oldest datetime found among the creation, modification, or access time.

Utilize Media Organizer to keep your media files systematically ordered and easily accessible. Enjoy a more streamlined experience in managing your digital assets!

---

## Disclaimer

Please note that while ```Media Organizer``` is designed with care and attention, it is the user's responsibility to ensure proper backups and safeguards are in place before using the tool. We are not responsible for any data loss or corruption that may occur. Use this tool at your own risk, and always ensure you have a secure backup of your files before proceeding.
