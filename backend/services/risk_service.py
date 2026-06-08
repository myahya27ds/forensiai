def calculate_risk(
    metadata,
    ela_result
):

    score = 0

    findings = []

    # ======================
    # Metadata
    # ======================

    if not metadata:

        score += 30

        findings.append(
            "Metadata tidak ditemukan"
        )

    else:

        score += 5

    # ======================
    # Software Detection
    # ======================

    if (
        metadata
        and "Software" in metadata
    ):

        score += 25

        findings.append(
            f"Software terdeteksi: {metadata['Software']}"
        )

    # ======================
    # ELA Mean
    # ======================

    mean_ela = ela_result[
        "mean_error"
    ]

    if mean_ela > 20:

        score += 25

        findings.append(
            "ELA Mean sangat tinggi"
        )

    elif mean_ela > 10:

        score += 15

        findings.append(
            "ELA Mean sedang"
        )

    # ======================
    # ELA Std
    # ======================

    std_ela = ela_result[
        "std_error"
    ]

    if std_ela > 20:

        score += 20

        findings.append(
            "Variasi ELA tinggi"
        )

    elif std_ela > 10:

        score += 10

        findings.append(
            "Variasi ELA sedang"
        )

    # ======================
    # Risk Level
    # ======================

    if score >= 70:

        risk = "HIGH"

    elif score >= 40:

        risk = "MEDIUM"

    else:

        risk = "LOW"

    return {

        "score": score,

        "risk": risk,

        "findings": findings
    }