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

# CREATE DATA

np.random.seed(42) # ensures that the sales numbers, profit margins, and map points don’t change each time the app runs

cities_ma = [
    "Boston", "Cambridge", "Worcester", "Springfield", "Lowell",
    "Brockton", "Quincy", "New Bedford", "Fall River", "Lynn"
]

months = ["January", "February", "March", "April", "May", "June"]

store_counts = np.random.randint(1, 4, size=len(cities_ma))  # Each city can have multiple stores

records = []
for city, count in zip(cities_ma, store_counts):
    for store in range(count):
        records.append({
            "City": city,
            "Store ID": f"{city[:3].upper()}-{store+1}",
            "Sales ($)": np.random.randint(40_000, 200_000),
            "Profit ($)": np.random.randint(5_000, 50_000),
            "Month": np.random.choice(months)
        })

data = pd.DataFrame(records)

# SECTION 1 – DATAFRAME DEMO

st.header("1. Store Performance Data")

st.subheader("Retail Stores Across Massachusetts")
st.dataframe(data, use_container_width=True)

col1, col2, col3 = st.columns(3)
col1.metric("Total Stores", f"{data.shape[0]}")
col2.metric("Total Sales", f"${data['Sales ($)'].sum():,}")
col3.metric("Average Profit Margin", f"{(data['Profit ($)'].sum()/data['Sales ($)'].sum())*100:.1f}%")


# SECTION 2 – PLOTTING DEMO

st.header("2. Sales and Profit Visualizations")

# Average performance per city
city_summary = (
    data.groupby("City")[["Sales ($)", "Profit ($)"]]
    .mean()
    .sort_values("Sales ($)", ascending=False)
)

st.subheader("Average Sales and Profit by City")
st.bar_chart(city_summary)

# Monthly sales trend (across all stores)
st.subheader("Total Monthly Sales Trend")
monthly_sales = (
    data.groupby("Month")["Sales ($)"]
    .sum()
    .reindex(months)
)
st.line_chart(monthly_sales)
st.caption("Shows total sales growth and seasonality over six months.")

# Profit margin by city
st.subheader("Average Profit Margin by City")
data["Profit Margin (%)"] = (data["Profit ($)"] / data["Sales ($)"]) * 100
margin_by_city = (
    data.groupby("City")["Profit Margin (%)"]
    .mean()
    .sort_values(ascending=False)
)
st.bar_chart(margin_by_city)
st.caption("Compares which cities are most efficient at turning sales into profit.")


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
