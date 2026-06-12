import cv2
import numpy as np
import os


def localize_clones(
    image_path,
    output_path
):

    image = cv2.imread(
        image_path
    )

    if image is None:

        return {

            "bbox_count": 0,

            "bbox_path": None

        }

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # =====================
    # ORB Features
    # =====================

    orb = cv2.ORB_create(
        nfeatures=2000
    )

    keypoints, descriptors = (
        orb.detectAndCompute(
            gray,
            None
        )
    )

    if descriptors is None:

        return {

            "bbox_count": 0,

            "bbox_path": None

        }

    # =====================
    # Feature Matching
    # =====================

    matcher = cv2.BFMatcher(
        cv2.NORM_HAMMING,
        crossCheck=True
    )

    matches = matcher.match(
        descriptors,
        descriptors
    )

    suspicious_points = []

    for match in matches:

        if (
            match.queryIdx
            ==
            match.trainIdx
        ):
            continue

        pt1 = keypoints[
            match.queryIdx
        ].pt

        pt2 = keypoints[
            match.trainIdx
        ].pt

        distance = np.linalg.norm(
            np.array(pt1)
            -
            np.array(pt2)
        )

        if distance > 20:

            suspicious_points.append(
                (
                    int(pt1[0]),
                    int(pt1[1])
                )
            )

            suspicious_points.append(
                (
                    int(pt2[0]),
                    int(pt2[1])
                )
            )

    # =====================
    # No Clone Found
    # =====================

    if len(
        suspicious_points
    ) < 10:

        return {

            "bbox_count": 0,

            "bbox_path": None

        }

    # =====================
    # Bounding Box
    # =====================

    points = np.array(
        suspicious_points
    )

    x, y, w, h = cv2.boundingRect(
        points
    )

    result = image.copy()

    cv2.rectangle(

        result,

        (x, y),

        (x + w, y + h),

        (0, 0, 255),

        3

    )

    cv2.putText(

        result,

        "Suspected Clone Region",

        (x, max(30, y - 10)),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.8,

        (0, 0, 255),

        2

    )

    os.makedirs(
        os.path.dirname(
            output_path
        ),
        exist_ok=True
    )

    cv2.imwrite(
        output_path,
        result
    )

    return {

        "bbox_count": 1,

        "bbox_path": output_path

    }