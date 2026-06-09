import cv2
from matplotlib import image
from streamlit import image 


def generate_overlay(
    original_path,
    heatmap_path,
    output_path
):

    original = cv2.imread(
        original_path
    )

    heatmap = cv2.imread(
        heatmap_path
    )

    heatmap = cv2.resize(
        heatmap,
        (
            original.shape[1], 
            original.shape[0]
        )
    )

    overlay = cv2.addWeighted(
        original,
        0.7,
        heatmap,
        0.3,
        0
    )

    cv2.imwrite(
        output_path,
        overlay
    )

    return output_path