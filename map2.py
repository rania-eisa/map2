import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

st.title("خريطة المباني")

# ----------------------------------
# قراءة الملف
# ----------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("loc2.xlsx")
    df.columns = df.columns.str.strip().str.lower()
    df['building'] = df['building'].astype(str).str.strip().str.lower()

    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')

    df = df.dropna(subset=['latitude', 'longitude'])
    return df

df = load_data()

st.write("عدد النقاط:", len(df))

# ----------------------------------
# خريطة الألوان
# ----------------------------------
color_map = {
    'apartments': 'purple',
    'schools': 'blue',
    'banks': 'green',
    'hotels': 'orange',
    'hospital': 'red',
    'industry': 'gray'
}

# ----------------------------------
# إنشاء الخريطة
# ----------------------------------
m = folium.Map(location=[31.26, 32.29], zoom_start=13)

for _, row in df.iterrows():
    btype = row['building']
    color = color_map.get(btype, 'darkblue')

    popup_info = f"""
    <strong>Type:</strong> {row['building']}<br>
    <strong>LCLid:</strong> {row['lclid']}<br>
    <strong>District:</strong> {row['district']}<br>
    <strong>Latitude:</strong> {row['latitude']}<br>
    <strong>Longitude:</strong> {row['longitude']}
    """

    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=popup_info,
        tooltip=btype,
        icon=folium.Icon(color=color, icon='info-sign')
    ).add_to(m)

# ----------------------------------
# عرض الخريطة داخل Streamlit
# ----------------------------------
st_folium(m, width=1200, height=600)