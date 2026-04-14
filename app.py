import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# Membaca dataset yang sudah dibersihkan (gantilah dengan nama file yang sesuai)
df_clean = pd.read_csv('hotel_distribution_cleaned.csv')

# Menampilkan judul utama
st.title("Dashboard Monitoring Distribusi Hotel")

# Menambahkan filter data menggunakan Sidebar
kecamatan = st.sidebar.selectbox("Pilih Kecamatan", df_clean['city'].unique())
df_filtered = df_clean[df_clean['city'] == kecamatan]

# Tampilkan data yang sudah difilter
st.write(f"Data Hotel di Kecamatan {kecamatan}")
st.dataframe(df_filtered)

# 1. Jumlah Hotel per Kota
st.subheader("Jumlah Hotel per Kota")
hotel_per_city = df_clean.groupby('city')['name'].nunique().reset_index()
hotel_per_city.columns = ['city', 'total_hotel']

fig1, ax1 = plt.subplots(figsize=(12, 6))
ax1.bar(hotel_per_city['city'], hotel_per_city['total_hotel'], color='dodgerblue')
ax1.set_xlabel('Kota', fontsize=14)
ax1.set_ylabel('Jumlah Hotel', fontsize=14)
ax1.set_xticklabels(hotel_per_city['city'], rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig1)

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

# 3. Rata-rata Harga per Kota
st.subheader("Rata-rata Harga Hotel per Kota (IDR)")
price_per_city = df_clean.groupby('city')['price'].mean().reset_index()
price_per_city.columns = ['city', 'avg_price']

fig3, ax3 = plt.subplots(figsize=(12, 6))
bars3 = ax3.bar(price_per_city['city'], price_per_city['avg_price'], color='mediumseagreen')
ax3.set_xlabel('Kota', fontsize=14)
ax3.set_ylabel('Harga', fontsize=14)

# Label harga di atas bar
for bar in bars3:
    yval = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2, yval + 50000, f'{int(yval):,}', ha='center', fontsize=12)

plt.tight_layout()
st.pyplot(fig3)

# 4. Distribusi Star Rating Hotel (Pie Chart)
st.subheader("Distribusi Star Rating Hotel")
star_distribution = df_clean['starRating'].value_counts().reset_index()
star_distribution.columns = ['starRating', 'jumlah']
fig4, ax4 = plt.subplots(figsize=(8, 8))
ax4.pie(star_distribution['jumlah'], labels=star_distribution['starRating'], autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors, pctdistance=0.85, wedgeprops={"edgecolor": "none"})
ax4.set_title("Distribusi Star Rating Hotel", fontsize=16, weight='bold')
st.pyplot(fig4)

# 5. Peta Lokasi Hotel per Kota (menggunakan folium)
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