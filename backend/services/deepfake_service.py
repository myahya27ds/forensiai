import cv2
import numpy as np
import os


def detect_copymove(
    image_path,
    output_path
):

    image = cv2.imread(image_path)

    if image is None:

        return {

            "copymove_detected": False,
            "matched_regions": 0,
            "copymove_score": 0,
            "copymove_path": None

        }

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # =====================
    # ORB Feature Detection
    # =====================

    orb = cv2.ORB_create(
        nfeatures=2000
    )

    keypoints, descriptors = orb.detectAndCompute(
        gray,
        None
    )

    if descriptors is None:

        return {

            "copymove_detected": False,
            "matched_regions": 0,
            "copymove_score": 0,
            "copymove_path": None

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

    suspicious_matches = []

    for match in matches:

        if match.queryIdx == match.trainIdx:
            continue

        pt1 = keypoints[
            match.queryIdx
        ].pt

        pt2 = keypoints[
            match.trainIdx
        ].pt

        distance = np.linalg.norm(
            np.array(pt1)
            - np.array(pt2)
        )

        if distance > 20:

            suspicious_matches.append(
                match
            )

    matched_regions = len(
        suspicious_matches
    )

    # =====================
    # Score Calculation
    # =====================

    copymove_score = min(
        matched_regions / 50,
        1.0
    )

    copymove_detected = (
        matched_regions > 10
    )

    # =====================
    # Visualization
    # =====================

    result = cv2.drawMatches(

        image,
        keypoints,

        image,
        keypoints,

        suspicious_matches[:50],

        None,

        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS

    )

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    cv2.imwrite(
        output_path,
        result
    )

    return {

        "copymove_detected":
            copymove_detected,

        "matched_regions":
            matched_regions,

        "copymove_score":
            round(
                copymove_score,
                2
            ),

        "copymove_path":
            output_path

    }