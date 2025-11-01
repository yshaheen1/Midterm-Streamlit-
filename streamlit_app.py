"""
Name:       Yusuf Shaheen
Library:    Streamlit
URL:        https://docs.streamlit.io
Description:
Streamlit allows data scientists to create interactive dashboards directly in Python.
This demo presents a Massachusetts retail sales dashboard combining a data table,
charts, and a map — all connected to the same dataset.
"""

import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------------------------------------
# PAGE SETUP
# -----------------------------------------------------------
st.set_page_config(page_title="Massachusetts Retail Dashboard", layout="wide")

st.title("Massachusetts Retail Dashboard 🏬")
st.write(
    "This dashboard demonstrates how Streamlit can combine data tables, charts, "
    "and maps in one cohesive workflow using Python."
)

# -----------------------------------------------------------
# DATA CREATION – MASSACHUSETTS CITIES
# -----------------------------------------------------------
np.random.seed(42)

# Define cities and approximate coordinates for mapping
ma_cities = {
    "Boston": (42.36, -71.06),
    "Worcester": (42.26, -71.80),
    "Springfield": (42.10, -72.59),
    "Lowell": (42.63, -71.32),
    "Cambridge": (42.37, -71.11),
}

# Create DataFrame with sales and profit only (no lat/lon in visible table)
sales_data = pd.DataFrame({
    "City": list(ma_cities.keys()),
    "Sales ($)": np.random.randint(60_000, 200_000, size=len(ma_cities)),
    "Profit ($)": np.random.randint(8_000, 40_000, size=len(ma_cities))
})

# Create hidden coordinates DataFrame for mapping
map_data = pd.DataFrame({
    "lat": [coords[0] for coords in ma_cities.values()],
    "lon": [coords[1] for coords in ma_cities.values()]
})

# -----------------------------------------------------------
# SECTION 1 – DATA OVERVIEW
# -----------------------------------------------------------
st.header("1. Sales Overview by City")

st.subheader("Retail Performance Across Massachusetts")
st.dataframe(sales_data, use_container_width=True)

total_sales = sales_data["Sales ($)"].sum()
total_profit = sales_data["Profit ($)"].sum()
profit_margin = (total_profit / total_sales) * 100

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Profit Margin", f"{profit_margin:.1f}%")

# -----------------------------------------------------------
# SECTION 2 – PLOTTING DEMO
# -----------------------------------------------------------
st.header("2. Visualize Sales and Profit")

st.subheader("Bar Chart – Sales and Profit by City")
chart_data = sales_data.set_index("City")[["Sales ($)", "Profit ($)"]]
st.bar_chart(chart_data)

st.subheader("Scatter Plot – Relationship Between Sales and Profit")
st.scatter_chart(sales_data, x="Sales ($)", y="Profit ($)")

st.caption("Data scientists can use these charts to spot cities with high sales but low profit efficiency.")

# -----------------------------------------------------------
# SECTION 3 – MAPPING DEMO
# -----------------------------------------------------------
st.header("3. Massachusetts Store Map")

st.subheader("Store Locations Across Massachusetts")
st.map(map_data)

st.caption("The map shows the approximate locations of the retail stores within the state of Massachusetts.")

# -----------------------------------------------------------
# FOOTER
# -----------------------------------------------------------
st.write("---")
st.caption("Created by Yusuf Shaheen — Babson College OIM 7502 Midterm Project")
