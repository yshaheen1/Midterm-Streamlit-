"""
Name:       Yusuf Shaheen
Library:    Streamlit
URL:        https://docs.streamlit.io
Description:
A simple Streamlit demo showing how to visualize data interactively using charts.
"""

import streamlit as st
import pandas as pd
import numpy as np

# ----------------------------------------------------------
# PAGE SETUP
# ----------------------------------------------------------
st.set_page_config(page_title="Streamlit Plotting Demo", layout="centered")
st.title("📊 Streamlit Plotting Demo")
st.write("This basic example shows how to create simple charts with Streamlit.")

# ----------------------------------------------------------
# CREATE SAMPLE DATA
# ----------------------------------------------------------
st.header("1. Generate Random Data")

rows = st.slider("Select number of rows", 10, 100, 30)
data = pd.DataFrame({
    "x": np.arange(1, rows + 1),
    "y": np.random.randint(1, 100, size=rows),
    "z": np.random.randn(rows).cumsum()
})

st.write("Here’s a preview of the dataset:")
st.dataframe(data)

# ----------------------------------------------------------
# PLOTTING EXAMPLES
# ----------------------------------------------------------
st.header("2. Plot Charts")

st.subheader("Line Chart")
st.line_chart(data[["x", "z"]])

st.subheader("Area Chart")
st.area_chart(data[["x", "y"]])

st.subheader("Bar Chart")
st.bar_chart(data[["x", "y"]])

# ----------------------------------------------------------
# ADD SIMPLE INTERACTIVITY
# ----------------------------------------------------------
st.header("3. Interactive Chart")
col_x = st.selectbox("Select X-axis column", data.columns, index=0)
col_y = st.selectbox("Select Y-axis column", data.columns, index=1)
st.write(f"Plotting **{col_y}** vs **{col_x}**")

st.scatter_chart(data, x=col_x, y=col_y)

# ----------------------------------------------------------
# ABOUT
# ----------------------------------------------------------
st.header("4. What You Learned")
st.markdown("""
- How to create charts with Streamlit (`line_chart`, `bar_chart`, `area_chart`, `scatter_chart`)
- How to add widgets for user input (sliders and selectboxes)
- How to quickly turn data into interactive visuals without any JavaScript
""")
