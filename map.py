import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import Draw, MarkerCluster, Fullscreen
from folium import Marker
import pandas as pd
import os

# Display App Structure
st.title("통근버스 이용자 지도")

office_df = pd.read_json('office.json')
data = pd.read_json('data.json')

office = st.sidebar.selectbox("근무지", office_df.loc[:, "근무지"], key="office")
format = st.sidebar.selectbox("포맷", ["Cluster", "Marker"], key="format")

lat = office_df.loc[office_df["근무지"]==office,"lat"].values[0]
lng = office_df.loc[office_df["근무지"]==office,"lng"].values[0]

# Display Map

m = folium.Map(
    location = ( lat, lng ),
    control_scale=True,
    zoom_start=11
)
Marker(location=[lat, lng], popup=office).add_to(m)
Draw(export=True).add_to(m)
mc = MarkerCluster()
Fullscreen().add_to(m)

for idx, row in data.loc[data["근무지"]==office, :].iterrows():
    if format == "Marker":
        Marker(location=[row["lat"], row["lng"]],
                icon=folium.Icon(color='purple', icon='home')
                ).add_to(m)
    elif format == "Cluster":
        mc.add_child(
            Marker(location=[row["lat"], row["lng"]],
            icon=folium.Icon(color='purple', icon='home')
                )
        )
        m.add_child(mc)

# st.components.v1.html(folium.Figure().add_child(m).render())
folium_static(m, width=1200, height=800)

# Download Map HTML file
output_dir = "maps"  # Customized directory
os.makedirs(output_dir, exist_ok=True)

html_file_path = os.path.join(output_dir, "map.html")
m.save(html_file_path)

try:
    with open(html_file_path, "rb") as file:
        file_data = file.read()
    st.download_button(
        label="Download Map as HTML",
        data=file_data,
        file_name="map.html",  # Default download name
        mime="text/html",  # Specify the MIME type
    )
except FileNotFoundError:
    st.error("The map file could not be found.")
