# Cluster-Lieferante-04.06
📊 Data-Driven Kraljic Matrix Optimization Dashboard
An interactive Web Application built with Streamlit, Scikit-Learn (K-Means Clustering), and Plotly to transform raw supplier dataset scores into an objective, dynamic, and presentation-ready Kraljic Portfolio Matrix.

🚀 Live Demo
🔗 [Insert your Streamlit live link here after deployment]

🎯 Project Overview
Traditional procurement management relies heavily on subjective evaluations to segment suppliers. This project solves that bias by utilizing Machine Learning (K-Means) to establish a highly stable, data-driven yearly baseline for supplier categories, while allowing real-time parameter weighting and chronological dynamic filtering (Months/Quarters).

🧩 Core Matrix Dimensions:
X-Axis (Strategic Importance): Normalized Supplier Spend (0 to 100) based on total order values.
Y-Axis (Supply Risk / Vulnerability): A dynamic composite risk score (0 to 100) combining 5 critical indices: Quality Performance, Financial Risk, Sustainability (ESG), Standards & Compliance, and Political Risk.
🔴 Visual Portfolio Segmentation (Kraljic Quadrants)
Suppliers are objectively segmented into 4 stable clusters designed specifically for executive presentations with explicit high-impact color schemes:

🔴 Strategic suppliers (High Spend / High Risk): Focus on long-term partnership development and integration.
🔵 Leverage suppliers (High Spend / Low Risk): Capitalize on buying power, competitive bidding, and cost reduction.
🟡 Bottleneck suppliers (Low Spend / High Risk): Mitigate supply volume risks, look for substitution, and build backup networks.
🟢 Non-Critical suppliers (Low Spend / Low Risk): Standardize and automate logistics pipelines to minimize administrative overhead.
🛠️ Repository Architecture
├── Merged dataset with Scores.csv   # Target dataset with processed scoring elements
├── app.py                           # Main Streamlit application codebase 
├── requirements.txt                 # Python environmental dependencies
└── README.md                        # Project documentation (This file)