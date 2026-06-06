import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

st.title("ForensiAI Dashboard")

df = pd.DataFrame()

try:

    response = requests.get(
        "http://127.0.0.1:8000/history"
    )

    response.raise_for_status()

    data = response.json()

    df = pd.DataFrame(data)

    st.success("Backend Connected")

except Exception as e:

    st.error("Backend FastAPI belum berjalan")

    st.code(str(e))

if not df.empty:

    col1, col2, col3, col4 = st.columns(4)

    total = len(df)
    low = len(df[df["risk"] == "LOW"])
    medium = len(df[df["risk"] == "MEDIUM"])
    high = len(df[df["risk"] == "HIGH"])

    col1.metric("Total", total)
    col2.metric("Low", low)
    col3.metric("Medium", medium)
    col4.metric("High", high)

    st.subheader("Analysis History")

    st.dataframe(df)

    if "risk" in df.columns:

        risk_counts = df["risk"].value_counts()

        fig, ax = plt.subplots()

        ax.pie(
            risk_counts,
            labels=risk_counts.index,
            autopct="%1.1f%%"
        )

        ax.set_title("Risk Distribution")

        st.pyplot(fig)
    
    if not df.empty and "mean_ela" in df.columns and "std_ela" in df.columns:

        st.subheader("ELA Analysis")

        fig, ax = plt.subplots()

        ax.scatter(df["mean_ela"], df["std_ela"], c="blue", alpha=0.5)

        ax.set_xlabel("Mean ELA")
        ax.set_ylabel("Std ELA")
        ax.set_title("Mean vs Std of ELA")

        st.pyplot(fig)
        