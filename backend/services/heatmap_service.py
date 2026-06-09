import cv2
import numpy as np


def generate_heatmap(
    ela_path,
    output_path
):

    image = cv2.imread(
        ela_path
    )

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    heatmap = cv2.applyColorMap(
        gray,
        cv2.COLORMAP_JET
    )

    cv2.imwrite(
        output_path,
        heatmap
    )

    return output_path