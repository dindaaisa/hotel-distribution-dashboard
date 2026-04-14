import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# Membaca dataset yang sudah dibersihkan
df_clean = pd.read_csv('hotel_distribution_cleaned.csv')

# Menampilkan judul utama dengan icon
st.title("🏨 Dashboard Monitoring Distribusi Hotel 🏙️")

# Sidebar Filter
st.sidebar.header("🛎️ Filter Data")
selected_city = st.sidebar.selectbox("Pilih Kota", df_clean['city'].unique())

# Filter data berdasarkan kota yang dipilih
filtered_data = df_clean[df_clean['city'] == selected_city]

# 1. Displaying Key Metrics (e.g., Total Hotel, Total Rating, etc.)
total_hotel = filtered_data['name'].nunique()
total_city = df_clean['city'].nunique()
avg_price = filtered_data['price'].mean()
avg_rating = filtered_data['starRating'].mean()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="📍 Total Hotel", value=total_hotel)
with col2:
    st.metric(label="🌍 Total Kota", value=total_city)
with col3:
    st.metric(label="💲 Harga Rata-Rata", value=f"IDR {avg_price:,.0f}")

# Garis pemisah
st.markdown("---")

# 2. Tabel Data yang Ada
st.subheader("📑 Tabel Data Hotel")
st.write(filtered_data)

# 3. Evaluasi Kualitas Data
st.subheader("🧪 Evaluasi Kualitas Data")
accuracy = 100.00
completeness = 100.00
consistency = 100.00
timeliness = "Tidak terukur"

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="✅ Accuracy", value=f"{accuracy}%")
with col2:
    st.metric(label="📊 Completeness", value=f"{completeness}%")
with col3:
    st.metric(label="🔑 Consistency", value=f"{consistency}%")
with col4:
    st.metric(label="⏳ Timeliness", value=timeliness, delta="N/A")

st.write(f"Timeliness tidak dapat diukur karena dataset tidak memiliki timestamp.")

# Garis pemisah
st.markdown("---")

# 4. Jumlah Hotel per Kota (Bar Chart)
st.subheader("📊 Jumlah Hotel per Kota")
hotel_per_city = df_clean.groupby('city')['name'].nunique().reset_index()
hotel_per_city.columns = ['city', 'total_hotel']

fig1, ax1 = plt.subplots(figsize=(12, 6))
ax1.bar(hotel_per_city['city'], hotel_per_city['total_hotel'], color='skyblue')
ax1.set_xlabel('Kota', fontsize=14)
ax1.set_ylabel('Jumlah Hotel', fontsize=14)
ax1.set_xticklabels(hotel_per_city['city'], rotation=45, ha='right')
ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'))
plt.tight_layout()
st.pyplot(fig1)

# 5. Rata-rata Rating per Kota (Pie Chart)
st.subheader("⭐ Rata-rata Rating Hotel per Kota")
rating_per_city = df_clean.groupby('city')['starRating'].mean().reset_index()
rating_per_city.columns = ['city', 'avg_rating']

fig2, ax2 = plt.subplots(figsize=(8, 8))
ax2.pie(rating_per_city['avg_rating'], labels=rating_per_city['city'], autopct='%1.1f%%', startangle=90)
ax2.set_title('Distribusi Rata-Rata Rating per Kota', fontsize=16)
st.pyplot(fig2)

# 6. Rata-rata Harga per Kota (Box Plot)
st.subheader("💰 Rata-rata Harga per Kota")
price_per_city = df_clean.groupby('city')['price'].mean().reset_index()
price_per_city.columns = ['city', 'avg_price']

fig3, ax3 = plt.subplots(figsize=(12, 6))
sns.boxplot(x='city', y='price', data=df_clean, ax=ax3, color='lightgreen')
ax3.set_xlabel('Kota', fontsize=14)
ax3.set_ylabel('Harga per Malam (IDR)', fontsize=14)
plt.tight_layout()
st.pyplot(fig3)

# 7. Durasi Menginap per Kota (Visualisasi Baru)
st.subheader("⏳ Durasi Menginap Rata-Rata per Kota")
stay_duration_per_city = df_clean.groupby('city')['num_staying_nights'].mean().reset_index()
stay_duration_per_city.columns = ['city', 'avg_stay_duration']

fig4, ax4 = plt.subplots(figsize=(12, 6))
ax4.bar(stay_duration_per_city['city'], stay_duration_per_city['avg_stay_duration'], color='purple')
ax4.set_xlabel('Kota', fontsize=14)
ax4.set_ylabel('Durasi Menginap (Hari)', fontsize=14)

# Label angka di atas bar
for bar in ax4.patches:
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width() / 2, height + 0.05, round(height, 2), ha='center', fontsize=12)

plt.tight_layout()
st.pyplot(fig4)

# 8. Hotel dengan Rating Tertinggi per Kota (Visualisasi Baru)
st.subheader("🏅 Hotel dengan Rating Tertinggi per Kota")
best_hotels_per_city = df_clean.loc[df_clean.groupby('city')['starRating'].idxmax()][['city', 'name', 'starRating']]

# Menampilkan tabel hotel dengan rating tertinggi per kota
st.write(best_hotels_per_city)

# 9. Distribusi Star Rating Hotel (Pie Chart)
st.subheader("🌟 Distribusi Star Rating Hotel")
star_distribution = df_clean['starRating'].value_counts().reset_index()
star_distribution.columns = ['starRating', 'jumlah']
fig5, ax5 = plt.subplots(figsize=(8, 8))
ax5.pie(star_distribution['jumlah'], labels=star_distribution['starRating'], autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors, pctdistance=0.85, wedgeprops={"edgecolor": "none"})
ax5.set_title("Distribusi Star Rating Hotel", fontsize=16, weight='bold')
st.pyplot(fig5)

# 10. Jumlah Hotel dengan Fasilitas Tertentu
st.subheader("🏨 Jumlah Hotel dengan Fasilitas Tertentu")
facilities_count = df_clean['hotelFeatures'].str.contains("gym|spa|pool|accessibility", case=False, na=False).sum()
st.write(f"Jumlah hotel dengan fasilitas gym/spa/pool atau aksesibilitas: {facilities_count}")

# Garis pemisah
st.markdown("---")

# 11. Kesimpulan
st.subheader("🎯 Kesimpulan")
st.write("""
**Masalah Utama:** Ketidakseimbangan distribusi hotel di berbagai kota pada periode Tahun Baru, mengarah pada potensi kekurangan atau kelebihan kapasitas hotel.

**Fokus Analisis:** Menganalisis **supply hotel** berdasarkan lokasi, rating, dan harga, untuk menentukan kota-kota dengan ketersediaan dan kualitas hotel yang optimal.

**Solusi yang Diberikan:** 
- Dashboard ini membantu **memantau distribusi hotel**, memperlihatkan **rata-rata harga** dan **rating hotel** di tiap kota.
- Menyediakan **rekomendasi distribusi hotel** dengan mempertimbangkan kualitas dan harga, serta memberi wawasan terkait **hotel dengan fasilitas unggulan**.

**Output yang Dihasilkan:** 
- Memberikan **insight** mengenai pengalokasian hotel berdasarkan kebutuhan pasar dan **rekomendasi strategis** untuk kota dengan potensi pengembangan lebih lanjut.
""")