import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random

import folium
from folium.plugins import Draw, Fullscreen, LocateControl, GroupedLayerControl
from streamlit_folium import st_folium
import datetime
from datetime import datetime, timedelta, date
import random

import ast

from credentials import *



# ---LAYOUT---



def logIn():
    name = st.text_input("Vul uw gebruikersnaam in, alstublieft",value=None)  
    password = st.text_input("Vul uw wachtwoord in, alstublieft")
    try:
        if name == None:
            st.stop()
        
        index = df_references[df_references['username']==name].index[0]
        true_password = df_references.loc[index,"password"]

    except:
        st.warning("De gebruikersnaam is niet correct.")
        st.stop()
                             
    if st.button("logIn"):
        if password == true_password:
            st.session_state.login = {"name": name, "password": password}
            st.rerun()

        else:
            st.markdown(f"Sorry {name.split()[0]}, het wachtwoord is niet correct.")

def project():
    st.subheader(f"Welkom {st.session_state.login['name'].split()[0]}!!",divider='grey')
    index_project = df_references[df_references['username']==st.session_state.login["name"]].index[0]
    project_list = df_references.loc[index_project,"project"].split(',')
    project = st.selectbox("Aan welke project ga je werken?",project_list,label_visibility="visible")
    opdracht = st.selectbox("Aan welke opdracht ga je werken?",DICTIONARY_PROJECTS[project],label_visibility="visible")
    if st.button("begin"):
         st.session_state.project = {"project_name": project,"opdracht": opdracht}
         st.rerun()
        
def logOut():
    if st.button("logOut",use_container_width=True):
        del st.session_state.login
        del st.session_state.project     
        st.rerun()

def logOut_project():
    if st.button("Opdracht wijzigen",use_container_width=True):
        del st.session_state.project
        st.rerun()
        
#---DATASET---
ttl = '10m'
ttl_references = '10m'
conn = st.connection("gsheets", type=GSheetsConnection)
df_point = conn.read(ttl=ttl,worksheet="df_observations")
df_references = conn.read(ttl=ttl_references,worksheet="df_users")

#--- APP ---

if "login" not in st.session_state:
    logIn()
    st.stop()


if 'project' not in st.session_state:  
    project()
    st.stop()




with st.sidebar:
    logOut_project()
    logOut()
    st.divider()




create_page = st.Page("home.py", title="Home", icon=":material/add_circle:")
delete_page = st.Page("pages/✍️_Voeg_een_waarneming_in.py", title="Entry", icon=":material/delete:")

pg = st.navigation([create_page, delete_page])
st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()

# try:
#     try:
#         if st.session_state.project['project_name'] != 'Admin':
#             df_2 = df_point[df_point['project']==st.session_state.project['project_name']]
#             df_2 = df_2[df_2['soortgroup']==st.session_state.project['opdracht']]
    
#         else:
#             df_2 = df_point[df_point['soortgroup']==st.session_state.project['opdracht']]
    
        
#         df_2["datum"] = pd.to_datetime(df_2["datum"]).dt.date
    
    
#         st.sidebar.subheader("Filter op",divider=False)
#         d = st.sidebar.slider("Datum", min_value=df_2.datum.min(),max_value=df_2.datum.max(),value=(df_2.datum.min(), df_2.datum.max()),format="DD-MM-YYYY")
        
#         df_2 = df_2[(df_2['datum']>=d[0]) & (df_2['datum']<=d[1])]
#     except:
#         pass
        
#     if st.session_state.project['opdracht'] in ["Vleermuizen","Vogels"]:
#         species_filter_option = df_2["sp"].unique()
#         species_filter = st.sidebar.multiselect("Sorten",species_filter_option,species_filter_option)
#         df_2 = df_2[df_2['sp'].isin(species_filter)]

#     st.sidebar.divider()
    
#     df_2["icon_data"] = df_2.apply(lambda x: None if x["geometry_type"] in ["LineString","Polygon"] 
#                                    else (icon_dictionary[x["soortgroup"]][x["sp"]][x["functie"]] if x["soortgroup"] in ['Vogels','Vleermuizen'] 
#                                          else icon_dictionary[x["soortgroup"]][x["functie"]]), 
#                                    axis=1)
    
#     df_2 = df_2.reset_index(drop=True)
    
#     map = folium.Map(tiles=None)
#     LocateControl(auto_start=False,position="topleft").add_to(map)
#     Fullscreen(position="topleft").add_to(map)
    
#     functie_dictionary = {}
#     functie_len = df_2['functie'].unique()
    
#     for functie in functie_len:
#         functie_dictionary[functie] = folium.FeatureGroup(name=functie)    

#     # functie_dictionary["geometry"] = folium.FeatureGroup(name="geometry")
    
#     for feature_group in functie_dictionary.keys():
#         map.add_child(functie_dictionary[feature_group])

#     folium.TileLayer('OpenStreetMap',overlay=False,show=True,name="Streets").add_to(map)
#     folium.TileLayer(tiles="Cartodb Positron",overlay=False,show=False,name="Light").add_to(map)
#     folium.TileLayer('Cartodb dark_matter',overlay=False,show=False,name="Dark").add_to(map)
    
    
    
#     folium.LayerControl().add_to(map)    

    

#     # folium.GeoJson('geometries/map (6).geojson',
#     #               tooltip=folium.features.GeoJsonTooltip(
#     #      fields=['name'],
#     #      labels=False,
#     #      style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
#     #  )).add_to(functie_dictionary["geometry"])

#     for i in range(len(df_2)):

#         if df_2.iloc[i]['geometry_type'] == "Point":

#             if (df_2.iloc[i]['sp']=="Huismus") & (df_2.iloc[i]['functie'] in ["mogelijke nestlocatie","nestlocatie"]):
#                 ICON_SIZE_2 = ICON_SIZE_huismus

#             elif df_2.iloc[i]['functie'] == "Waarneming rat doorgegeven, geen actie op ondernomen":
#                 ICON_SIZE_2 = ICON_SIZE_rat_maybe

#             elif (df_2.iloc[i]['sp'] in ['Ruige dwergvleermuis', 'Laatvlieger','Rosse vleermuis','Meervleermuis','Watervleermuis']):
#                 ICON_SIZE_2 = ICON_SIZE_BAX_EXTRA

#             elif (df_2.iloc[i]['sp'] in ['...Andere(n)']):
#                 ICON_SIZE_2 = ICON_SIZE_ANDER

#             else:                
#                 ICON_SIZE_2 = ICON_SIZE
                

#             html = popup_html(i)
#             popup = folium.Popup(folium.Html(html, script=True), max_width=300)
#             fouctie_loop = functie_dictionary[df_2.iloc[i]['functie']]
    
#             folium.Marker([df_2.iloc[i]['lat'], df_2.iloc[i]['lng']],
#                           popup=popup,
#                           icon=folium.features.CustomIcon(df_2.iloc[i]["icon_data"], icon_size=ICON_SIZE_2)
#                          ).add_to(fouctie_loop)
                

#         # elif df_2.iloc[i]['geometry_type'] == "LineString":
#         #     # fouctie_loop = functie_dictionary[df_2.iloc[i]['functie']]
#         #     folium.PolyLine(df_2.iloc[i]['coordinates']).add_to(map)

#         elif df_2.iloc[i]['geometry_type'] == "Polygon":
#             html = popup_polygons(i)
#             popup = folium.Popup(folium.Html(html, script=True), max_width=300)
#             fouctie_loop = functie_dictionary[df_2.iloc[i]['functie']]
#             location = df_2.iloc[i]['coordinates']
#             location = ast.literal_eval(location)
#             location = [i[::-1] for i in location[0]]
                        
#             if df_2.iloc[i]['functie']=="Paringsgebied":
#                 fill_color="red"

#             else:
#                 fill_color="green"
                
#             folium.Polygon(location,fill_color=fill_color,weight=0,fill_opacity=0.5,
#                           popup=popup
#                           ).add_to(fouctie_loop)

    

#     output_2 = st_folium(map,returned_objects=["last_active_drawing"],width=OUTPUT_width, height=OUTPUT_height,
#                          feature_group_to_add=list(functie_dictionary.values()))
        
#     try:
#         try:
#             id = str(output_2["last_active_drawing"]['geometry']['coordinates'][0])+str(output_2["last_active_drawing"]['geometry']['coordinates'][1])
#             name = f"{id}"
#         except:
#             id = str(output_2["last_active_drawing"]['geometry']['coordinates'][0][0][0])+str(output_2["last_active_drawing"]['geometry']['coordinates'][0][0][1])
#             name = f"{id}"

#         with st.sidebar:
#             #---FOR THE PICTURE---
#             try:
#                 res = drive.get(name).read()                
#                 with st.expander("Zie media"):
#                     try:
#                         st.image(res)
#                     except:
#                         st.video(res)
#                 if st.button("Waarneming bijwerken",use_container_width=True):
#                     update_item()

#                 with st.form("entry_form", clear_on_submit=True,border=False):
#                     submitted = st.form_submit_button(":red[**Verwijder waarneming**]",use_container_width=True)
#                     if submitted:
#                         # if waarnemer ==  df_point.set_index("key").loc[id,"waarnemer"]:
#                         db.delete(id)
#                         drive.delete(name)
#                         st.success('Waarneming verwijderd', icon="✅")
#                         st.page_link("🗺️_Home.py", label="vernieuwen", icon="🔄",use_container_width=True)
#                             # else:
#                             #     st.warning('Je kunt deze observatie niet uitwissen. Een andere gebruiker heeft het gemarkeerd.', icon="⚠️")
#              #---FOR THE PICTURE---               
#             except:
#                 # st.info('Geen foto opgeslagen voor deze waarneming')

#                 if st.button("Waarneming bijwerken",use_container_width=True):
#                     update_item()

                
#                 with st.form("entry_form", clear_on_submit=True,border=False):
#                     submitted = st.form_submit_button(":red[**Verwijder waarneming**]",use_container_width=True)
#                     if submitted:
#                         df = conn.read(ttl=0,worksheet="df_observations")
#                         df_filter = df[df["key"]==id]
#                         df_drop = df[~df.apply(tuple, axis=1).isin(df_filter.apply(tuple, axis=1))]
#                         conn.update(worksheet='df_observations',data=df_drop)
#                         st.success('Waarneming verwijderd', icon="✅") 
#                         st.page_link("home.py", label="Vernieuwen", icon="🔄",use_container_width=True)

#     except:
#         st.stop()

# except:
#     st.image("https://media.istockphoto.com/photos/open-empty-cardboard-box-on-a-white-background-picture-id172167710?k=6&m=172167710&s=612x612&w=0&h=Z4fueCweh9q-X_VBRAPCYSalyaAnXG3ioErb8oJSVek=")
#     st.stop()
