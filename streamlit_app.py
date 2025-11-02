"""
Name:        Yusuf Shaheen
Library:     Streamlit
URL:         https://appapppy-mhmrrcmgcgm25pw9sx45ez.streamlit.app/

Description:
This library allows data scientists and analysts to build interactive web applications
directly from Python scripts without any web development experience. Streamlit simplifies
data visualization, reporting, and model deployment by providing intuitive components such as
charts, tables, and interactive widgets. This project demonstrates its use in creating a
Massachusetts Retail Dashboard for visualizing sales, profit trends, and store locations.
"""


import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------
st.set_page_config(page_title="Massachusetts Retail Dashboard", layout="wide")

st.title("Massachusetts Retail Dashboard")
st.write(
    "This Streamlit demo shows fictional retail performance data across multiple "
    "cities in Massachusetts. It connects tables, charts, and maps to provide a complete analysis."
)

# -----------------------------------------------------------
# CREATE DATA
# -----------------------------------------------------------
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
# SECTION 3 – MAPPING DEMO (with automatic geocoding)
# -----------------------------------------------------------
st.header("3. Massachusetts Store Locations")

from geopy.geocoders import Nominatim

@st.cache_data
def get_city_coordinates(cities):
    """Fetch real latitude and longitude for each Massachusetts city."""
    geolocator = Nominatim(user_agent="streamlit-demo")
    coords = {}
    for city in cities:
        try:
            location = geolocator.geocode(f"{city}, Massachusetts, USA")
            if location:
                coords[city] = (location.latitude, location.longitude)
        except Exception:
            pass
    return coords

# Get coordinates dynamically
city_coords = get_city_coordinates(cities_ma)

# Create map data with small random offsets for multiple stores per city
map_points = []
for _, row in data.iterrows():
    if row["City"] in city_coords:
        base_lat, base_lon = city_coords[row["City"]]
        lat_jitter = np.random.uniform(-0.005, 0.005)
        lon_jitter = np.random.uniform(-0.005, 0.005)
        map_points.append({"lat": base_lat + lat_jitter, "lon": base_lon + lon_jitter})

map_df = pd.DataFrame(map_points)

st.subheader("Automatically Geocoded Store Map")
st.map(map_df)
st.caption(
    "Each dot represents a store location in Massachusetts. "
    "City coordinates were retrieved automatically using the geopy library."
)
# -----------------------------------------------------------
# FOOTER
# -----------------------------------------------------------
st.write("---")
st.caption("Created by Yusuf Shaheen — Babson College OIM 7502 Midterm Project")
