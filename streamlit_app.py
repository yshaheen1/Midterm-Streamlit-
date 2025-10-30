import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# -------------------------------------------------------------------
# Page setup
# -------------------------------------------------------------------
st.set_page_config(page_title="Simple Streamlit Demo", layout="wide")
st.title("Streamlit Demo for Data Science")
st.write("Upload a CSV file or use an example dataset, then explore and train a small model.")

# -------------------------------------------------------------------
# Data loading
# -------------------------------------------------------------------
st.sidebar.header("Step 1. Load Data")

uploaded = st.sidebar.file_uploader("Upload CSV file", type=["csv"])
use_example = st.sidebar.checkbox("Use example dataset (housing prices)")

if uploaded:
    df = pd.read_csv(uploaded)
    st.success("✅ Uploaded dataset loaded!")
elif use_example:
    from sklearn.datasets import fetch_california_housing
    data = fetch_california_housing(as_frame=True)
    df = data.frame
    df["target"] = data.target
    st.info("Using built-in California housing dataset.")
else:
    st.warning("Please upload a CSV file or select the example dataset.")
    st.stop()

# -------------------------------------------------------------------
# Explore the data
# -------------------------------------------------------------------
st.header("1. Explore Data")

st.write("### Preview of the dataset")
st.dataframe(df.head(), use_container_width=True)

st.write("### Basic information")
col1, col2, col3 = st.columns(3)
col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])
col3.metric("Missing values", int(df.isna().sum().sum()))

# Choose numeric columns for plotting
num_cols = df.select_dtypes(include=np.number).columns.tolist()
if len(num_cols) >= 2:
    x_col = st.selectbox("Select X-axis column", num_cols, index=0)
    y_col = st.selectbox("Select Y-axis column", num_cols, index=1)
    st.write("### Scatter chart")
    st.scatter_chart(df[[x_col, y_col]], x=x_col, y=y_col)
else:
    st.info("Need at least two numeric columns to plot a chart.")

# -------------------------------------------------------------------
# Train a small regression model
# -------------------------------------------------------------------
st.header("2. Train a Simple Model")

target = st.selectbox("Choose target column (the value you want to predict)", df.columns, index=len(df.columns)-1)
feature = st.selectbox("Choose feature column (used for prediction)", [c for c in df.columns if c != target])

if st.button("Train Model"):
    X = df[[feature]]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    rmse = mean_squared_error(y_test, preds, squared=False)
    r2 = r2_score(y_test, preds)

    st.success("✅ Model trained successfully!")
    st.metric("RMSE", f"{rmse:.4f}")
    st.metric("R² Score", f"{r2:.4f}")

    # Show a few predictions
    results = pd.DataFrame({"Actual": y_test.head(10).values, "Predicted": preds[:10]})
    st.write("### Sample Predictions")
    st.dataframe(results)

# -------------------------------------------------------------------
# About section
# -------------------------------------------------------------------
st.header("3. Why This Matters for Data Scientists")
st.write("""
- Build dashboards and share results without web development.
- Use widgets (slider, selectbox, file uploader) for live interactivity.
- Combine Streamlit with pandas, sklearn, or any data library.
""")
