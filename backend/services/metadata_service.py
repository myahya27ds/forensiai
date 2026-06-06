from PIL import Image
from PIL.ExifTags import TAGS


def extract_metadata(image_path):
    try:
        image = Image.open(image_path)

        exif_data = image.getexif()

        metadata = {}

        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            metadata[tag] = str(value)

        return metadata

    except Exception as e:
        return {
            "error": str(e)
        }