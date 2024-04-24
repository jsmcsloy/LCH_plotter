import streamlit as st 
import pandas as pd
import plotly.express as px

st.title("Simple plotter for LCH values")

# Side bar - capture L, C, H and insert into dataframe
L = st.sidebar.number_input("Enter L value", value=50)
C = st.sidebar.number_input("Enter C value", value=50)
H = st.sidebar.number_input("Enter H value", value=180)

# Button to add LCH values into a list
if 'data_list' not in st.session_state:
    st.session_state.data_list = []

if st.sidebar.button("Add LCH value"):
    st.session_state.data_list.append({'L': L, 'C': C, 'H': H})
    st.sidebar.success("Added: L={}, C={}, H={}".format(L, C, H))

# Load CSV of data points
data_file = st.sidebar.file_uploader("Load in the CSV file...")

if data_file is not None:
    df = pd.read_csv(data_file)
    if 'Name' not in df.columns:
        st.error("CSV must contain a 'Name' column.")
else:
    # If no file uploaded yet, use accumulated data
    df = pd.DataFrame(st.session_state.data_list)

# Plotting only if dataframe is not empty
if not df.empty:
    try:
        # Plot with names always visible
        fig = px.scatter_polar(df, r="C", theta="H", direction='counterclockwise', start_angle=0,
                               text="Name",  # assuming 'Name' is the column with labels
                               hover_data=df.columns)  # dynamically include all columns in hover data
        fig.update_traces(textposition='top center')
        fig.update_layout(
            polar=dict(
                radialaxis=dict(showticklabels=False)  # Hides the radial axis tick labels
            ),
            hoverlabel=dict(bgcolor="white", font_size=12, font_family="Rockwell")
        )
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Error generating plot: {e}")
else:
    st.info("Upload data or add LCH values to generate plot.")
