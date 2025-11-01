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
# PAGE SETUP
# -----------------------------------------------------------
st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")

st.title("Retail Sales Dashboard 📊")
st.write(
    "This dashboard demonstrates how Streamlit can be used to explore and "
    "visualize related business data — in this case, monthly retail sales "
    "and profit performance across multiple cities."
)

# -----------------------------------------------------------
# CREATE A RELATED DATASET
# -----------------------------------------------------------
np.random.seed(42)

months = ["January", "February", "March", "April", "May", "June"]
cities = ["Boston", "New York", "Chicago", "San Francisco", "Miami"]

records = []
for city in cities:
    base_sales = np.random.randint(80_000, 150_000)
    for month in months:
        sales = base_sales + np.random.randint(-10_000, 10_000)
        profit = sales * np.random.uniform(0.05, 0.20)
        records.append([city, month, sales, profit])

data = pd.DataFrame(records, columns=["City", "Month", "Sales ($)", "Profit ($)"])

# -----------------------------------------------------------
# SECTION 1 – DATAFRAME DEMO
# -----------------------------------------------------------
st.header("1. Data Overview")

st.subheader("Retail Sales Data")
st.dataframe(data, use_container_width=True)

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${data['Sales ($)'].sum():,}")
col2.metric("Total Profit", f"${data['Profit ($)'].sum():,}")
col3.metric("Average Profit Margin", f"{(data['Profit ($)'].sum() / data['Sales ($)'].sum())*100:.1f}%")

st.caption("Each record represents one city's monthly sales and profit figures.")

# -----------------------------------------------------------
# SECTION 2 – PLOTTING DEMO
# -----------------------------------------------------------
st.header("2. Visualization")

# Average monthly performance across all cities
monthly_summary = data.groupby("Month")[["Sales ($)", "Profit ($)"]].mean().reset_index()

st.subheader("Average Monthly Sales and Profit")
st.line_chart(monthly_summary.set_index("Month"))

# Relationship between sales and profit
st.subheader("Relationship Between Sales and Profit")
st.scatter_chart(data, x="Sales ($)", y="Profit ($)")

st.caption("The line chart shows average performance trends, while the scatter chart shows the correlation between sales and profit across all cities and months.")

# -----------------------------------------------------------
# SECTION 3 – CITY COMPARISON DEMO
# -----------------------------------------------------------
st.header("3. City Comparison")

selected_city = st.selectbox("Choose a city to view its performance", cities)

city_data = data[data["City"] == selected_city]
st.subheader(f"Monthly Sales Trend – {selected_city}")
st.line_chart(city_data.set_index("Month")[["Sales ($)", "Profit ($)"]])

st.caption("Select a city to compare its monthly performance in sales and profit.")

# -----------------------------------------------------------
# FOOTER
# -----------------------------------------------------------
st.write("---")
st.caption("Created by Yusuf Shaheen — Babson College OIM 7502 Midterm Project")
