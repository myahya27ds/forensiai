def generate_explanation(
    metadata,
    analysis,
    ela_result,
    noise_result
):

    explanation = []

    # =====================
    # Metadata
    # =====================

    if metadata:

        explanation.append(
            "Metadata berhasil ditemukan."
        )

        if "Software" in metadata:

            explanation.append(
                f"Gambar pernah diproses menggunakan software {metadata['Software']}."
            )

    else:

        explanation.append(
            "Metadata tidak ditemukan pada gambar."
        )

    # =====================
    # ELA
    # =====================

    explanation.append(
        f"Nilai ELA rata-rata sebesar {ela_result['mean_error']}."
    )

    explanation.append(
        f"Variasi ELA sebesar {ela_result['std_error']}."
    )

    # =====================
    # Noise
    # =====================

    explanation.append(
        f"Tingkat noise terdeteksi {noise_result['noise_level']}."
    )

    # =====================
    # Risk
    # =====================

    explanation.append(
        f"Tingkat risiko manipulasi dikategorikan {analysis['risk']}."
    )

    explanation.append(
        f"Skor risiko mencapai {analysis['score']} dari 100."
    )

    explanation.append(
        f"Probabilitas manipulasi diperkirakan {analysis['manipulation_probability'] * 100:.0f}%."
    )

    explanation.append(
        f"Skor keaslian diperkirakan {analysis['authenticity_score'] * 100:.0f}%."
    )

    return " ".join(explanation)