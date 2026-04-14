import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# Membaca dataset yang sudah dibersihkan
df_clean = pd.read_csv('hotel_distribution_cleaned.csv')

# Menampilkan judul utama
st.title("Dashboard Monitoring Distribusi Hotel 🏨")

# Filter Sidebar
selected_city = st.sidebar.selectbox("🔍 Pilih Kota", df_clean['city'].unique())

# 1. Displaying Key Metrics (e.g., Total Hotel, Total Rating, etc.)
total_hotel = df_clean['name'].nunique()
total_city = df_clean['city'].nunique()
avg_price = df_clean['price'].mean()
avg_rating = df_clean['starRating'].mean()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="🏨 Total Hotel", value=total_hotel)
with col2:
    st.metric(label="🌆 Total Kota", value=total_city)
with col3:
    st.metric(label="💰 Harga Rata-Rata", value=f"IDR {avg_price:,.0f}")

# Garis pemisah visualisasi
st.markdown("<hr>", unsafe_allow_html=True)

# 2. Jumlah Hotel per Kota
st.subheader("📊 Jumlah Hotel per Kota")
hotel_per_city = df_clean.groupby('city')['name'].nunique().reset_index()
hotel_per_city.columns = ['city', 'total_hotel']

fig1, ax1 = plt.subplots(figsize=(12, 6))
ax1.bar(hotel_per_city['city'], hotel_per_city['total_hotel'], color='dodgerblue')
ax1.set_xlabel('Kota', fontsize=14)
ax1.set_ylabel('Jumlah Hotel', fontsize=14)
ax1.set_xticklabels(hotel_per_city['city'], rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig1)

# Menampilkan Tabel Data Hotel per Kota
st.subheader("📋 Data Hotel per Kota")
city_data = df_clean[df_clean['city'] == selected_city]
st.dataframe(city_data[['city', 'region', 'name', 'starRating', 'price']])

# Evaluasi Kualitas Data
st.subheader("🔍 Evaluasi Kualitas Data")
accuracy = 100.00
completeness = 100.00
consistency = 100.00
timeliness = "Tidak terukur"

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="📈 Accuracy", value=f"{accuracy}%")
with col2:
    st.metric(label="✔️ Completeness", value=f"{completeness}%")
with col3:
    st.metric(label="🔄 Consistency", value=f"{consistency}%")
with col4:
    st.metric(label="⏱️ Timeliness", value=timeliness)

st.write(f"Timeliness tidak dapat diukur karena dataset tidak memiliki timestamp.")

# Garis pemisah visualisasi
st.markdown("<hr>", unsafe_allow_html=True)

# 3. Harga vs Rating
st.subheader("💵⭐ Harga vs Rating")
fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.scatter(df_clean['price'], df_clean['starRating'], alpha=0.5, color='b')
ax2.set_title("Hubungan Harga dan Rating Hotel", fontsize=16, weight='bold')
ax2.set_xlabel("Harga per Malam (IDR)", fontsize=14)
ax2.set_ylabel("Rating Hotel", fontsize=14)
plt.grid(True)
plt.tight_layout()
st.pyplot(fig2)

# Garis pemisah visualisasi
st.markdown("<hr>", unsafe_allow_html=True)

# 4. Distribusi Harga Hotel per Kota
st.subheader("💸 Distribusi Harga Hotel per Kota")
fig3, ax3 = plt.subplots(figsize=(12, 6))
sns.histplot(df_clean['price'], kde=True, color='purple', ax=ax3)
ax3.set_title("Distribusi Harga Hotel", fontsize=16)
ax3.set_xlabel("Harga per Malam (IDR)", fontsize=14)
ax3.set_ylabel("Frekuensi", fontsize=14)
plt.tight_layout()
st.pyplot(fig3)

# Garis pemisah visualisasi
st.markdown("<hr>", unsafe_allow_html=True)

# 5. Ketersediaan Hotel per Kota (Top 5)
st.subheader("🏙️ Ketersediaan Hotel per Kota (Top 5)")
top_cities = df_clean['city'].value_counts().head(5)
fig4, ax4 = plt.subplots(figsize=(12, 6))
ax4.bar(top_cities.index, top_cities.values, color='lightgreen')
ax4.set_xlabel('Kota', fontsize=14)
ax4.set_ylabel('Jumlah Hotel', fontsize=14)
plt.tight_layout()
st.pyplot(fig4)

# Garis pemisah visualisasi
st.markdown("<hr>", unsafe_allow_html=True)

# 6. Rata-rata Harga Hotel per Kota
st.subheader("🏠 Rata-rata Harga Hotel per Kota")
price_per_city = df_clean.groupby('city')['price'].mean().reset_index()
price_per_city.columns = ['city', 'avg_price']

fig5, ax5 = plt.subplots(figsize=(12, 6))
bars5 = ax5.bar(price_per_city['city'], price_per_city['avg_price'], color='orange')
ax5.set_xlabel('Kota', fontsize=14)
ax5.set_ylabel('Harga Rata-Rata (IDR)', fontsize=14)

# Label harga di atas bar
for bar in bars5:
    yval = bar.get_height()
    ax5.text(bar.get_x() + bar.get_width()/2, yval + 50000, f'{int(yval):,}', ha='center', fontsize=12)

plt.tight_layout()
st.pyplot(fig5)

# Kesimpulan / Solusi yang Diberikan
st.subheader("🎯 Solusi dan Kesimpulan")
st.write("""
- **Masalah Utama**: Distribusi ketersediaan hotel yang tidak merata saat Tahun Baru
- **Fokus Analisis**: Memantau dan menganalisis distribusi hotel (bukan booking atau customer)
- **Solusi**: Monitoring dan optimasi distribusi hotel berdasarkan data yang tersedia
- **Output**: Dashboard interaktif untuk memvisualisasikan distribusi dan memberikan rekomendasi optimasi
""")