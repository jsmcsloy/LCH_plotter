import streamlit as st 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from PIL import Image  # Import Image module from PIL library
import plot_3d as lcm  # Ensure this module is available in your environment


# Function to convert L*a*b to LCH
def lab_to_lch(row):
    L, a, b = row['L'], row['a'], row['b']
    C = np.sqrt(a**2 + b**2)
    h_rad = np.arctan2(b, a)
    h_deg = np.degrees(h_rad) % 360
    return L, C, h_deg

st.title("Plot LCH or Lab values")

# Sidebar - capture L, C, H and insert into dataframe
colour_space = st.sidebar.radio("Select Colour Space", ["Lab", "LCH"])

if colour_space == "Lab":
    L = st.sidebar.number_input("Enter L value", value=50.00)
    a = st.sidebar.number_input("Enter a value", value=0.00)
    b = st.sidebar.number_input("Enter b value", value=0.00)
    ref = st.sidebar.text_input("Enter reference ")
    lab_data = (L, a, b)
    lch_data = lab_to_lch({'L': L, 'a': a, 'b': b})  # Convert Lab to LCH
    L_value, C, H = lch_data
else:
    L_value = st.sidebar.number_input("Enter L value", value=50.00)
    C = st.sidebar.number_input("Enter C value", value=50.00)
    H = st.sidebar.number_input("Enter H value", value=180.00)
    ref = st.sidebar.text_input("Enter reference ")

# Button to add LCH values into a list
if 'data_list' not in st.session_state:
    st.session_state.data_list = []

if st.sidebar.button("Add value"):
    st.session_state.data_list.append({'L': L_value, 'C': C, 'H': H, "Toner": ref})
    st.sidebar.success(f"Added: L={L_value}, C={C}, H={H}, Ref={ref}")

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
show_scale = st.sidebar.checkbox("Show Scale", value=False)

# Checkbox to toggle the flip to 3D scale
show_3d = st.sidebar.checkbox("Show in 3D", value=False)

if not show_3d: 
    # Plotting only if dataframe is not empty
    if not df.empty:
        try:
            st.markdown("""---""") 
            st.write("")
            # Add a slider to control the background image opacity 
            opacity = st.slider('Select chart background opacity', 0.0, 1.0, 1.0) 

            # Check if "source" column is present in the DataFrame
            if "Source" in df.columns:
                fig = px.scatter_polar(df, r="C", theta="H", color="Source", direction='counterclockwise', start_angle=-23, text="Toner", height=600,
                                       hover_data=df.columns, range_r=[0, 130])
            else:
                fig = px.scatter_polar(df, r="C", theta="H", direction='counterclockwise', start_angle=-23, text="Toner", height=600,
                                       hover_data=df.columns, range_r=[0, 130])
            
            fig.update_layout( 
                legend=dict(
                    orientation="v",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=1
                ),       
                polar_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                polar=dict(
                    radialaxis=dict(showticklabels=show_scale, visible=show_scale)
                ),
                hoverlabel=dict(bgcolor="white", font_size=16, font_family="Rockwell"),
                images=[dict(
                    source= "app/wheel.jpg",    # "https://iili.io/JUVtZog.png"
                    xref="paper", yref="paper",
                    x=0.503, y=0.503,
                    sizex=1.0, sizey=1.13,
                    xanchor="center",
                    yanchor="middle",
                    sizing="contain",
                    layer="below"
                )],
                margin=dict(l=50, r=50, t=50, b=50)
            )

            # Update the image and grid
            fig.update_layout_images(opacity=opacity)
            fig.update_traces(marker=dict(size=10))
            fig.update_traces(textposition='top left')  # Adjust marker size as needed
        
            # Plot chart on screen
            st.plotly_chart(fig)
        except Exception as e:
            st.error(f"Error generating plot: {e}")
    else:
        st.info("Upload data or add LCH values to generate plot.")
else:
    if not df.empty:
        try:
            L_values = df['L'].tolist()
            C_values = df['C'].tolist()
            H_values = df['H'].tolist()
            
            # Ensure 'Toner' column exists in the DataFrame
            Toners = df['Toner'].tolist() if 'Toner' in df.columns else [""] * len(df)
            
            # Define marker shapes based on 'Source' values if 'Source' column exists
            if 'Source' in df.columns:
                sources = df['Source'].tolist()
                unique_sources = list(set(sources))
                symbols = ['circle', 'square', 'diamond', 'cross', 'x', 'star', 'triangle-up', 'triangle-down']
                source_symbol_map = {source: symbols[i % len(symbols)] for i, source in enumerate(unique_sources)}
                marker_symbols = [source_symbol_map[source] for source in sources]
            else:
                marker_symbols = ['circle'] * len(df)

            df2 = lcm.plot_lch_colors(L_values, C_values, H_values)
            colours = [i for i in df2[1]]  # Extract color data from the result

            # Generate hover text
            hover_text = [f'L: {L}<br>C: {C}<br>H: {H}<br>Toner: {toner}'
                          for L, C, H, toner in zip(L_values, C_values, H_values, Toners)]

            # Create 3D scatter plot
            fig = go.Figure(data=[go.Scatter3d(
                x=C_values,
                y=H_values,
                z=L_values,
                mode='markers',
                marker=dict(
                    size=7,
                    color=colours,
                    opacity=0.8,
                    symbol=marker_symbols  # Set marker symbols based on source
                ),
                text=hover_text,
                hoverinfo='text'
            )])

            # Update layout
            fig.update_layout(
                scene=dict(
                    xaxis_title='Chroma (C)',
                    yaxis_title='Hue (H)',
                    zaxis_title='Lightness (L)',
                ),
                margin=dict(l=0, r=0, b=0, t=0)
            )

            st.plotly_chart(fig)
        except Exception as e:
            st.error(f"Error generating 3D plot: {e}")
    else:
        st.info("Upload data or add LCH values to generate plot.")
