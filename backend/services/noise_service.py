import cv2
import numpy as np


def analyze_noise(image_path):

    image = cv2.imread(image_path)

    if image is None:

        return {

            "mean_noise": 0,

            "std_noise": 0,

            "noise_level": "UNKNOWN"

        }

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    blur = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    noise = cv2.absdiff(
        gray,
        blur
    )

    mean_noise = float(
        np.mean(noise)
    )

    std_noise = float(
        np.std(noise)
    )

    # =====================
    # Noise Classification
    # =====================

    if mean_noise > 15:

        noise_level = "HIGH"

    elif mean_noise > 8:

        noise_level = "MEDIUM"

    else:

        noise_level = "LOW"

    return {

        "mean_noise": round(
            mean_noise,
            2
        ),

        "std_noise": round(
            std_noise,
            2
        ),

        "noise_level": noise_level

    }