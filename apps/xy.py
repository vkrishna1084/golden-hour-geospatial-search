import leafmap.foliumap as leafmap
import pandas as pd
import streamlit as st



def find_state(input_txt):
    us_state = ''
    if 'alaska' in input_txt.lower(): us_state = 'Alaska'
    elif 'alabama' in input_txt.lower(): us_state = 'Alabama'
    elif 'arkansas' in input_txt.lower(): us_state = 'Arkansas'
    elif 'arizona' in input_txt.lower(): us_state = 'Arizona'
    elif 'california' in input_txt.lower(): us_state = 'California'
    elif 'colorado' in input_txt.lower(): us_state = 'Colorado'
    elif 'connecticut' in input_txt.lower(): us_state = 'Connecticut'
    elif 'washington dc' in input_txt.lower(): us_state = 'District of Columbia'
    elif 'delaware' in input_txt.lower(): us_state = 'Delaware'
    elif 'florida' in input_txt.lower(): us_state = 'Florida'
    elif 'georgia' in input_txt.lower(): us_state = 'Georgia'
    elif 'hawaii' in input_txt.lower(): us_state = 'Hawaii'
    elif 'iowa' in input_txt.lower(): us_state = 'Iowa'
    elif 'idaho' in input_txt.lower(): us_state = 'Idaho'
    elif 'illinois' in input_txt.lower(): us_state = 'Illinois'
    elif 'indiana' in input_txt.lower(): us_state = 'Indiana'
    elif 'kansas' in input_txt.lower(): us_state = 'Kansas'
    elif 'kentucky' in input_txt.lower(): us_state = 'Kentucky'
    elif 'louisiana' in input_txt.lower(): us_state = 'Louisiana'
    elif 'massachusetts' in input_txt.lower(): us_state = 'Massachusetts'
    elif 'maryland' in input_txt.lower(): us_state = 'Maryland'
    elif 'maine' in input_txt.lower(): us_state = 'Maine'
    elif 'michigan' in input_txt.lower(): us_state = 'Michigan'
    elif 'minnesota' in input_txt.lower(): us_state = 'Minnesota'
    elif 'missouri' in input_txt.lower(): us_state = 'Missouri'
    elif 'mississippi' in input_txt.lower(): us_state = 'Mississippi'
    elif 'montana' in input_txt.lower(): us_state = 'Montana'
    elif 'north carolina' in input_txt.lower(): us_state = 'North Carolina'
    elif 'north dakota' in input_txt.lower(): us_state = 'North Dakota'
    elif 'nebraska' in input_txt.lower(): us_state = 'Nebraska'
    elif 'new hampshire' in input_txt.lower(): us_state = 'New Hampshire'
    elif 'new jersey' in input_txt.lower(): us_state = 'New Jersey'
    elif 'new mexico' in input_txt.lower(): us_state = 'New Mexico'
    elif 'nevada' in input_txt.lower(): us_state = 'Nevada'
    elif 'new york' in input_txt.lower(): us_state = 'New York'
    elif 'ohio' in input_txt.lower(): us_state = 'Ohio'
    elif 'oklahoma' in input_txt.lower(): us_state = 'Oklahoma'
    elif 'oregon' in input_txt.lower(): us_state = 'Oregon'    
    elif 'pennsylvania' in input_txt.lower(): us_state = 'Pennsylvania'
    elif 'puerto rico' in input_txt.lower(): us_state = 'Puerto Rico'
    elif 'rhode island' in input_txt.lower(): us_state = 'Rhode Island'
    elif 'south carolina' in input_txt.lower(): us_state = 'South Carolina'
    elif 'south dakota' in input_txt.lower(): us_state = 'South Dakota'
    elif 'tennessee' in input_txt.lower(): us_state = 'Tennessee'
    elif 'texas' in input_txt.lower(): us_state = 'Texas'
    elif 'utah' in input_txt.lower(): us_state = 'Utah'    
    elif 'virginia' in input_txt.lower(): us_state = 'Virginia'
    elif 'vermont' in input_txt.lower(): us_state = 'Vermont'
    elif 'washington' in input_txt.lower(): us_state = 'Washington'
    elif 'wisconsin' in input_txt.lower(): us_state = 'Wisconsin'
    elif 'west virginia' in input_txt.lower(): us_state = 'West Virginia'
    elif 'wyoming' in input_txt.lower(): us_state = 'Wyoming'
    return us_state

def find_damage(input_txt):
    dmg = ''
    if 'flooding' in input_txt.lower(): dmg = 'flooding'
    elif 'flooding_fire' in input_txt.lower(): dmg = 'flooding_fire'
    elif 'landslide' in input_txt.lower(): dmg = 'landslide'
    elif 'rubble' in input_txt.lower(): dmg = 'landslide_rubble'
    elif 'fire' in input_txt.lower(): dmg = 'fire'
    return dmg

def handle_input(m):
    input = st.session_state.input

    if input:
        state = find_state(st.session_state.input)
        damage = find_damage(st.session_state.input)

        df = pd.read_csv("disaster_data_sorted.csv")
        usdf = pd.read_csv("us_states_lat_lon.csv")

        if state:
            sdf = df[df['state']==state]
            gps_df = usdf[usdf['name']==state]
            m.set_center(gps_df['longitude'].values[0], gps_df['latitude'].values[0], 7)
            #m.set_center(-79.0193, 35.7595, 7)
        else:
            sdf = df

        if damage:
            mdf = sdf[sdf['damage_label']==damage]
        else:
            mdf = sdf

        m.add_points_from_xy(mdf, 'gps_lon', 'gps_lat', ['uuid','gps_lon','gps_lat','state','damage_label','url'])

    else:
        m.set_center(-95.7129, 37.0902, 5)

    m.to_streamlit(height=700)

'''
        if (state == 'Florida'):
            df = pd.read_csv("disaster_data_fl.csv")
            #damage = find_damage(st.session_state.input)
            if damage: 
                sort_df = df[df['damage_label']==damage]
            else:
                sort_df = df
            m.add_points_from_xy(sort_df, 'gps_lon', 'gps_lat', ['uuid','gps_lon','gps_lat','state','damage_label','url'])
            m.set_center(-81.5157, 27.6648, 7)

        elif (state == 'North Carolina'):
            df = pd.read_csv("disaster_data_nc.csv")
            #damage = find_damage(st.session_state.input)
            if damage: 
                sort_df = df[df['damage_label']==damage]
            else:
                sort_df = df
            m.add_points_from_xy(sort_df, 'gps_lon', 'gps_lat', ['uuid','gps_lon','gps_lat','state','damage_label','url'])
            m.set_center(-79.0193, 35.7595, 7)

        elif (state == 'Puerto Rico'):
            df = pd.read_csv("disaster_data_pr.csv")
            #damage = find_damage(st.session_state.input)
            if damage: 
                sort_df = df[df['damage_label']==damage]
            else:
                sort_df = df
            m.add_points_from_xy(sort_df, 'gps_lon', 'gps_lat', ['uuid','gps_lon','gps_lat','state','damage_label','url'])
            m.set_center(-66.5901, 18.2208, 10)

        else:
            df = pd.read_csv("disaster_data_sorted.csv")
            m.add_points_from_xy(df, 'gps_lon', 'gps_lat', ['uuid','gps_lon','gps_lat','state','damage_label','url'])
            m.set_center(-95.7129, 37.0902, 5)
            
        m.to_streamlit(height=700)
'''

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

    

    '''
    if srch_ip:
        df = pd.read_csv("disaster_data.csv")
        m.add_points_from_xy(df, 'gps_lon', 'gps_lat', ['uuid','gps_lon','gps_lat','state','Answer','s3_path','url'])
        m.to_streamlit(height=700)
    

    
    if url:

        try:
            df = pd.read_csv(url)

            columns = df.columns.values.tolist()
            row1_col1, row1_col2, row1_col3, row1_col4, row1_col5 = st.columns(
                [1, 1, 3, 1, 1]
            )

            lon_index = 0
            lat_index = 0

            for col in columns:
                if col.lower() in ["lon", "longitude", "long", "lng"]:
                    lon_index = columns.index(col)
                elif col.lower() in ["lat", "latitude"]:
                    lat_index = columns.index(col)

            with row1_col1:
                x = st.selectbox("Select longitude column", columns, lon_index)

            with row1_col2:
                y = st.selectbox("Select latitude column", columns, lat_index)

            with row1_col3:
                popups = st.multiselect("Select popup columns", columns, columns)

            with row1_col4:
                heatmap = st.checkbox("Add heatmap")

            if heatmap:
                with row1_col5:
                    if "pop_max" in columns:
                        index = columns.index("pop_max")
                    else:
                        index = 0
                    heatmap_col = st.selectbox("Select heatmap column", columns, index)
                    try:
                        m.add_heatmap(df, y, x, heatmap_col)
                    except:
                        st.error("Please select a numeric column")

            try:
                m.add_points_from_xy(df, x, y, popups)
            except:
                st.error("Please select a numeric column")

        except Exception as e:
            st.error(e)

    
    m = leafmap.Map(locate_control=True)
    m.add_basemap("ROADMAP")

    m.to_streamlit(height=700)
    '''