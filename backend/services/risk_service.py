def calculate_risk(
    metadata,
    ela_result
):

    score = 0

    findings = []

    # =====================
    # Metadata
    # =====================

    if not metadata:

        score += 30

        findings.append(
            "Metadata not found"
        )

    if (
        metadata
        and "Software" in metadata
    ):

        score += 25

        findings.append(
            f"Editing software detected: {metadata['Software']}"
        )

    # =====================
    # ELA Mean
    # =====================

    mean_ela = ela_result["mean_error"]

    if mean_ela > 25:

        score += 20

        findings.append(
            "High ELA mean detected"
        )

    elif mean_ela > 10:

        score += 10

    # =====================
    # ELA Std
    # =====================

    std_ela = ela_result["std_error"]

    if std_ela > 40:

        score += 25

        findings.append(
            "High ELA variance detected"
        )

    elif std_ela > 20:

        score += 10

    # =====================
    # Risk Level
    # =====================

    if score >= 70:

        risk = "HIGH"

    elif score >= 35:

        risk = "MEDIUM"

    else:

        risk = "LOW"

    confidence = round(
        min(score / 100, 0.99),
        2
    )

    return {

        "score": score,

        "risk": risk,

        "confidence": confidence,

        "findings": findings
    }