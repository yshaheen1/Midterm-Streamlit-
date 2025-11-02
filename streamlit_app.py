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

np.random.seed(42)

cities_ma = [
    "Boston", "Cambridge", "Worcester", "Springfield", "Lowell",
    "Brockton", "Quincy", "New Bedford", "Fall River", "Lynn"
]

months = ["January", "February", "March", "April", "May", "June"]

# Each city can have multiple stores

store_counts = np.random.randint(1, 4, size=len(cities_ma))  # 1–3 stores per city

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


# SECTION 3 – MAPPING DEMO 

st.header("3. Massachusetts Store Locations")

@st.cache_data
def get_city_coordinates():
    """Predefined coordinates for Massachusetts cities."""
    return {
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

city_coords = get_city_coordinates()

map_points = []
for _, row in data.iterrows():
    base_lat, base_lon = city_coords[row["City"]]
    lat_jitter = np.random.uniform(-0.005, 0.005)
    lon_jitter = np.random.uniform(-0.005, 0.005)
    map_points.append({"lat": base_lat + lat_jitter, "lon": base_lon + lon_jitter})

map_df = pd.DataFrame(map_points)

st.subheader("Massachusetts Store Map")
st.map(map_df)
st.caption(
    "Each dot represents a retail store location across Massachusetts cities. "
)
