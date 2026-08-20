# Delivery Performance, Delay Risk, and Logistics Efficiency Analysis

web application-https://supply-chain-analytics-qm9ameskz9ygpsdthqipsx.streamlit.app
---

## 🚀 Project Overview & Objectives
*   **Delivery Performance Overview:** Measures on-time vs. delayed deliveries and tracks average delay scorecards.
*   **Delay Risk Analysis:** Evaluates `late_delivery_risk` distributions and analyzes delay gap histograms.
*   **Shipping Mode Comparison:** Investigates delay patterns and SLA compliance across *First Class*, *Second Class*, *Same Day*, and *Standard Class* shipping modes.
*   **Regional & Market Diagnostics:** Pinpoints geographic bottlenecks across global markets and order regions.

---

## 🛠️ Repository Structure
*   `APL_Logistics (1).csv`: The primary operational dataset containing 180,519 order and shipment records.
*   `eda.py`: Exploratory Data Analysis script for data cleaning, feature engineering (`Delay_Gap`), and baseline KPI generation.
*   `app_complete.py`: A production-ready Streamlit interactive web application with multi-dimensional filters and diagnostic visual scorecards.
*   `app.py`: Core baseline Streamlit application script.

---

## 📊 Key Performance Indicators (KPIs)
1.  **On-Time Delivery Rate (%):** Percentage of orders delivered within scheduled timelines.
2.  **Late Delivery Risk Ratio:** Proportion of shipments flagged with late delivery risk.
3.  **Average Delivery Delay (Days):** Mean difference between actual shipping duration and scheduled duration (`Delay Gap`).
4.  **Shipping Mode Efficiency Index:** Comparative SLA compliance across logistics transport tiers.

---

## ⚙️ Installation & Running the Application

### 1. Install Dependencies
Ensure Python is installed, then run the following command to install required packages:
```bash
pip install streamlit pandas numpy matplotlib seaborn
