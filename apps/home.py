from time import sleep
import streamlit as st
import leafmap as leafmap
import pandas as pd

def handle_input(m):
    rt_state = st.session_state.us_state
    
    while True:
        srch_res = api.call(rt_state, st.session_state['session_id'])
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
    st.title("Real Time Disaster Image Annotation")

    st.write(
        """
    Real time annotation of the disaster images will be shown in this dashboard. Please select the State from the drop down menu\n
    """
    )

    m = leafmap.Map()
    states_df = pd.read_csv("us_states_lat_lon.csv")
    us_states = states_df['name']

    st.session_state.us_state = st.selectbox("Select State", us_states, on_change=handle_input(m))
