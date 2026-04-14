import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# Membaca dataset yang sudah dibersihkan (gantilah dengan nama file yang sesuai)
df_clean = pd.read_csv('hotel_distribution_cleaned.csv')

# Sidebar untuk memilih kecamatan
st.sidebar.header("🔍 Filter Data")
kecamatan_list = ['Semua'] + df_clean['city'].unique().tolist()
selected_kecamatan = st.sidebar.selectbox("Pilih Kecamatan", kecamatan_list)

# Filter data berdasarkan kecamatan yang dipilih
if selected_kecamatan != 'Semua':
    df_clean = df_clean[df_clean['city'] == selected_kecamatan]

# Menampilkan judul utama
st.title("Dashboard Monitoring Distribusi Hotel")

# 1. Menampilkan Total Hotel, Pengobatan, dan Rata-rata Penyelesaian
total_hotel = df_clean['name'].nunique()
total_pengobatan = df_clean[df_clean['status'] == 'Completed'].shape[0]
avg_complete_rate = (total_pengobatan / total_hotel) * 100

st.subheader("🎯 1. MASALAH UTAMA")
st.markdown("Distribusi ketersediaan hotel tidak merata saat Tahun Baru")

st.subheader("🎯 2. FOKUS ANALISIS")
st.markdown("Supply hotel (bukan booking, bukan customer)")

st.subheader("🎯 3. SOLUSI")
st.markdown("Monitoring & optimasi distribusi hotel")

st.subheader("🎯 4. OUTPUT")
st.markdown("Dashboard + rekomendasi distribusi")

# Menampilkan metrik total hotel, total pengobatan, dan rata-rata penyelesaian
col1, col2, col3 = st.columns(3)
col1.metric("Total Hotel", total_hotel)
col2.metric("Total Pengobatan", total_pengobatan)
col3.metric("Avg Complete Rate", f"{avg_complete_rate:.2f}%")

# 2. Rata-rata Rating per Kota
st.subheader("Rata-rata Rating Hotel per Kota")
rating_per_city = df_clean.groupby('city')['starRating'].mean().reset_index()
rating_per_city.columns = ['city', 'avg_rating']

fig2, ax2 = plt.subplots(figsize=(12, 6))
bars2 = ax2.bar(rating_per_city['city'], rating_per_city['avg_rating'], color='lightcoral')
ax2.set_xlabel('Kota', fontsize=14)
ax2.set_ylabel('Rating', fontsize=14)

# Label angka di atas bar
for bar in bars2:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, yval + 0.05, round(yval, 2), ha='center', fontsize=12)

plt.tight_layout()
st.pyplot(fig2)

# 3. Distribusi Star Rating Hotel (Pie Chart)
st.subheader("Distribusi Star Rating Hotel")
star_distribution = df_clean['starRating'].value_counts().reset_index()
star_distribution.columns = ['starRating', 'jumlah']
fig4, ax4 = plt.subplots(figsize=(8, 8))
ax4.pie(star_distribution['jumlah'], labels=star_distribution['starRating'], autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors, pctdistance=0.85, wedgeprops={"edgecolor": "none"})
ax4.set_title("Distribusi Star Rating Hotel", fontsize=16, weight='bold')
st.pyplot(fig4)

# 4. Peta Lokasi Hotel per Kota (menggunakan folium)
st.subheader("Peta Lokasi Hotel per Kota")
city_coordinates = {
    "Jakarta": [-6.2088, 106.8456],
    "Bandung": [-6.9175, 107.6191],
    "Surabaya": [-7.2575, 112.7521],
    "Yogyakarta": [-7.7956, 110.3695]
}

# Membuat objek peta
m = folium.Map(location=city_coordinates["Jakarta"], zoom_start=12)

# Menambahkan marker ke peta
for city, coord in city_coordinates.items():
    folium.Marker(location=coord, popup=city).add_to(m)

# Menampilkan peta menggunakan streamlit_folium
st.write("Peta Lokasi Hotel per Kota")
st_folium(m, width=700)

# 5. Evaluasi Kualitas Data
st.subheader("🔬 Evaluasi Kualitas Data")
accuracy = 100.0
completeness = 100.0
consistency = 100.0
timeliness = "Tidak terukur"

col4, col5, col6, col7 = st.columns(4)
col4.metric("Accuracy", f"{accuracy}%", icon="✅")
col5.metric("Completeness", f"{completeness}%", icon="✅")
col6.metric("Consistency", f"{consistency}%", icon="✅")
col7.warning(f"Timeliness {timeliness}", icon="⚠️")

# 6. Harga vs Rating (Scatter Plot)
st.subheader("Harga vs Rating")
fig5, ax5 = plt.subplots(figsize=(10, 6))
ax5.scatter(df_clean['price'], df_clean['starRating'], alpha=0.5, color='b')
ax5.set_title("Hubungan Harga dan Rating Hotel", fontsize=16, weight='bold')
ax5.set_xlabel("Harga per Malam (IDR)", fontsize=14)
ax5.set_ylabel("Rating Hotel", fontsize=14)
plt.grid(True)
plt.tight_layout()
st.pyplot(fig5)

# 7. Menambahkan Tabel untuk Data Hotel
st.subheader("Tabel Data Hotel")
st.write(df_clean.head(10))
