import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

# Set page config
st.set_page_config(
    page_title="APL Logistics Supply Chain Analytics Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown(
    """
    <style>
    .main { background-color: #f4f6f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    </style>
""",
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
  df = pd.read_csv("APL_Logistics (2).csv", encoding="latin1")
  df["Delay_Gap"] = (
      df["Days for shipping (real)"] - df["Days for shipment (scheduled)"]
  )
  return df


with st.spinner("Loading APL Logistics supply chain dataset..."):
  df = load_data()

# Sidebar Filters
st.sidebar.title("🎛️ Control Panel")
st.sidebar.markdown("---")

selected_market = st.sidebar.multiselect(
    "Select Market(s)",
    options=df["Market"].unique(),
    default=df["Market"].unique(),
)

selected_region = st.sidebar.multiselect(
    "Select Order Region(s)",
    options=df["Order Region"].unique(),
    default=df["Order Region"].unique(),
)

selected_mode = st.sidebar.multiselect(
    "Select Shipping Mode(s)",
    options=df["Shipping Mode"].unique(),
    default=df["Shipping Mode"].unique(),
)

selected_segment = st.sidebar.multiselect(
    "Select Customer Segment(s)",
    options=df["Customer Segment"].unique(),
    default=df["Customer Segment"].unique(),
)

# Filter dataframe
filtered_df = df[
    (df["Market"].isin(selected_market))
    & (df["Order Region"].isin(selected_region))
    & (df["Shipping Mode"].isin(selected_mode))
    & (df["Customer Segment"].isin(selected_segment))
]

# Dashboard Header
st.title("📦 APL Logistics: Supply Chain Intelligence & Risk Dashboard")
st.markdown(
    "### Operational Monitoring, SLA Compliance, and Delay Risk Diagnostics"
)
st.markdown("---")

if filtered_df.empty:
  st.warning(
      "⚠️ No data available for the selected filters. Please adjust your"
      " criteria."
  )
else:
  # --- MODULE 1: DELIVERY PERFORMANCE OVERVIEW ---
  st.header("📊 1. Delivery Performance Overview")

  total_orders = len(filtered_df)
  on_time_rate = (
      filtered_df["Delivery Status"].isin(
          ["Shipping on time", "Advance shipping"]
      )
  ).mean() * 100
  late_risk_ratio = (filtered_df["Late_delivery_risk"] == 1).mean() * 100
  avg_delay = filtered_df["Delay_Gap"].mean()

  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric("Total Filtered Orders", f"{total_orders:,}")
  with col2:
    st.metric("On-Time Delivery Rate", f"{on_time_rate:.2f}%")
  with col3:
    st.metric("Late Delivery Risk Ratio", f"{late_risk_ratio:.2f}%")
  with col4:
    st.metric("Avg Delivery Delay (Days)", f"{avg_delay:.2f} Days")

  st.markdown("---")

  # --- MODULE 2: DELAY RISK ANALYSIS DASHBOARD ---
  st.header("📉 2. Delay Risk Analysis Dashboard")

  r_col1, r_col2 = st.columns(2)

  with r_col1:
    st.subheader("Late Delivery Risk Distribution")
    risk_counts = (
        filtered_df["Late_delivery_risk"].value_counts().reset_index()
    )
    risk_counts.columns = ["Risk_Status", "Count"]
    risk_counts["Risk_Status"] = risk_counts["Risk_Status"].map(
        {1: "Late Risk (1)", 0: "No Risk (0)"}
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(
        data=risk_counts,
        x="Risk_Status",
        y="Count",
        hue="Risk_Status",
        legend=False,
        palette=["#e74c3c", "#2ecc71"],
        ax=ax,
    )
    ax.set_ylabel("Order Count")
    ax.set_xlabel("Late Delivery Risk Indicator")
    st.pyplot(fig)

  with r_col2:
    st.subheader("Delay Gap Histogram (Real vs Scheduled)")
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.histplot(
        filtered_df["Delay_Gap"], bins=25, kde=True, color="#3498db", ax=ax
    )
    ax.set_xlabel("Delay Gap (Days)")
    ax.set_ylabel("Order Frequency")
    st.pyplot(fig)

  st.markdown("---")

  # --- MODULE 3: SHIPPING MODE COMPARISON ---
  st.header("🚢 3. Shipping Mode Efficiency & SLA Compliance")

  m_col1, m_col2 = st.columns(2)

  mode_summary = (
      filtered_df.groupby("Shipping Mode")
      .agg(
          Total_Orders=("Late_delivery_risk", "count"),
          Late_Risk_Ratio=(
              "Late_delivery_risk",
              lambda x: (x == 1).mean() * 100,
          ),
          Avg_Delay=("Delay_Gap", "mean"),
      )
      .reset_index()
  )

  with m_col1:
    st.subheader("Late Risk Ratio by Mode (%)")
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(
        data=mode_summary,
        x="Shipping Mode",
        y="Late_Risk_Ratio",
        hue="Shipping Mode",
        legend=False,
        palette="Blues_r",
        ax=ax,
    )
    ax.set_ylabel("Late Delivery Risk (%)")
    ax.set_ylim(0, 100)
    st.pyplot(fig)

  with m_col2:
    st.subheader("Shipping Mode Performance Table")
    display_mode_df = mode_summary.copy()
    display_mode_df["Late_Risk_Ratio"] = (
        display_mode_df["Late_Risk_Ratio"].round(2).astype(str) + "%"
    )
    display_mode_df["Avg_Delay"] = (
        display_mode_df["Avg_Delay"].round(2).astype(str) + " Days"
    )
    st.dataframe(display_mode_df, use_container_width=True)

  st.markdown("---")

  # --- MODULE 4: REGIONAL & MARKET HEATMAPS ---
  st.header("🌍 4. Regional & Market Logistics Efficiency")

  reg_summary = (
      filtered_df.groupby(["Market", "Order Region"])
      .agg(
          Total_Orders=("Late_delivery_risk", "count"),
          Late_Risk_Ratio=(
              "Late_delivery_risk",
              lambda x: (x == 1).mean() * 100,
          ),
          Avg_Delay=("Delay_Gap", "mean"),
      )
      .reset_index()
      .sort_values(by="Late_Risk_Ratio", ascending=False)
  )

  st.subheader("Top High-Risk Regions & Markets")
  display_reg_df = reg_summary.head(10).copy()
  display_reg_df["Late_Risk_Ratio"] = (
      display_reg_df["Late_Risk_Ratio"].round(2).astype(str) + "%"
  )
  display_reg_df["Avg_Delay"] = (
      display_reg_df["Avg_Delay"].round(2).astype(str) + " Days"
  )
  st.dataframe(display_reg_df, use_container_width=True)