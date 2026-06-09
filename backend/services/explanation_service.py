def generate_explanation(
    metadata,
    ela_result,
    analysis
):

    explanations = []

    if not metadata:

        explanations.append(
            "Metadata unavailable."
        )

    if metadata.get("Software"):

        explanations.append(
            f"Software detected: {metadata['Software']}"
        )

    if ela_result["mean_error"] > 25:

        explanations.append(
            "High ELA anomaly detected."
        )

    elif ela_result["mean_error"] > 10:

        explanations.append(
            "Moderate ELA anomaly detected."
        )

    if ela_result["std_error"] > 40:

        explanations.append(
            "High variance anomaly detected."
        )

    risk = analysis["risk"]

    if risk == "HIGH":

        conclusion = (
            "Image shows strong indicators "
            "of manipulation."
        )

    elif risk == "MEDIUM":

        conclusion = (
            "Image may contain edited regions."
        )

    else:

        conclusion = (
            "Image appears authentic."
        )

    return {

        "explanations": explanations,

        "conclusion": conclusion
    }