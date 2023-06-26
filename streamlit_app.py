import streamlit as st
from streamlit_option_menu import option_menu
from apps import home, xy  # import your app modules here

if 'input' not in st.session_state:
    st.session_state.input = ''

if 'us_state' not in st.session_state:
    st.session_state.us_state = ''

st.set_page_config(page_title="Streamlit Geospatial", layout="wide")

# A dictionary of apps in the format of {"App title": "App icon"}
# More icons can be found here: https://icons.getbootstrap.com

apps = [
    {"func": xy.app, "title": "Geospatial Search", "icon": "map"},
    {"func": home.app, "title": "Real Time Dashboard", "icon": "map"},
]

titles = [app["title"] for app in apps]
titles_lower = [title.lower() for title in titles]
icons = [app["icon"] for app in apps]

params = st.experimental_get_query_params()

if "page" in params:
    default_index = int(titles_lower.index(params["page"][0].lower()))
else:
    default_index = 0

with st.sidebar:
    selected = option_menu(
        "Main Menu",
        options=titles,
        icons=icons,
        menu_icon="cast",
        default_index=default_index,
    )
    
    st.sidebar.title("Tech Stack")
    st.sidebar.info(
        """
        AWS: End-to-End solution\n
        Pinecone: Indexing and Searching \n
        Open AI: Semantic Processing\n
        Hugging Face: Transformer Architecture\n
        LangChain: Prompt Engineering\n
        Streamlit: Interactive User Interface\n
    """
    )
    

for app in apps:
    if app["title"] == selected:
        app["func"]()
        break
