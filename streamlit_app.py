"""
Name:       Yusuf Shaheen
Library:    Streamlit
URL:        https://docs.streamlit.io
Description:
Streamlit allows users to create interactive data apps entirely with Python. 
This demo combines three examples — displaying a DataFrame, plotting charts, 
and showing a map — to demonstrate how Streamlit helps data scientists explore and present data interactively.
"""

import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------------------------------------
# PAGE SETUP
# -----------------------------------------------------------
st.set_page_config(page_title="Streamlit Combined Demo", layout="wide")

st.title("Streamlit Combined Demo 🚀")
st.write("This demo shows how to use Streamlit for data visualization, tables, and maps — all in one app.")

# -----------------------------------------------------------
# SECTION 1 – DATAFRAME DEMO
# -----------------------------------------------------------
st.header("1. DataFrame Demo")

# Create example data
data = pd.DataFrame({
    "Product": ["Shoes", "Shirts", "Jeans", "Jackets", "Hats"],
    "Sales": [120, 230, 310, 180, 140],
    "Profit": [20, 50, 80, 40, 25]
})

st.subheader("Sample Sales Data")
st.dataframe(data, use_container_width=True)

# Display basic stats
st.subheader("Summary Statistics")
st.write(data.describe())

# -----------------------------------------------------------
# SECTION 2 – PLOTTING DEMO
# -----------------------------------------------------------
st.header("2. Plotting Demo")

# Generate random data for charts
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["Category A", "Category B", "Category C"]
)

st.subheader("Line Chart Example")
st.line_chart(chart_data)

st.subheader("Scatter Chart Example")
st.scatter_chart(chart_data)

# -----------------------------------------------------------
# SECTION 3 – MAPPING DEMO
# -----------------------------------------------------------
st.header("3. Mapping Demo")

# Create random geographic data (Boston area)
map_data = pd.DataFrame({
    "lat": 42.36 + np.random.randn(100) * 0.01,
    "lon": -71.06 + np.random.randn(100) * 0.01
})

st.subheader("Map of Random Points (Boston Area)")
st.map(map_data)

# -----------------------------------------------------------
# FOOTER
# -----------------------------------------------------------
st.write("---")
st.caption("Created by Yusuf Shaheen — Babson College OIM 7502 Midterm Project")
