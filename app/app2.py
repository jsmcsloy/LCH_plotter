import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import numpy as np
import matplotlib as mpl
from colorspacious import cspace_converter

def lch_to_rgb(l, c, h):
    convert_to_rgb = cspace_converter("CIELCh", "sRGB1")
    rgb = convert_to_rgb((l, c, h))
    rgb = [max(0, min(1, x)) for x in rgb]
    return rgb

st.title("Trace CSV over HSV Plot")

data = st.sidebar.file_uploader("Load in the CSV file", type=['csv'])

if data is not None:
    df = pd.read_csv(data)

    theta = np.linspace(0, 2 * np.pi, 100)
    r = np.linspace(0, 1, 100)
    T, R = np.meshgrid(theta, r)
    X = R * np.cos(T)
    Y = R * np.sin(T)
    hsv = np.stack((T/(2 * np.pi), R, np.ones_like(R)), axis=-1)cd ap0
    rgb = mpl.colors.hsv_to_rgb(hsv)

    rgb_flat = rgb.reshape(-1, 3)
    fig = go.Figure(data=go.Scatter(x=X.flatten(), y=Y.flatten(), mode='markers',
                                    marker=dict(color=['rgb({},{},{})'.format(int(r*255), int(g*255), int(b*255)) for r, g, b in rgb_flat],
                                                size=10, opacity=0.5)))

    for index, row in df.iterrows():
        rgb = lch_to_rgb(row['L'], row['C'], row['H'])
        x_position = np.cos(row['H'] % 360 / 360 * 2 * np.pi) * row['C'] / 100
        y_position = np.sin(row['H'] % 360 / 360 * 2 * np.pi) * row['C'] / 100
        fig.add_trace(go.Scatter(x=[x_position], y=[y_position], mode='markers+text',
                                 text=f"L={row['L']}",
                                 marker=dict(size=12, color='rgb({},{},{})'.format(*[int(v * 255) for v in rgb]))))

    st.plotly_chart(fig)
else:
    st.write("Please upload a CSV file.")
