import streamlit as st 
import pandas as pd
import plotly.express as px
import numpy as np

# Function to convert L*a*b to LCH
def lab_to_lch(row):
    L, a, b = row['L'], row['a'], row['b']
    C = np.sqrt(a**2 + b**2)
    h_rad = np.arctan2(b, a)
    h_deg = np.degrees(h_rad) % 360
    return L, C, h_deg

st.title("Simple Plotter for LCH or Lab Values")

# Sidebar - select colour space
colour_space = st.sidebar.radio("Select Colour Space", ["Lab", "LCH"])

if colour_space == "Lab":
    L = st.sidebar.number_input("Enter L value", value=50.00)
    a = st.sidebar.number_input("Enter a value", value=0.00)
    b = st.sidebar.number_input("Enter b value", value=0.00)
else:
    L = st.sidebar.number_input("Enter L value", value=50.00)
    C = st.sidebar.number_input("Enter C value", value=50.00)
    H = st.sidebar.number_input("Enter H value", value=180.00)

ref = st.sidebar.text_input("Enter Reference")

# Initialize data storage
if 'data_list' not in st.session_state:
    st.session_state.data_list = []

# Add values to the list
if st.sidebar.button("Add value"):
    if colour_space == "Lab":
        lch_data = lab_to_lch({'L': L, 'a': a, 'b': b})
        st.session_state.data_list.append({'L': lch_data[0], 'C': lch_data[1], 'H': lch_data[2], "Toner": ref})
    else:
        st.session_state.data_list.append({'L': L, 'C': C, 'H': H, "Toner": ref})
    
    st.sidebar.success(f"Added: L={L}, C={C}, H={H}, Ref={ref}")

# Load CSV of data points
data_file = st.sidebar.file_uploader("Load in the CSV file...", type='csv')

if data_file is not None:
    df = pd.read_csv(data_file)
    if 'L' in df.columns and 'a' in df.columns and 'b' in df.columns:
        df[['L', 'C', 'H']] = df.apply(lab_to_lch, axis=1, result_type='expand')
    else:
        st.error("CSV must contain 'L', 'a', and 'b' columns for Lab color space.")
else:
    df = pd.DataFrame(st.session_state.data_list)

# Checkbox to toggle the scale
show_scale = st.sidebar.checkbox("Show Scale", value=False)

# Plotting only if dataframe is not empty
if not df.empty:
    try:
        st.markdown("---")
        opacity = st.slider('Select chart background opacity', 0.0, 1.0, 1.0)

        fig = px.scatter_polar(df, r="C", theta="H", text="Toner", height=600,
                                hover_data=df.columns, range_r=[0, 130],
                                direction='counterclockwise', start_angle=-23)

        # Update layout with images and settings
        fig.update_layout(
            polar_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="v", yanchor="bottom", y=1.02, xanchor="center", x=1),
            polar=dict(radialaxis=dict(showticklabels=show_scale, visible=show_scale)),
            hoverlabel=dict(bgcolor="white", font_size=16, font_family="Rockwell"),
            images=[dict(
                source="https://iili.io/JUVtZog.png",
                xref="paper", yref="paper",
                x=0.503, y=0.503,
                sizex=1.0, sizey=1.13,
                xanchor="center", yanchor="middle",
                sizing="contain", layer="below"
            )],
            margin=dict(l=50, r=50, t=50, b=50)
        )

        fig.update_layout_images(opacity=opacity)
        fig.update_traces(marker=dict(size=10), textposition='top left')

        # Plot chart on screen
        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Error generating plot: {e}")
else:
    st.info("Upload data or add LCH values to generate plot.")
