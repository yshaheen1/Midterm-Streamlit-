# Displaying Text and Headings

import streamlit as st

st.title("Basic Streamlit functions")
st.header("Section Header")
st.subheader("Subsection Header")
st.write("This is an interactive dashboard")
x = st.slider("Select a value", 0, 100, 50)
st.write("You selected:", x)

# Displaying Data

import pandas as pd

data = pd.DataFrame({
    "Product": ["Shoes", "Shirts", "Pants"],
    "Sales": [100, 50, 80]
})
st.dataframe(data)    
st.table(data.head())

# Widgets
name = st.text_input("Enter your name")
age = st.slider("Select your age", 0, 100, 25)
show = st.checkbox("Show message")

if show:
    st.write(f"Hello {name}, you are {age} years old!")
