"""
Name:       Yusuf Shaheen
Library:    Streamlit
URL:        https://appapppy-mhmrrcmgcgm25pw9sx45ez.streamlit.app/
Description:
Streamlit allows users to create interactive data apps entirely with Python. 
This demo combines three examples — displaying a DataFrame, plotting charts, 
and showing a map — to demonstrate how Streamlit helps data scientists explore and present data interactively.
"""

import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------
st.set_page_config(page_title="Sales Dashboard Demo", layout="wide")

st.title("📊 Streamlit Sales Dashboard Demo")
st.write("This app demonstrates how Streamlit can be used for connected data analysis — showing sales data, visualizations, and store locations all tied together.")

# -----------------------------------------------------------
# CREATE ONE LINKED DATASET
# -----------------------------------------------------------
np.random.seed(42)
cities = ["Boston", "New York", "Chicago", "Los Angeles", "San Francisco", "Miami", "Dallas", "Seattle"]
lats = [42.36, 40.71, 41.88, 34.05, 37.77, 25.76, 32.78, 47.61]
lons = [-71.06, -74.00, -87.63, -118.24, -122.42, -80.19, -96.80, -122.33]
sales = np.random.randint(50000, 200000, size=len(cities))
profit = np.round(sales * np.random.uniform(0.1, 0.3, size=len(cities)), 2)

data = pd.DataFrame({
    "City": cities,
    "Latitude": lats,
    "Longitude": lons,
    "Sales ($)": sales,
    "Profit ($)": profit
})

# -----------------------------------------------------------
# SECTION 1 – DATAFRAME DEMO
# -----------------------------------------------------------
st.header("1️⃣ Data Overview")

st.write("Below is the dataset of eight fictional store locations across the US.")
st.dataframe(data, use_container_width=True)

col1, col2, col3 = st.columns(3)
col1.metric("Number of Stores", len(data))
col2.metric("Total Sales", f"${data['Sales ($)'].sum():,.0f}")
col3.metric("Total Profit", f"${data['Profit ($)'].sum():,.0f}")

st.write("**Summary Statistics:**")
st.dataframe(data.describe(), use_container_width=True)

# -----------------------------------------------------------
# SECTION 2 – PLOTTING DEMO
# -----------------------------------------------------------
st.header("2️⃣ Sales & Profit Visualization")

# Sort data for nicer plotting
data_sorted = data.sort_values("Sales ($)", ascending=False)

st.subheader("Bar Chart of Sales by City")
st.bar_chart(data_sorted.set_index("City")["Sales ($)"])

st.subheader("Sales vs Profit Scatter Plot")
st.scatter_chart(data_sorted, x="Sales ($)", y="Profit ($)")

# -----------------------------------------------------------
# SECTION 3 – MAPPING DEMO
# -----------------------------------------------------------
st.header("3️⃣ Store Locations Map")

st.write("The map below shows where each store is located. Hover over points to see which city they represent.")
map_data = data.rename(columns={"Latitude": "lat", "Longitude": "lon"})
st.map(map_data)

# -----------------------------------------------------------
# CONCLUSION
# -----------------------------------------------------------
st.write("---")
st.markdown("""
### ✅ Summary
This connected demo shows how **Streamlit** can:
- Display and summarize business data with `st.dataframe()`  
- Visualize key metrics using `st.bar_chart()` and `st.scatter_chart()`  
- Plot geographic data on a map with `st.map()`  

Together, these tools create a quick, interactive dashboard that helps data scientists and analysts explore and present insights in real time.
""")

st.caption("Created by Yusuf Shaheen — Babson College OIM 7502 Midterm Project")
