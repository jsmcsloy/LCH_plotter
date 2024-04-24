import streamlit as st 
import pandas as pd
import plotly.express as px

st.title("Simple plotter for LCH values")

# Side bar - Capture L, C, H and insert into dataframe
L = st.sidebar.number_input("Enter L value", format="%.2f")
C = st.sidebar.number_input("Enter C value", format="%.2f")
H = st.sidebar.number_input("Enter H value", format="%.2f")

# Load CSV of data points
data = st.sidebar.file_uploader("Load in the CSV file", type=['csv'])

if data is not None:
    df = pd.read_csv(data)
    try:
        fig = px.scatter_polar(df, r="C", theta="H", direction='counterclockwise', start_angle=0)
        fig.update_layout(
            polar=dict(
                radialaxis=dict(showticklabels=False)  # Hides the radial axis tick labels
            )
        )
        st.plotly_chart(fig)  # Correct method to display the plot in Streamlit
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.write("Please upload a CSV file to plot data.")
