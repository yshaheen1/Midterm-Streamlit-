"""
Name:       Yusuf Shaheen
Library:    Streamlit
URL:        https://appapppy-mhmrrcmgcgm25pw9sx45ez.streamlit.app/
Description:
Streamlit allows data scientists to create interactive dashboards quickly.
This demo shows fictional retail store performance across Boston, combining data, charts, and mapping.
"""


# IMPORTS

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


# DATASET CREATION (shared across all demos)

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


# DEMO 1 – DATAFRAME OVERVIEW

st.header("1. Retail Store Data Overview")
st.markdown("#### Explore the Boston Retail Dataset")

st.dataframe(map_data.drop(columns=["lat", "lon"]), use_container_width=True) # Hide latitude and longitude when displaying

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
    "The dataset contains 100 simulated Boston retail stores, "
    "each with randomly assigned categories, sales, and revenue values."
)


# DEMO 2 – VISUALIZATION ANALYTICS  

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

st.markdown("#### Profit Margin by Store Type")

# Calculate profit margin per store
map_data["Profit Margin (%)"] = (map_data["Revenue ($)"] / map_data["Sales ($)"]) * 100

# Average margin per category
margin_summary = map_data.groupby("Store Type")["Profit Margin (%)"].mean().reset_index()

# Horizontal bar chart
margin_chart = (
    alt.Chart(margin_summary)
    .mark_bar(color="#FF0082")
    .encode(
        x=alt.X("Profit Margin (%):Q", title="Average Profit Margin (%)"),
        y=alt.Y("Store Type:N", sort="-x", title="Store Type"),
        tooltip=["Store Type", "Profit Margin (%)"]
    )
    .properties(title="Average Profit Margin by Store Type")
)
st.altair_chart(margin_chart, use_container_width=True)

st.caption(
    "This chart highlights which retail categories are most efficient at converting sales into revenue. "
    "Higher profit margins indicate stronger financial performance relative to total sales."
)





# DEMO 3 – MAPPING DEMO 

st.header("3. Boston Store Locations")
st.markdown("#### Retail Store Map (Single Color)")

# Dropdown to filter store type
selected_type = st.selectbox("Select a Retail Store Type", ["All"] + store_types)

# Filter data
if selected_type != "All":
    filtered_data = map_data[map_data["Store Type"] == selected_type].copy()
else:
    filtered_data = map_data.copy()

# --- Display metrics and map ---
col1, col2 = st.columns([1, 2])

with col1:
    st.metric("Total Stores", f"{filtered_data.shape[0]}")
    st.metric("Total Revenue", f"${filtered_data['Revenue ($)'].sum():,.0f}")
    st.metric("Average Revenue", f"${filtered_data['Revenue ($)'].mean():,.0f}")

with col2:
    st.map(filtered_data, color=(255, 0, 130), size=10)


st.caption(
    "The map updates dynamically based on the selected store type."
)

