import streamlit as st 
import pandas as pd
import plotly.express as px

st.title("Simple plotter for LCH values")

#side bar - capture L,C,H and insert into dataframe
L = st.sidebar.number_input("Enter L value")
C = st.sidebar.number_input("Enter C value")
H = st.sidebar.number_input("Enter H value")

#load csv of data points
data = st.sidebar.file_uploader("load in the csv file......")

df = data


try:
    fig = px.scatter_polar(df, r="C", theta="H", direction='counterclockwise', start_angle=0)
    fig.update_layout(
        polar=dict(
            radialaxis=dict(showticklabels=False)  # Hides the radial axis tick labels
        )
    )

    fig.show()

except Exception as e:
    print(e)
