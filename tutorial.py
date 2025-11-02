import streamlit as st
st.title("Hello Streamlit!")
st.write("This is my first interactive dashboard.")
x = st.slider("Select a value", 0, 100, 50)
st.write("You selected:", x)
