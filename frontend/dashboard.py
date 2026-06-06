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

# ===================================
# Upload Section
# ===================================

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

            st.success("Analysis Completed")

            st.json(response.json())

            st.rerun()

        except Exception as e:

            st.error(f"Upload failed: {e}")

# ===================================
# Load History
# ===================================

try:

    response = requests.get(
        f"{API_URL}/history"
    )

    response.raise_for_status()

    data = response.json()

    df = pd.DataFrame(data)

except Exception as e:

    st.error(f"Cannot load history: {e}")

    df = pd.DataFrame()

# ===================================
# Dashboard
# ===================================

if not df.empty:

    total = len(df)

    low = len(df[df["risk"] == "LOW"])
    medium = len(df[df["risk"] == "MEDIUM"])
    high = len(df[df["risk"] == "HIGH"])

    avg_score = round(df["score"].mean(), 2)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Analysis", total)
    col2.metric("Low Risk", low)
    col3.metric("Medium Risk", medium)
    col4.metric("Avg Score", avg_score)

    st.divider()

    # ===================================
    # Filter
    # ===================================

    st.subheader("Filter")

    risk_filter = st.selectbox(
        "Risk Level",
        ["ALL", "LOW", "MEDIUM", "HIGH"]
    )

    filtered_df = df.copy()

    if risk_filter != "ALL":

        filtered_df = filtered_df[
            filtered_df["risk"] == risk_filter
        ]

    # ===================================
    # History Table
    # ===================================

    st.subheader("Analysis History")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    # ===================================
    # Investigation Detail
    # ===================================

    st.subheader("Investigation Detail")

    selected_file = st.selectbox(
        "Select File",
        filtered_df["filename"]
    )

    selected_row = filtered_df[
        filtered_df["filename"] == selected_file
    ].iloc[0]

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
        round(selected_row["mean_ela"], 2)
    )

    c4.metric(
        "Std ELA",
        round(selected_row["std_ela"], 2)
    )

    st.json(
        selected_row.to_dict()
    )

    st.divider()

    # ===================================
    # Charts
    # ===================================

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:

        st.subheader("Risk Distribution")

        risk_counts = df["risk"].value_counts()

        fig1, ax1 = plt.subplots()

        ax1.pie(
            risk_counts,
            labels=risk_counts.index,
            autopct="%1.1f%%"
        )

        st.pyplot(fig1)

    with col_chart2:

        if (
            "mean_ela" in df.columns
            and "std_ela" in df.columns
        ):

            st.subheader("ELA Analysis")

            fig2, ax2 = plt.subplots()

            ax2.scatter(
                df["mean_ela"],
                df["std_ela"],
                alpha=0.7
            )

            ax2.set_xlabel("Mean ELA")

            ax2.set_ylabel("Std ELA")

            ax2.set_title(
                "Mean vs Std ELA"
            )

            st.pyplot(fig2)

else:

    st.warning(
        "No analysis data found."
    )