import cv2
import numpy as np
import os

from sklearn.cluster import DBSCAN


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

            "copymove_path": None,

            "bbox_count": 0,

            "bbox_path": None,

            "debug_matches": 0

        }

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # ==================================
    # SIFT
    # ==================================

    sift = cv2.SIFT_create(
        nfeatures=3000
    )

    keypoints, descriptors = sift.detectAndCompute(
        gray,
        None
    )

    print(
        "KEYPOINTS:",
        len(keypoints)
    )

    if (
        descriptors is None
        or len(keypoints) < 10
    ):

        return {

            "copymove_detected": False,

            "matched_regions": 0,

            "copymove_score": 0,

            "copymove_path": None,

            "bbox_count": 0,

            "bbox_path": None,

            "debug_matches": 0

        }

    # ==================================
    # FLANN
    # ==================================

    FLANN_INDEX_KDTREE = 1

    index_params = {

        "algorithm": FLANN_INDEX_KDTREE,

        "trees": 5

    }

    search_params = {

        "checks": 100

    }

    flann = cv2.FlannBasedMatcher(
        index_params,
        search_params
    )

    matches = flann.knnMatch(
        descriptors,
        descriptors,
        k=10
    )

    good_matches = []

    points = []

    # ==================================
    # Copy-Move Matching
    # ==================================

    for pair in matches:

        for m in pair:

            if m.queryIdx == m.trainIdx:
                continue

            pt1 = np.array(
                keypoints[m.queryIdx].pt
            )

            pt2 = np.array(
                keypoints[m.trainIdx].pt
            )

            spatial_distance = np.linalg.norm(
                pt1 - pt2
            )

            # abaikan fitur yg terlalu dekat
            if spatial_distance < 30:
                continue

            # descriptor similarity
            if m.distance < 250:

                good_matches.append(m)

                points.append(pt1)

                points.append(pt2)

    matched_regions = len(
        good_matches
    )

    print(
        "GOOD MATCHES:",
        matched_regions
    )

    # ==================================
    # Debug Visualization
    # ==================================

    debug_path = output_path.replace(
        ".jpg",
        "_matches.jpg"
    )

    if matched_regions > 0:

        debug_image = cv2.drawMatches(

            image,
            keypoints,

            image,
            keypoints,

            good_matches[:100],

            None,

            flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS

        )

        cv2.imwrite(
            debug_path,
            debug_image
        )

    # ==================================
    # Early Exit
    # ==================================

    if len(points) < 6:

        return {

            "copymove_detected": False,

            "matched_regions": matched_regions,

            "copymove_score": 0,

            "copymove_path": debug_path,

            "bbox_count": 0,

            "bbox_path": None,

            "debug_matches": matched_regions

        }

    # ==================================
    # DBSCAN
    # ==================================

    points = np.array(points)

    print(
        "POINTS:",
        len(points)
    )

    clustering = DBSCAN(
        eps=60,
        min_samples=2
    ).fit(points)

    labels = clustering.labels_

    result = image.copy()

    cluster_count = 0

    # ==================================
    # Bounding Boxes
    # ==================================

    for label in set(labels):

        if label == -1:
            continue

        cluster_points = points[
            labels == label
        ]

        if len(cluster_points) < 3:
            continue

        cluster_count += 1

        x_min = int(
            cluster_points[:, 0].min()
        )

        y_min = int(
            cluster_points[:, 1].min()
        )

        x_max = int(
            cluster_points[:, 0].max()
        )

        y_max = int(
            cluster_points[:, 1].max()
        )

        cv2.rectangle(

            result,

            (x_min, y_min),

            (x_max, y_max),

            (0, 0, 255),

            3

        )

    print(
        "CLUSTERS:",
        cluster_count
    )

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    cv2.imwrite(
        output_path,
        result
    )

    copymove_detected = (
        cluster_count > 0
    )

    copymove_score = min(

        (
            matched_regions / 100
        )
        +
        (
            cluster_count / 10
        ),

        1.0

    )

    print(
        "COPYMOVE:",
        copymove_detected
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

        "bbox_count":
            cluster_count,

        "bbox_path":
            output_path,

        "copymove_path":
            output_path,

        "debug_matches":
            matched_regions

    }