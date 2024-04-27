import streamlit as st 
import pandas as pd
import plotly.express as px
import numpy as np
from PIL import Image  # Import Image module from PIL library


# Add a L*a*b  or  LCH value manually to plot on the chatt or upload a cvs file. The csv must have columns L,a,b,Toner


# Function to convert L*a*b to LCH
def lab_to_lch(row):
    L, a, b = row['L'], row['a'], row['b']
    C = np.sqrt(a**2 + b**2)
    h_rad = np.arctan2(b, a)
    h_deg = np.degrees(h_rad) % 360
    return L, C, h_deg

st.title("Simple plotter for LCH or Lab values")

# Sidebar - capture L, C, H and insert into dataframe
colour_space = st.sidebar.radio("Select Colour Space", ["Lab", "LCH"])

if colour_space == "Lab":
    L = st.sidebar.number_input("Enter L value", value=50)
    a = st.sidebar.number_input("Enter a value", value=0)
    b = st.sidebar.number_input("Enter b value", value=0)
    ref = st.sidebar.text_input("Enter reference ")
    lab_data = (L, a, b)
    lch_data = lab_to_lch({'L': L, 'a': a, 'b': b})  # Convert Lab to LCH
    L, C, H = lch_data
else:
    L = st.sidebar.number_input("Enter L value", value=50)
    C = st.sidebar.number_input("Enter C value", value=50)
    H = st.sidebar.number_input("Enter H value", value=180)
    ref = st.sidebar.text_input("Enter reference ")

# Button to add LCH values into a list
if 'data_list' not in st.session_state:
    st.session_state.data_list = []

if st.sidebar.button("Add value"):
    if colour_space == "Lab":
        st.session_state.data_list.append({'L': L, 'C': C, 'H': H, "Toner": ref})
    else:
        st.session_state.data_list.append({'L': L, 'C': C, 'H': H, "Toner": ref})
    st.sidebar.success("Added: L={}, C={}, H={}, Ref={}".format(L, C, H, ref))

# Load CSV of data points
data_file = st.sidebar.file_uploader("Load in the CSV file...")

if data_file is not None:
    df = pd.read_csv(data_file)
    if 'L' in df.columns and 'a' in df.columns and 'b' in df.columns:
        # Convert Lab values to LCH
        df[['L', 'C', 'H']] = df.apply(lab_to_lch, axis=1, result_type='expand')
    else:
        st.error("CSV must contain 'L', 'a', and 'b' columns for Lab color space.")
else:
    # If no file uploaded yet, use accumulated data
    df = pd.DataFrame(st.session_state.data_list)

# Checkbox to toggle the scale
show_scale = st.sidebar.checkbox("Show Scale", value=True)

# Plotting only if dataframe is not empty
if not df.empty:
    
    try:

        st.markdown("""---""") 
        st.write("")
        #add a slider to control the background image opacity 
        opacity = st.slider(
        'Select chart background opacity',
        0.0, 1.0, (1.0)) 


        # Include the Toner as hover data
        fig = px.scatter_polar(df, r="C", theta="H", direction='counterclockwise', start_angle=-23, text="Toner", 
                               hover_data=df.columns, range_r=[0, 132])  # dynamically include all columns in hover data
        
        fig.update_layout ( 
        #make transparent
        polar_bgcolor = 'rgba(0,0,0,0)',
        paper_bgcolor = 'rgba(0,0,0,0)',

       
       
        # Show or hide the radial axis tick labels based on the checkbox
        polar=dict(
            radialaxis=dict(showticklabels=show_scale, visible= show_scale)),
            hoverlabel=dict(bgcolor="white", font_size=14, font_family="Rockwell"),

        #grab a LCH background image from the web
        images= [dict(
                    #source="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTEwJBlL0BSeVPaLCBKFk15vf-LKej1Kvx5yQ&usqp=CAU",
                    source="https://iili.io/JUVtZog.png",
                    xref="paper", yref="paper",
                    x=0.503, y=0.503,
                    sizex= 1.0, sizey=1.13,
                    xanchor="center",
                    yanchor="middle",
                    sizing="contain",
                    layer="below")], 
                    margin=dict(l=50, r=50, t=50, b=50))

        #update the image and grid
        fig.update_layout_images(opacity = opacity )
        fig.update_traces(marker=dict(size=8))
        fig.update_traces(textposition='top left')  # Adjust marker size as needed
    
        #plot chart on screen
        st.plotly_chart(fig)

            
    except Exception as e:
        st.error(f"Error generating plot: {e}")
else:
    st.info("Upload data or add LCH values to generate plot.")
