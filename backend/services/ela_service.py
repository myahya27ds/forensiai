from PIL import Image, ImageChops, ImageEnhance
import numpy as np

def generate_ela(image_path, output_path, quality=90):

    original = Image.open(image_path)

    temp_path = "temp_ela.jpg"

    original.save(
        temp_path,
        "JPEG",
        quality=quality
    )

    compressed = Image.open(temp_path)

    ela_image = ImageChops.difference(
        original,
        compressed
    )

    extrema = ela_image.getextrema()

    max_diff = max(
        ex[1]
        for ex in extrema
    )

    if max_diff == 0:
        max_diff = 1

    scale = 255.0 / max_diff

    ela_image = ImageEnhance.Brightness(
        ela_image
    ).enhance(scale)

    ela_image.save(output_path)

    # Hitung statistik error
    ela_array = np.array(ela_image)

    mean_error = float(np.mean(ela_array))
    max_error = float(np.max(ela_array))
    std_error = float(np.std(ela_array))

    return {
        "ela_path": output_path,
        "mean_error": round(mean_error, 2),
        "max_error": round(max_error, 2),
        "std_error": round(std_error, 2),
        "image_path": image_path
    }