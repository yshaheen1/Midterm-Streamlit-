"""
Name:       Yusuf Shaheen
Library:    Streamlit
URL:        https://appapppy-mhmrrcmgcgm25pw9sx45ez.streamlit.app/
Description:
Streamlit allows data scientists to create interactive dashboards quickly.
This demo shows fictional retail store performance across Massachusetts
over six months, combining data, charts, and mapping.
"""

import streamlit as st
import pandas as pd
import numpy as np


# PAGE CONFIG

st.set_page_config(page_title="Massachusetts Retail Dashboard", layout="wide")

st.title("Massachusetts Retail Dashboard")
st.write(
    "This Streamlit demo shows fictional retail performance data across multiple "
    "cities in Massachusetts. It connects tables, charts, and maps to provide a complete analysis."
)

# -----------------------------------------------------------
# DATASET CREATION (shared across all demos)
# -----------------------------------------------------------
np.random.seed(42)

store_types = ["Grocery", "Clothing", "Electronics", "Pharmacy", "Sports"]
num_stores = 100

map_data = pd.DataFrame({
    "lat": np.random.randn(num_stores) / 50 + 42.36,
    "lon": np.random.randn(num_stores) / 50 - 71.06,
    "Store Type": np.random.choice(store_types, num_stores)
})


# -----------------------------------------------------------
# SECTION 1 – DATAFRAME DEMO (Store Overview)
# -----------------------------------------------------------
st.header("1. Retail Store Data Overview")

st.markdown("#### Explore the Retail Store Dataset")

# Reuse map_data generated in Demo 3
st.dataframe(map_data, use_container_width=True)

# Calculate summary stats
total_stores = map_data.shape[0]
store_type_counts = map_data["Store Type"].value_counts()
top_type = store_type_counts.idxmax()
top_count = store_type_counts.max()

# KPI metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Stores", total_stores)
col2.metric("Most Common Type", top_type)
col3.metric("Count of Top Type", top_count)

st.caption(
    "This dataset contains 100 simulated retail stores across Massachusetts. "
    "Each store is randomly assigned a category and geographic coordinates. "
    "KPIs summarize total store count and category distribution."
)


# -----------------------------------------------------------
# SECTION 2 – VISUALIZATION DEMO (Store Analytics)
# -----------------------------------------------------------
st.header("2. Retail Store Distribution and Analysis")

st.markdown("#### Store Count by Retail Type")

# Bar chart: number of stores per category
type_counts = map_data["Store Type"].value_counts().reset_index()
type_counts.columns = ["Store Type", "Count"]

st.bar_chart(type_counts.set_index("Store Type"))

st.markdown("#### Store Distribution by Region (Latitude)")

# Line chart: average latitude per store type (simulating north-south spread)
lat_summary = map_data.groupby("Store Type")["lat"].mean().reset_index()
lat_summary = lat_summary.sort_values("lat", ascending=False)
st.line_chart(lat_summary.set_index("Store Type"))

st.caption(
    "The bar chart shows how stores are distributed by category, "
    "while the line chart highlights how store types are geographically positioned across Massachusetts."
)



# -----------------------------------------------------------
# SECTION 3 – MAPPING DEMO (Interactive Store Type Dropdown)
# -----------------------------------------------------------
st.header("3. Massachusetts Store Locations")

st.markdown("#### Explore Retail Store Types Across Massachusetts")

# Define retail categories
store_types = ["Grocery", "Clothing", "Electronics", "Pharmacy", "Sports"]

# Fixed number of stores
num_stores = 100

# Randomly assign store types and coordinates around Massachusetts (centered near Boston)
map_data = pd.DataFrame({
    "lat": np.random.randn(num_stores) / 50 + 42.36,
    "lon": np.random.randn(num_stores) / 50 - 71.06,
    "Store Type": np.random.choice(store_types, num_stores)
})

# Sidebar or main dropdown for selecting store type
selected_type = st.selectbox("Select a Retail Store Type", store_types)

# Filter map data based on selection
filtered_data = map_data[map_data["Store Type"] == selected_type]

# Display metrics and map
col1, col2 = st.columns([1, 2])

with col1:
    st.metric("Total Stores in Massachusetts", num_stores)
    st.metric(f"{selected_type} Stores", filtered_data.shape[0])
    st.write("Each dot represents a store of the selected type.")

with col2:
    st.map(filtered_data, color=(255, 0, 130), size=10)

st.caption(
    f"Showing {filtered_data.shape[0]} {selected_type.lower()} store locations out of {num_stores} total stores across Massachusetts. "
    "This demonstrates how Streamlit widgets like dropdowns can filter and dynamically update geospatial data visualizations."
)
