def calculate_risk(metadata):

    score = 100
    findings = []

    # Metadata hilang
    if not metadata:
        score -= 30
        findings.append("Metadata tidak ditemukan")

    # Software editor terdeteksi
    if "Software" in metadata:
        score -= 25
        findings.append(
            f"Editing software terdeteksi: {metadata['Software']}"
        )

    # Tentukan level risiko
    if score >= 80:
        risk = "LOW"
    elif score >= 50:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return {
        "score": score,
        "risk": risk,
        "findings": findings
    }