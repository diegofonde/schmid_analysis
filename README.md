# 📊 Schmid College Student Resource Optimization

> **Project Overview (Ongoing):** Built an end-to-end data pipeline, predictive clustering model, and interactive dashboard ecosystem to analyze resource utilization trends for 400+ students, directly influencing department budget allocations.

## 🚀 Live Links & Assets
* **Interactive Dashboard:** https://public.tableau.com/app/profile/diego.gabriel.fondevilla/viz/Schmid_Survey/StudentProfile?publish=yes
* **Production API Endpoint:** 
* **User Interface:** https://diegofonde-schmid-analysis-app-owcntx.streamlit.app

---

## 🛠️ Tech Stack & Architecture
* **Data Ingestion & Quality:** Python, SQLite (In development)
* **Statistical Modeling & ML:** R, Partitioning Around Medoids (PAM), Hierarchical Clustering, Gower’s Distance Matrix
* **Deployment & Engineering:** FastAPI, Uvicorn, Render, Streamlit
* **Business Intelligence:** Tableau

---

## 📈 Key Impact & Business Outcomes
* **Identified Operational Bottlenecks:** Discovered that **11 out of 17 major campus resources were underutilized by 50% or more**, exposing a critical disconnect in student outreach[cite: 1].
* **Influenced Resource Allocation:** Presented data-driven behavioral segmentations to the College Dean and advisors, directly guiding department budget restructuring toward high-need student demographics[cite: 1].
* **Created Long-Term Infrastructure:** Migrated unstructured survey data into a structured SQLite relational schema to allow for ongoing, longitudinal service analysis[cite: 1].

---

## 🧬 Machine Learning & Methodology

### 1. Data Processing & Distance Metrics
Because the dataset contained mixed data types (categorical survey responses and numerical engagement metrics), standard Euclidean distance metrics were insufficient. 
* Implemented a **Gower’s Distance Matrix** to mathematically compute dissimilarity across mixed data features.

### 2. Clustering Optimization
* Evaluated both Hierarchical and **Partitioning Around Medoids (PAM)** algorithms.
* Optimized the cluster size at $k = 4$, achieving a **0.65 Silhouette Score**, ensuring distinct, highly interpretable student behavioral profiles.

### 3. Production Pipeline
[Qualtrics Raw Data] ➡️ [SQLite Database] ➡️ [PAM Clustering Model] ➡️ [FastAPI Backend] ➡️ [Streamlit Live UI]

* Wrapped the final trained PAM model in a lightweight **FastAPI** application[cite: 1].
* Deployed the API to **Render** to serve real-time predictions based on new user survey inputs via a custom-built **Streamlit** dashboard.

---

## 📂 Repository Structure
```text
├── data/                  # Excel files containing data used to train the model
├── models/                # .inpynb notebooks used for EDA and model creation
├── pages/                 # Streamlit pages
├── api.py                 # FastAPI application script logic**
├── app.py                 # Streamlit user interface code
├── pam_app_assets.pkl     # Trained PAM clustering model objects (.pkl / .rds)
└── README.md
