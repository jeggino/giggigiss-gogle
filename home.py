import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from streamlit_option_menu import option_menu  
from datetime import datetime as dt
import random
from dateutil import parser

tab1, tab2 = st.tabs(["Dataframe", "Map"])

conn = st.connection("gsheets", type=GSheetsConnection)
df_old = conn.read(ttl=0,worksheet="df_observations")

with tab1:
    df_old


import streamlit as st
import pydeck
import pandas as pd



ICON_URL = "https://static.vecteezy.com/system/resources/previews/014/488/954/original/location-pin-collection-red-pointer-icon-for-pin-on-the-map-to-show-the-location-png.png"

icon_data = {
    "url": ICON_URL,
    "width": 50,
    "height": 50,
    "anchorY": 242,
}

df_old["icon_data"] = None
for i in df_old.index:
    df_old["icon_data"][i] = icon_data

point_layer = pydeck.Layer(
    "IconLayer",
    data=df_old,
    id="id",
    get_position=["lng", "lat"],
    get_icon="icon_data",
    pickable=True,
    size_scale=1,
    get_size="aantal",
)

view_state = pydeck.ViewState(
    latitude=df_old.lat.mean(), longitude=df_old.lng.mean(), controller=True, zoom=8, pitch=30,map_style='light',
)

chart = pydeck.Deck(
    point_layer,
    initial_view_state=view_state,
    tooltip={"text": "{project}"},
)

with tab2:
    col1, col2 = st.columns([2,1])
    with col1:
        event = st.pydeck_chart(chart, on_select="rerun", selection_mode="single-object")
    
    with col2:
        try:
            table = pd.DataFrame(event.selection['objects']['id']).T.rename(columns={0:"Entry"})
            st.dataframe(table, use_container_width=True)

        except:
            st.info("select a point")

