import streamlit as st
import pandas as pd
import numpy as np

# Title and description
st.title("My First Streamlit App")
st.write("This is a simple interactive web app built entirely with Python!")

# Add a slider
number = st.slider("Pick a number", 0, 100, 25)
st.write("You picked:", number)

# Add text input
name = st.text_input("Enter your name")
if name:
    st.write(f"Hello {name}! 👋")

# Create sample data
data = pd.DataFrame({
    "x": np.arange(1, 11),
    "y": np.random.randint(1, 100, 10)
})

# Show data table
st.subheader("Sample Data Table")
st.dataframe(data)

# Show a simple line chart
st.subheader("Line Chart Example")
st.line_chart(data, x="x", y="y")

# Add a checkbox
if st.checkbox("Show raw data"):
    st.write(data)
