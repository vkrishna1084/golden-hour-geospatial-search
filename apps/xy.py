import leafmap.foliumap as leafmap
import pandas as pd
import streamlit as st
import api
import json


def handle_input(m):
    input = st.session_state.input
    srch_res = api.call(input, st.session_state['session_id'])
    srch_df = pd.DataFrame(srch_res)
    usdf = pd.read_csv("us_states_lat_lon.csv")

    state = srch_df['state'].values[0]

    if state:
        gps_df = usdf[usdf['name']==state]
        m.set_center(gps_df['longitude'].values[0], gps_df['latitude'].values[0], 7)

    else:
        m.set_center(-95.7129, 37.0902, 5)

    m.add_points_from_xy(srch_df, 'gps_lon', 'gps_lat', ['uuid','gps_lon','gps_lat','state','damage_label','url'])
    m.to_streamlit(height=700)


def app():

    st.title("Geospatial Search")

    st.write(
        """
    Advanced state of the art Geospatial Search for disaster images with natural language prompt powered by Large Language Models. Search the image catalog by specifying the type of damage and the place you wanted to search\n
    Example: Give me the flooding damage disaster images in Florida state
    """
    )

    m = leafmap.Map(locate_control=True, plugin_LatLngPopup=False)
    #m.add_basemap("ROADMAP")
    


    #sample_query = "Give me the flooding damage disaster images in Florida state"
    input = st.text_input("Enter your query here:", key="input", on_change=handle_input(m))
    #m.to_streamlit(height=700)
