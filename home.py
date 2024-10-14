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

col1, col2 = st.columns([4,1])
point_layer = pydeck.Layer(
    "ScreenGridLayer",
    data=df_old,
    id="id",
    get_position=["lng", "lat"],
    get_color="[255, 75, 75]",
    pickable=True,
    auto_highlight=True,
    get_radius="aantal*100",
)

view_state = pydeck.ViewState(
    latitude=df_old.lat.mean(), longitude=df_old.lng.mean(), controller=True, zoom=2.4, pitch=30
)

chart = pydeck.Deck(
    point_layer,
    initial_view_state=view_state,
    tooltip={"text": "{project}"},
)

with tab2:
    woth col1:
        event = st.pydeck_chart(chart, on_select="rerun", selection_mode="singlev-object")
    
    with col2:
        event.selection
