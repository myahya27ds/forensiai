import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

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

col1, col2, col3, col4 = st.columns(4)

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
    "Avg Score",
    stats["avg_score"]
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

    st.dataframe(
        filtered_df,
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

    # ==========================
    # PDF REPORT
    # ==========================

    st.link_button(
        "📄 Download PDF Report",
        f"{API_URL}/report/{selected_row['id']}"
    )

    st.divider()

    # ==========================
    # DELETE BUTTON
    # ==========================

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
        "image_path" in selected_row
        and "ela_path" in selected_row
    ):

        st.subheader(
            "Image Comparison"
        )

        col_left, col_right = st.columns(2)

        with col_left:

            st.image(
                selected_row["image_path"],
                caption="Original Image",
                use_container_width=True
            )

        with col_right:

            st.image(
                selected_row["ela_path"],
                caption="ELA Result",
                use_container_width=True
            )

    st.divider()

    # ==================================
    # DETAIL METRICS
    # ==================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Risk Score",
        selected_row["score"]
    )

    c2.metric(
        "Risk Level",
        selected_row["risk"]
    )

    c3.metric(
        "Mean ELA",
        round(
            selected_row["mean_ela"],
            2
        )
    )

    c4.metric(
        "Std ELA",
        round(
            selected_row["std_ela"],
            2
        )
    )

    st.json(
        selected_row.to_dict()
    )

    st.divider()

    # ==================================
    # CHARTS
    # ==================================

    chart1, chart2 = st.columns(2)

    with chart1:

        st.subheader(
            "Risk Distribution"
        )

        risk_counts = (
            df["risk"]
            .value_counts()
        )

        fig1, ax1 = plt.subplots()

        ax1.pie(
            risk_counts,
            labels=risk_counts.index,
            autopct="%1.1f%%"
        )

        st.pyplot(fig1)

    with chart2:

        if (
            "mean_ela" in df.columns
            and "std_ela" in df.columns
        ):

            st.subheader(
                "ELA Analysis"
            )

            fig2, ax2 = plt.subplots()

            ax2.scatter(
                df["mean_ela"],
                df["std_ela"],
                alpha=0.7
            )

            ax2.set_xlabel(
                "Mean ELA"
            )

            ax2.set_ylabel(
                "Std ELA"
            )

            ax2.set_title(
                "Mean vs Std ELA"
            )

            st.pyplot(fig2)

else:

    st.warning(
        "No analysis data found."
    )