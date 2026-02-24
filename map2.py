import pandas as pd
import folium

# قراءة الملف
df = pd.read_excel("loc2.xlsx")
df.columns = df.columns.str.strip().str.lower()
df['building'] = df['building'].astype(str).str.strip().str.lower()

# تحويل الإحداثيات لأرقام
df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')

# ✅ عكس الأعمدة لأن الملف كان مقلوبًا
#df[['latitude', 'longitude']] = df[['longitude', 'latitude']]

# حذف الصفوف غير الصالحة
df = df.dropna(subset=['latitude', 'longitude'])

# خريطة الألوان حسب نوع المبنى
color_map = {
    'apartments': 'purple',
    'schools': 'blue',
    'banks': 'green',
    'hotels': 'orange',
    'hospital': 'red',
    'industry': 'gray'
}

# إنشاء الخريطة
m = folium.Map(location=[31.26, 32.29], zoom_start=13)

# إضافة النقاط بأيقونات ملونة
for _, row in df.iterrows():
    btype = row['building']
    color = color_map.get(btype, 'darkblue')  # لون افتراضي لو النوع غير موجود

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

# حفظ الخريطة
m.save("colored_map.html")
print("تم حفظ الخريطة باسم colored_icon_map.html")
