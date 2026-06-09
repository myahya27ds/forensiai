from PIL import Image
from PIL import ImageOps


def normalize_orientation(image_path):

    image = Image.open(image_path)

    image = ImageOps.exif_transpose(
        image
    )

    image.save(image_path)

    return image_path