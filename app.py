import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Membaca dataset yang sudah dibersihkan
df_clean = pd.read_csv('hotel_distribution_cleaned.csv')

# Menampilkan judul utama
st.title("Dashboard Monitoring Distribusi Hotel 🏨")

# Sidebar Filter - Pilih Kota
st.sidebar.header("🔍 Filter Data")
selected_city = st.sidebar.selectbox("Pilih Kota", df_clean['city'].unique(), key="city_select")

# 1. Displaying Key Metrics (e.g., Total Hotel, Total Rating, etc.)
total_hotel = df_clean['name'].nunique()
total_city = df_clean['city'].nunique()
avg_price = df_clean['price'].mean()
avg_rating = df_clean['starRating'].mean()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Hotel", value=total_hotel)
with col2:
    st.metric(label="Total Kota", value=total_city)
with col3:
    st.metric(label="Harga Rata-Rata", value=f"IDR {avg_price:,.0f}")

# 2. Displaying Data Quality Metrics
st.subheader("Evaluasi Kualitas Data 📊")
accuracy = 100.00
completeness = 100.00
consistency = 100.00
timeliness = "Tidak terukur"

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Accuracy", value=f"{accuracy}%")
with col2:
    st.metric(label="Completeness", value=f"{completeness}%")
with col3:
    st.metric(label="Consistency", value=f"{consistency}%")
with col4:
    st.metric(label="Timeliness", value=timeliness, delta="N/A")

st.write(f"Timeliness tidak dapat diukur karena dataset tidak memiliki timestamp.")

# 3. Jumlah Hotel per Kota
st.subheader("Jumlah Hotel per Kota 📊")
hotel_per_city = df_clean.groupby('city')['name'].nunique().reset_index()
hotel_per_city.columns = ['city', 'total_hotel']

fig1, ax1 = plt.subplots(figsize=(12, 6))
ax1.bar(hotel_per_city['city'], hotel_per_city['total_hotel'], color='#FFB6C1')  # Soft pink color for theme
ax1.set_xlabel('Kota', fontsize=14)
ax1.set_ylabel('Jumlah Hotel', fontsize=14)
ax1.set_xticklabels(hotel_per_city['city'], rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig1)

# Tampilkan tabel di bawah visualisasi
st.write("📋 Tabel Data Jumlah Hotel per Kota")
st.dataframe(hotel_per_city)

# 4. Rata-rata Rating per Kota
st.subheader("Rata-rata Rating Hotel per Kota ⭐")
rating_per_city = df_clean.groupby('city')['starRating'].mean().reset_index()
rating_per_city.columns = ['city', 'avg_rating']

fig2, ax2 = plt.subplots(figsize=(12, 6))
bars2 = ax2.bar(rating_per_city['city'], rating_per_city['avg_rating'], color='#FF6347')  # Tomato color for rating
ax2.set_xlabel('Kota', fontsize=14)
ax2.set_ylabel('Rating', fontsize=14)

# Label angka di atas bar
for bar in bars2:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, yval + 0.05, round(yval, 2), ha='center', fontsize=12)

plt.tight_layout()
st.pyplot(fig2)

# 5. Harga vs Rating (Scatter Plot)
st.subheader("Harga vs Rating 💰⭐")
fig5, ax5 = plt.subplots(figsize=(10, 6))
ax5.scatter(df_clean['price'], df_clean['starRating'], alpha=0.5, color='b')
ax5.set_title("Hubungan Harga dan Rating Hotel", fontsize=16, weight='bold')
ax5.set_xlabel("Harga per Malam (IDR)", fontsize=14)
ax5.set_ylabel("Rating Hotel", fontsize=14)
plt.grid(True)
plt.tight_layout()
st.pyplot(fig5)

# Kesimpulan dan solusi
st.subheader("🎯 Kesimpulan dan Solusi")
st.write("""
- **Masalah Utama:** Distribusi ketersediaan hotel tidak merata saat Tahun Baru.
- **Fokus Analisis:** Supply hotel (bukan booking, bukan customer).
- **Solusi:** Monitoring & optimasi distribusi hotel untuk memastikan distribusi yang lebih merata dan efektif.
- **Output:** Dashboard yang memvisualisasikan distribusi hotel dan rekomendasi optimasi distribusi.
""")

# Menambahkan info dalam bentuk tabel di sidebar
st.sidebar.header("🏨 Data Hotel per Kota")
st.sidebar.write("Pilih Kota untuk melihat data distribusi hotel.")
selected_city_data = df_clean[df_clean['city'] == selected_city]
st.sidebar.dataframe(selected_city_data)