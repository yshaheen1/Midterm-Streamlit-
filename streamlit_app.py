"""
Name:       Yusuf Shaheen
Library:    Streamlit
URL:        https://docs.streamlit.io
Description:
Streamlit allows data scientists to create interactive dashboards quickly.
This demo shows retail store performance across 10 Massachusetts cities,
demonstrating how data, plots, and maps can work together in one workflow.
"""

import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------
st.set_page_config(page_title="Massachusetts Retail Dashboard", layout="wide")

st.title("Massachusetts Retail Dashboard 🛒")
st.write(
    "This Streamlit demo shows fictional store performance data across multiple "
    "cities in Massachusetts. It connects data tables, charts, and maps to tell one story."
)

# -----------------------------------------------------------
# CREATE DATA
# -----------------------------------------------------------

np.random.seed(42)

cities_ma = [
    "Boston", "Cambridge", "Worcester", "Springfield", "Lowell",
    "Brockton", "Quincy", "New Bedford", "Fall River", "Lynn"
]

# each city can have multiple stores
store_counts = np.random.randint(1, 4, size=len(cities_ma))  # 1–3 stores per city

records = []
for city, count in zip(cities_ma, store_counts):
    for store in range(count):
        records.append({
            "City": city,
            "Store ID": f"{city[:3].upper()}-{store+1}",
            "Sales ($)": np.random.randint(40_000, 200_000),
            "Profit ($)": np.random.randint(5_000, 50_000),
            "Month": np.random.choice(["January", "February", "March", "April"])
        })

data = pd.DataFrame(records)

# -----------------------------------------------------------
# SECTION 1 – DATAFRAME DEMO
# -----------------------------------------------------------
st.header("1. Store Performance Data")

st.subheader("Retail Stores Across Massachusetts")
st.dataframe(data, use_container_width=True)

col1, col2, col3 = st.columns(3)
col1.metric("Total Stores", f"{data.shape[0]}")
col2.metric("Total Sales", f"${data['Sales ($)'].sum():,}")
col3.metric("Average Profit Margin", f"{(data['Profit ($)'].sum()/data['Sales ($)'].sum())*100:.1f}%")

# -----------------------------------------------------------
# SECTION 2 – PLOTTING DEMO
# -----------------------------------------------------------
st.header("2. Sales and Profit Visualizations")

# Average performance per city
city_summary = (
    data.groupby("City")[["Sales ($)", "Profit ($)"]]
    .mean()
    .sort_values("Sales ($)", ascending=False)
)

st.subheader("Average Sales and Profit by City")
st.bar_chart(city_summary)

st.subheader("Scatter Chart: Relationship Between Sales and Profit")
st.scatter_chart(data, x="Sales ($)", y="Profit ($)")

st.caption("This helps identify which cities have strong sales but lower profit margins.")

# -----------------------------------------------------------
# SECTION 3 – MAPPING DEMO
# -----------------------------------------------------------
st.header("3. Massachusetts Store Locations")

# simple city coordinates (approximate lat/lon)
city_coords = {
    "Boston": (42.3601, -71.0589),
    "Cambridge": (42.3736, -71.1097),
    "Worcester": (42.2626, -71.8023),
    "Springfield": (42.1015, -72.5898),
    "Lowell": (42.6334, -71.3162),
    "Brockton": (42.0834, -71.0184),
    "Quincy": (42.2529, -71.0023),
    "New Bedford": (41.6362, -70.9342),
    "Fall River": (41.7015, -71.1550),
    "Lynn": (42.4668, -70.9495),
}

# Create small jitter for multiple stores in same city
map_points = []
for _, row in data.iterrows():
    base_lat, base_lon = city_coords[row["City"]]
    lat_jitter = np.random.uniform(-0.01, 0.01)
    lon_jitter = np.random.uniform(-0.01, 0.01)
    map_points.append({"lat": base_lat + lat_jitter, "lon": base_lon + lon_jitter})

map_df = pd.DataFrame(map_points)

st.subheader("Map of Massachusetts Store Locations")
st.map(map_df)

st.caption("Each dot represents a store location across Massachusetts cities.")

# -----------------------------------------------------------
# FOOTER
# -----------------------------------------------------------
st.write("---")
st.caption("Created by Yusuf Shaheen — Babson College OIM 7502 Midterm Project")
