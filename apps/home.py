from time import sleep
import streamlit as st
import leafmap as leafmap
import pandas as pd

def handle_input(m):
    rt_state = st.session_state.us_state
        
    if (rt_state == 'Florida'):
        df = pd.read_csv("disaster_data_fl.csv")
        m.add_points_from_xy(df, 'gps_lon', 'gps_lat', ['uuid','gps_lon','gps_lat','state','damage_label','url'])
        m.set_center(-81.5157, 27.6648, 7)

    elif (rt_state == 'North Carolina'):
        df = pd.read_csv("disaster_data_nc.csv")
        m.add_points_from_xy(df, 'gps_lon', 'gps_lat', ['uuid','gps_lon','gps_lat','state','damage_label','url'])
        m.set_center(-79.0193, 35.7595, 7)

    elif (rt_state == 'Puerto Rico'):
        for j in [1,2,3]:
            if (j == int(1)):
                m.set_center(-66.5901, 18.2208, 10)
                #m.to_streamlit(height=700)

            elif (j == int(2)):
                sleep(30)
                #filename = "disaster_data_pr_%i.csv" %j
                #m.add_xy_data(filename, 'gps_lon', 'gps_lat', layer_name='layer1')
                df = pd.read_csv("disaster_data_pr_%i.csv" %j)
                m.add_points_from_xy(df, 'gps_lon', 'gps_lat', ['uuid','gps_lon','gps_lat','state','damage_label','url'], layer_name='layer1')
                #m.to_streamlit(height=700)

            elif (j == int(3)):
                sleep(30)
                #filename = "disaster_data_pr_%i.csv" %j
                #m.add_xy_data(filename, 'gps_lon', 'gps_lat', layer_name='layer2')
                df = pd.read_csv("disaster_data_pr_%i.csv" %j)
                m.add_points_from_xy(df, 'gps_lon', 'gps_lat', ['uuid','gps_lon','gps_lat','state','damage_label','url'], layer_name='layer2')
                #m.to_streamlit(height=700)

            m.to_streamlit(height=700)

    else:
        #df = pd.read_csv("disaster_data_sorted.csv")
        #m.add_points_from_xy(df, 'gps_lon', 'gps_lat', ['uuid','gps_lon','gps_lat','state','damage_label','url'])
        m.set_center(-95.7129, 37.0902, 5)
        m.to_streamlit(height=700)
        #m.to_streamlit(height=700)
    #m.to_streamlit(height=700)



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

    #m.set_center(-95.7129, 37.0902, 5)
    #m.to_streamlit(height=700)
    #m = leafmap.Map(locate_control=True)
    #m.set_center(-95.7129, 37.0902, 5)
    #m.to_streamlit(height=700)
