"""
Name:       Yusuf Shaheen
Library:    Streamlit
URL:        https://appapppy-mhmrrcmgcgm25pw9sx45ez.streamlit.app/
Description:
Streamlit allows data scientists to create interactive dashboards quickly.
This demo shows fictional retail store performance across Massachusetts
over six months, combining data, charts, and mapping.
"""

# -----------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# -----------------------------------------------------------
# DATASET CREATION (shared across all demos)
# -----------------------------------------------------------
np.random.seed(42)

store_types = ["Grocery", "Clothing", "Electronics", "Pharmacy", "Sports"]
num_stores = 100

map_data = pd.DataFrame({
    "lat": np.random.randn(num_stores) / 50 + 42.36,
    "lon": np.random.randn(num_stores) / 50 - 71.06,
    "Store Type": np.random.choice(store_types, num_stores),
    "Sales ($)": np.random.randint(20000, 200000, num_stores)
})

# Generate revenue as a fraction of sales with variability
map_data["Revenue ($)"] = (map_data["Sales ($)"] * np.random.uniform(0.5, 0.9, num_stores)).astype(int)

# -----------------------------------------------------------
# DEMO 1 – DATAFRAME OVERVIEW
# -----------------------------------------------------------
st.header("1. Retail Store Data Overview")
st.markdown("#### Explore the Massachusetts Retail Dataset")

st.dataframe(map_data, use_container_width=True)

# KPIs
total_stores = map_data.shape[0]
total_sales = map_data["Sales ($)"].sum()
total_revenue = map_data["Revenue ($)"].sum()
avg_margin = (total_revenue / total_sales) * 100

col1, col2, col3 = st.columns(3)
col1.metric("Total Stores", total_stores)
col2.metric("Total Sales", f"${total_sales:,.0f}")
col3.metric("Revenue Margin (%)", f"{avg_margin:.1f}%")

st.caption(
    "The dataset contains 100 simulated Massachusetts retail stores, "
    "each with randomly assigned categories, sales, and revenue values."
)

# -----------------------------------------------------------
# DEMO 2 – VISUALIZATION ANALYTICS  (fixed for Altair 5)
# -----------------------------------------------------------
st.header("2. Sales and Revenue Analytics")
st.markdown("#### Store Performance by Type")

# Aggregate total sales and revenue by store category
agg = map_data.groupby("Store Type")[["Sales ($)", "Revenue ($)"]].sum().reset_index()

# Melt the dataframe so Altair can read Metric / Value pairs
agg_melted = agg.melt(id_vars="Store Type", var_name="Metric", value_name="Value")

# Bar chart comparing total Sales vs Revenue by category
chart = (
    alt.Chart(agg_melted)
    .mark_bar()
    .encode(
        x=alt.X("Store Type:N", title="Retail Category"),
        y=alt.Y("Value:Q", title="Amount ($)"),
        color=alt.Color("Metric:N", title="Metric"),
        column=alt.Column("Metric:N", title=None),
        tooltip=["Store Type", "Metric", "Value"]
    )
    .properties(title="Total Sales and Revenue by Store Type")
    .configure_axis(labelFontSize=12, titleFontSize=12)
)
st.altair_chart(chart, use_container_width=True)

st.caption(
    "The bar chart compares total sales and revenue by store category, "
)

# -----------------------------------------------------------
# DEMO 3 – MAPPING DEMO (Revenue-based Coloring)
# -----------------------------------------------------------
st.header("3. Massachusetts Store Locations")

st.markdown("#### Map Colored by Revenue Levels")

# Dropdown to filter store type
selected_type = st.selectbox("Select a Retail Store Type", ["All"] + store_types)

if selected_type != "All":
    filtered_data = map_data[map_data["Store Type"] == selected_type]
else:
    filtered_data = map_data

st.map(filtered_data, color=(255, 0, 130), size=10)

# Plot with dynamic colors
st.map(filtered_data, color=filtered_data["color"], size=10)

# Display KPIs and map
col1, col2 = st.columns([1, 2])
with col1:
    st.metric("Total Stores", f"{filtered_data.shape[0]}")
    st.metric("Total Revenue", f"${filtered_data['Revenue ($)'].sum():,.0f}")
    st.metric("Average Revenue", f"${filtered_data['Revenue ($)'].mean():,.0f}")
with col2:
    st.map(filtered_data, color=filtered_data["color"], size=10)

st.caption(
    "The map visualizes 100 Massachusetts retail stores. "
    "Each dot represents a store, with darker magenta shades indicating higher revenue."
)
