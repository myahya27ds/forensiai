# ForensiAI

AI-powered digital image forensic analysis platform built with FastAPI, Streamlit, SQLite, and ReportLab.

## Features

* Image Upload
* Metadata Extraction
* Error Level Analysis (ELA)
* Risk Scoring Engine
* Investigation Dashboard
* PDF Investigation Report
* SQLite History Storage

---

## Dashboard

![Dashboard](docs/dashboard.jpeg)

---

## Investigation Report

![PDF Report](docs/report.jpeg)

---

## Tech Stack

* Python
* FastAPI
* Streamlit
* SQLAlchemy
* SQLite
* Pillow
* ReportLab

---

## Installation

```bash
pip install -r requirements.txt
```

Run Backend:

```bash
uvicorn backend.main:app --reload
```

Run Frontend:

```bash
streamlit run frontend/dashboard.py
```

---

## Project Structure

```text
forensiai/
│
├── backend/
├── frontend/
├── uploads/
├── reports/
├── docs/
├── tests/
├── requirements.txt
└── README.md
```

---

## Current Version

v0.6.1

## Author

Muhammad Yahya
