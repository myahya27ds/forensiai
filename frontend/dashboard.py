import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

import json

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="ForensiAI Dashboard",
    layout="wide"
)

st.title("🔍 ForensiAI Dashboard")

# ==================================
# UPLOAD IMAGE
# ==================================

st.subheader("Upload Image")

uploaded_file = st.file_uploader(
    "Choose Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    st.image(
        uploaded_file,
        caption="Preview",
        width=300
    )

    if st.button("Analyze Image"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type
            )
        }

        try:

            response = requests.post(
                f"{API_URL}/upload-image",
                files=files
            )

            response.raise_for_status()

            st.success(
                "Analysis Completed"
            )

            st.json(
                response.json()
            )

            st.rerun()

        except Exception as e:

            st.error(
                f"Upload failed: {e}"
            )

st.divider()

# ==================================
# LOAD STATS
# ==================================

try:

    stats_response = requests.get(
        f"{API_URL}/stats"
    )

    stats_response.raise_for_status()

    stats = stats_response.json()

except Exception as e:

    st.error(
        f"Cannot load stats: {e}"
    )

    stats = {
        "total": 0,
        "low": 0,
        "medium": 0,
        "high": 0,
        "avg_score": 0
    }

# ==================================
# DASHBOARD METRICS
# ==================================

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Analysis",
    stats["total"]
)

col2.metric(
    "Low Risk",
    stats["low"]
)

col3.metric(
    "Medium Risk",
    stats["medium"]
)

col4.metric(
    "High Risk",
    stats["high"]
)

col5.metric(
    "Avg Score",
    round(stats["avg_score"], 2)
)

st.divider()

# ==================================
# EXPORT CSV
# ==================================

st.subheader("Export Data")

st.link_button(
    "⬇ Download CSV",
    f"{API_URL}/export"
)

st.divider()

# ==================================
# LOAD HISTORY
# ==================================

try:

    response = requests.get(
        f"{API_URL}/history"
    )

    response.raise_for_status()

    data = response.json()

    df = pd.DataFrame(data)

except Exception as e:

    st.error(
        f"Cannot load history: {e}"
    )

    df = pd.DataFrame()

# ==================================
# HISTORY TABLE
# ==================================

if not df.empty:

    st.subheader("Analysis History")

    risk_filter = st.selectbox(
        "Filter Risk",
        ["ALL", "LOW", "MEDIUM", "HIGH"]
    )

    filtered_df = df.copy()

    if risk_filter != "ALL":

        filtered_df = filtered_df[
            filtered_df["risk"] == risk_filter
        ]

    columns_to_show = [
        col for col in [

            "id",
            "filename",

            "risk",
            "score",

            "authenticity_score",

            "mean_ela",
            "mean_noise",
            "noise_level",

            "copymove_detected",
            "matched_regions",
            "copymove_score"

        ]
        if col in filtered_df.columns
    ]

    display_df = filtered_df[
        columns_to_show
    ]

    st.dataframe(
        display_df,
        use_container_width=True
    )

    st.divider()

    # ==================================
    # DETAIL INVESTIGATION
    # ==================================

    st.subheader(
        "Investigation Detail"
    )

    selected_file = st.selectbox(
        "Select File",
        filtered_df["filename"]
    )

    selected_row = filtered_df[
        filtered_df["filename"]
        == selected_file
    ].iloc[0]

    # ==================================
    # AI SUMMARY
    # ==================================

    st.subheader(
        "AI Investigation Summary"
    )

    if (
        selected_row.get(
            "explanation"
        )
    ):

        st.info(
            selected_row["explanation"]
        )

    # ==================================
    # FINDINGS
    # ================================== 

    if (
        "findings" in filtered_df.columns
        and selected_row.get("findings")
    ):

        st.subheader(
            "Investigation Findings"
        )

        try:

            findings = json.loads(
                selected_row["findings"]
            )

            for item in findings:

                st.success(item)

        except:

            st.write(
                selected_row["findings"]
            )

    # ==================================
    # PDF REPORT
    # ==================================

    st.link_button(
        "📄 Download PDF Report",
        f"{API_URL}/report/{selected_row['id']}"
    )

    st.divider()

    # ==================================
    # DELETE BUTTON
    # ==================================

    if st.button(
        "🗑 Delete Analysis"
    ):

        try:

            delete_response = requests.delete(
                f"{API_URL}/analysis/{selected_row['id']}"
            )

            delete_response.raise_for_status()

            st.success(
                "Analysis deleted"
            )

            st.rerun()

        except Exception as e:

            st.error(
                f"Delete failed: {e}"
            )

    st.divider()

    # ==================================
    # IMAGE COMPARISON
    # ==================================

    if (
        selected_row.get("image_path")
        and selected_row.get("ela_path")
    ):

        st.subheader(
            "Image Comparison"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.image(
                selected_row["image_path"],
                caption="Original Image",
                use_container_width=True
            )

            if selected_row.get("heatmap_path"):

                st.image(
                    selected_row["heatmap_path"],
                    caption="Forgery Heatmap",
                    use_container_width=True
                )

        with col2:

            st.image(
                selected_row["ela_path"],
                caption="ELA Result",
                use_container_width=True
            )

            if selected_row.get("overlay_path"):

                st.image(
                    selected_row["overlay_path"],
                    caption="Overlay Visualization",
                    use_container_width=True
                )

    if (
        "copymove_path" in selected_row
        and pd.notnull(
            selected_row["copymove_path"]
        )
    ):

        st.image(
            selected_row["copymove_path"],
            caption="Copy-Move Detection",
            use_container_width=True
        )
    
    if (
        "bbox_path" in selected_row
        and pd.notnull(
            selected_row["bbox_path"]
        )
    ):

        st.image(
            selected_row["bbox_path"],
            caption="Clone Localization",
            use_container_width=True
        )

    st.divider()

    # ==================================
    # DETAIL METRICS
    # ==================================

    copymove_flag = str(
        selected_row.get(
            "copymove_detected",
            "False"
        )
    ).lower() == "true"
    
    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Copy-Move",
        "YES" if copymove_flag else "NO"
    )

    c2.metric(
        "Matched Regions",
        selected_row.get(
            "matched_regions",
            0
        )
    )

    c3.metric(
        "Copy-Move Score",
        round(
            selected_row.get(
                "copymove_score",
                0
            ) or 0,
            2
        )
    )

    c4.metric(
        "Noise Level",
        selected_row.get(
            "noise_level",
            "-"
        )
    )

    c5.metric(
        "Clone Regions",
        selected_row.get(
            "bbox_count",
            0
        )
    )

    st.divider()

    # ==================================
    # CHARTS
    # ==================================

    chart1, chart2, chart3 = st.columns(3)

    with chart1:

        st.subheader(
            "Risk Distribution"
        )

        risk_counts = (
            df["risk"]
            .value_counts()
        )

        if len(risk_counts) > 0:

            fig1, ax1 = plt.subplots()

            ax1.pie(
                risk_counts,
                labels=risk_counts.index,
                autopct="%1.1f%%"
            )

            st.pyplot(fig1)

    with chart2:

        st.subheader(
            "Risk Score Distribution"
        )

        if len(df) > 0:

            fig2, ax2 = plt.subplots()

            ax2.hist(
                df["score"],
                bins=10
            )

            ax2.set_xlabel(
                "Risk Score"
            )

            ax2.set_ylabel(
                "Frequency"
            )

            st.pyplot(fig2)

    with chart3:

        if (
            "mean_ela" in df.columns
            and "std_ela" in df.columns
            and len(df) > 0
        ):

            st.subheader(
                "ELA Analysis"
            )

            fig3, ax3 = plt.subplots()

            ax3.scatter(
                df["mean_ela"],
                df["std_ela"],
                alpha=0.7
            )

            ax3.set_xlabel(
                "Mean ELA"
            )

            ax3.set_ylabel(
                "Std ELA"
            )

            ax3.set_title(
                "Mean vs Std ELA"
            )

            st.pyplot(fig3)

    st.divider()

    st.subheader(
        "Noise Analysis"
    )

    n1, n2 = st.columns(2)

    with n1:

        if (
            "mean_noise" in df.columns
            and len(df) > 0
        ):

            fig4, ax4 = plt.subplots()

            ax4.hist(
                df["mean_noise"],
                bins=10
            )

            ax4.set_xlabel(
                "Mean Noise"
            )

            ax4.set_ylabel(
                "Frequency"
            )

            st.pyplot(fig4)

    with n2:

        if (
            "noise_level" in df.columns
            and len(df) > 0
        ):

            counts = (
                df["noise_level"]
                .value_counts()
            )

            fig5, ax5 = plt.subplots()

            ax5.pie(
                counts,
                labels=counts.index,
                autopct="%1.1f%%"
            )

            st.pyplot(fig5)

else:

    st.warning(
        "No analysis data found."
    )