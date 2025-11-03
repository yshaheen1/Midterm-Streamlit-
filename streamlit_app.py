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
# SECTION 3 – MAPPING DEMO (100 Stores + Widget Interaction)
# -----------------------------------------------------------
st.header("3. Massachusetts Store Locations")

st.markdown("#### Plot a Map")

# Create 100 random store locations centered near Boston
map_data = pd.DataFrame(
    np.random.randn(100, 2) / [50, 50] + [42.36, -71.06],
    columns=["lat", "lon"]
)

# Display the map with fixed color and point size
st.map(map_data, color=(255, 0, 130), size=10)

st.caption(
    "This map displays 100 simulated store locations distributed around Boston, Massachusetts. "
    "It demonstrates Streamlit’s ability to visualize geographic data using the built-in `st.map()` function."
)

# -----------------------------------------------------------
# INTERACTIVE WIDGETS DEMO (Inspired by Streamlit Sample)
# -----------------------------------------------------------
st.markdown("### Interactive Widgets and Columns")
st.markdown("#### Sliders with Containers")

# Create a three-column layout
left_column, middle_column, right_column = st.columns(3)

# Left Column – slider inside bordered container
with left_column:
    with st.container(border=True):
        x = st.slider(
            "Number of Points",
            min_value=10,
            max_value=200,
            value=50,
            step=10,
            help="Choose how many random values to generate for the histogram."
        )
        st.write(f"Generate {x} random values from a normal distribution.")

# Right Column – histogram visualization using Altair
with right_column:
    import altair as alt
    slide_data = pd.DataFrame({"values": np.random.normal(loc=10, scale=1.5, size=x)})
    chart = (
        alt.Chart(slide_data)
        .mark_bar(color="#FF0082")
        .encode(
            alt.X("values:Q", bin=True, title="Value"),
            alt.Y("count()", title="Frequency"),
        )
        .properties(title="Histogram Generated from Slider")
    )
    st.altair_chart(chart, use_container_width=True)

# Middle Column – instructions or summary
with middle_column:
    st.info(
        "This section demonstrates Streamlit’s ability to combine widgets, containers, and columns. "
        "Adjust the slider on the left to dynamically update the histogram on the right."
    )

st.caption(
    "Widgets like sliders and containers make dashboards interactive and intuitive, "
    "helping users control data and visualizations in real time."
)
