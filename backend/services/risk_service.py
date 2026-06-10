def calculate_risk(
    metadata,
    ela_result,
    noise_result
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
        and metadata.get("Software")
        and metadata["Software"] != "Unknown"
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
    # ELA Variance
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
    # Noise Analysis
    # =====================

    mean_noise = noise_result["mean_noise"]

    if mean_noise > 20:

        score += 15

        findings.append(
            "Abnormal image noise detected"
        )

    elif mean_noise > 10:

        score += 5

    if noise_result["noise_level"] == "HIGH":

        score += 20

        findings.append(
            "Abnormal noise pattern detected"
        )

    elif noise_result["noise_level"] == "MEDIUM":

        score += 10

    # =====================
    # Prevent Overflow
    # =====================

    score = min(score, 100)

    # =====================
    # Risk Level
    # =====================

    if score >= 70:

        risk = "HIGH"

    elif score >= 35:

        risk = "MEDIUM"

    else:

        risk = "LOW"

    # =====================
    # Probability
    # =====================

    manipulation_probability = round(
        score / 100,
        2
    )

    authenticity_score = round(
        1 - manipulation_probability,
        2
    )

    return {

        "score": score,

        "risk": risk,

        "confidence": round(
            max(
                manipulation_probability,
                authenticity_score
            ),
            2
        ),

        "manipulation_probability":
            manipulation_probability,

        "authenticity_score":
            authenticity_score,

        "findings": findings
    }