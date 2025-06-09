import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime # Untuk rentang tanggal di sidebar

# Set style seaborn untuk visualisasi yang rapi
sns.set(style='darkgrid') # Mengubah dari 'dark' ke 'darkgrid' untuk plot garis/bar


# --- 1. Fungsi Pembersihan & Penyesuaian Data 
@st.cache_data # Cache data agar tidak di-load ulang setiap kali ada interaksi
def load_and_clean_data():
    day_df = pd.read_csv("day.csv")
    hour_df = pd.read_csv("hour.csv")

    # Rename columns for day_df
    day_df.rename(columns={
        'dteday': 'tanggal',
        'yr': 'tahun',
        'mnth': 'bulan',
        'weathersit': 'kondisi_cuaca',
        'temp': 'suhu_normalisasi',
        'atemp': 'suhu_rasa_normalisasi',
        'hum': 'kelembaban_normalisasi',
        'windspeed': 'kecepatan_angin_normalisasi',
        'cnt': 'jumlah_pengguna'
    }, inplace=True)

    # Convert 'tanggal' to datetime
    day_df['tanggal'] = pd.to_datetime(day_df['tanggal'])

    # Map numerical values to categorical labels for day_df
    day_df['season'] = day_df['season'].map({
        1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
    })
    day_df['tahun'] = day_df['tahun'].map({
        0: 2011, 1: 2012
    })
    day_df['bulan'] = day_df['bulan'].map({
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    })
    day_df['holiday'] = day_df['holiday'].map({
        0: 'Bukan Hari Libur', 1: 'Hari Libur'
    })
    day_df['weekday'] = day_df['weekday'].map({
        0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'
    })
    day_df['workingday'] = day_df['workingday'].map({
        0: 'Bukan Hari Kerja', 1: 'Hari Kerja'
    })
    day_df['kondisi_cuaca'] = day_df['kondisi_cuaca'].map({
        1: 'Cerah/Sedikit Berawan',
        2: 'Berkabut/Berawan',
        3: 'Salju Ringan/Hujan',
        4: 'Hujan Lebat/Badai Salju'
    })

    # Rename columns for hour_df
    hour_df.rename(columns={
        'dteday': 'tanggal',
        'yr': 'tahun',
        'mnth': 'bulan',
        'hr': 'jam',
        'weathersit': 'kondisi_cuaca',
        'temp': 'suhu_normalisasi',
        'atemp': 'suhu_rasa_normalisasi',
        'hum': 'kelembaban_normalisasi',
        'windspeed': 'kecepatan_angin_normalisasi',
        'cnt': 'jumlah_pengguna'
    }, inplace=True)

    # Convert 'tanggal' to datetime
    hour_df['tanggal'] = pd.to_datetime(hour_df['tanggal'])

    # Map numerical values to categorical labels for hour_df
    hour_df['season'] = hour_df['season'].map({
        1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
    })
    hour_df['tahun'] = hour_df['tahun'].map({
        0: 2011, 1: 2012
    })
    hour_df['bulan'] = hour_df['bulan'].map({
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    })
    hour_df['holiday'] = hour_df['holiday'].map({
        0: 'Bukan Hari Libur', 1: 'Hari Libur'
    })
    hour_df['weekday'] = hour_df['weekday'].map({
        0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'
    })
    hour_df['workingday'] = hour_df['workingday'].map({
        0: 'Bukan Hari Kerja', 1: 'Hari Kerja'
    })
    hour_df['kondisi_cuaca'] = hour_df['kondisi_cuaca'].map({
        1: 'Cerah/Sedikit Berawan',
        2: 'Berkabut/Berawan',
        3: 'Salju Ringan/Hujan',
        4: 'Hujan Lebat/Badai Salju'
    })
    
    return day_df, hour_df

day_df, hour_df = load_and_clean_data()

# --- 2. Fungsi untuk Setiap Pertanyaan Bisnis (EDA) ---

# Pertanyaan 1: Pola penggunaan sepeda harian (distribusi penggunaan per jam)
def get_hourly_usage_pattern(df):
    df['tipe_hari'] = df['weekday'].apply(lambda x: 'Akhir Pekan' if x in ['Minggu', 'Sabtu'] else 'Hari Kerja')
    usage_pattern_hourly = df.groupby(['jam', 'tipe_hari'])['jumlah_pengguna'].mean().reset_index()
    return usage_pattern_hourly

# Pertanyaan 2: Perbandingan total penggunaan sepeda pada kategori hari
def get_usage_by_day_category(df):
    def categorize_day(row):
        if row['holiday'] == 'Hari Libur':
            return 'Hari Libur'
        elif row['workingday'] == 'Hari Kerja':
            return 'Hari Kerja (Non-Libur)'
        else:
            return 'Akhir Pekan (Non-Libur)'
    df['kategori_hari'] = df.apply(categorize_day, axis=1)
    usage_by_day_category = df.groupby('kategori_hari')['jumlah_pengguna'].sum().reset_index()
    
    # Pastikan urutan kategori untuk visualisasi
    desired_order = ['Hari Kerja (Non-Libur)', 'Akhir Pekan (Non-Libur)', 'Hari Libur']
    usage_by_day_category['kategori_hari'] = pd.Categorical(usage_by_day_category['kategori_hari'], categories=desired_order, ordered=True)
    usage_by_day_category = usage_by_day_category.sort_values('kategori_hari')
    
    return usage_by_day_category

# Pertanyaan 3: Total penggunaan sepeda per musim
def get_usage_by_season(df):
    usage_by_season = df.groupby('season')['jumlah_pengguna'].sum().reset_index()
    usage_by_season_sorted = usage_by_season.sort_values(by='jumlah_pengguna', ascending=False)
    return usage_by_season_sorted

# --- 3. Sidebar untuk Filter Tanggal ---
st.sidebar.title("Filter Data")

# Mengambil tanggal min dan max dari data day_df
min_date = day_df["tanggal"].min()
max_date = day_df["tanggal"].max()

# Informasi tanggal untuk setiap musim (berdasarkan definisi di dataset)
season_dates = {
    "Spring": ("2011-01-01", "2011-03-20", "2012-01-01", "2012-03-20"),
    "Summer": ("2011-03-21", "2011-06-20", "2012-03-21", "2012-06-20"),
    "Fall": ("2011-06-21", "2011-09-20", "2012-06-21", "2012-09-20"),
    "Winter": ("2011-09-21", "2011-12-31", "2012-09-21", "2012-12-31"),
}

# Widget date_input di sidebar
start_date, end_date = st.sidebar.date_input(
    label='Pilih Rentang Tanggal',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

st.sidebar.subheader("Informasi Musim:")
for season, dates in season_dates.items():
    st.sidebar.write(f"**{season}:**")
    st.sidebar.write(f"  *2011:* {dates[0]} - {dates[1]}")
    st.sidebar.write(f"  *2012:* {dates[2]} - {dates[3]}")


# --- Filter main_df berdasarkan rentang tanggal yang dipilih ---
# Perlu filter juga hour_df jika plot jam ingin sesuai rentang tanggal
main_day_df = day_df[(day_df["tanggal"] >= pd.to_datetime(start_date)) & 
                     (day_df["tanggal"] <= pd.to_datetime(end_date))]
main_hour_df = hour_df[(hour_df["tanggal"] >= pd.to_datetime(start_date)) & 
                      (hour_df["tanggal"] <= pd.to_datetime(end_date))]


# --- 4. Main Content Dashboard ---
st.header('Dashboard Analisis Penggunaan Sepeda 🚲')

# Metrik Sederhana (Contoh)
total_riders_day = main_day_df['jumlah_pengguna'].sum()
avg_daily_riders = round(main_day_df['jumlah_pengguna'].mean(), 2)

st.subheader("Ringkasan Statistik Dasar")
col1, col2 = st.columns(2)

with col1:
    st.metric("Total Pengguna (Dalam Rentang Tanggal)", value=f"{total_riders_day:,}")

with col2:
    st.metric("Rata-rata Pengguna Harian", value=f"{avg_daily_riders:,}")

# --- Plot untuk Pertanyaan Bisnis 1: Pola Penggunaan per Jam ---
st.subheader("1. Pola Penggunaan Sepeda per Jam (Hari Kerja vs. Akhir Pekan)")
hourly_usage_data = get_hourly_usage_pattern(main_hour_df) # Gunakan main_hour_df yang sudah difilter

hourly_usage_weekday = hourly_usage_data[hourly_usage_data['tipe_hari'] == 'Hari Kerja']
hourly_usage_weekend = hourly_usage_data[hourly_usage_data['tipe_hari'] == 'Akhir Pekan']

fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.lineplot(
    x='jam',
    y='jumlah_pengguna', 
    data=hourly_usage_weekday,
    label='Hari Kerja',
    marker='o',
    color='#1f77b4',
    ax=ax1
)
sns.lineplot(
    x='jam',
    y='jumlah_pengguna',
    data=hourly_usage_weekend,
    label='Akhir Pekan',
    marker='o',
    color='#ff7f0e',
    ax=ax1
)
ax1.set_title('Rata-rata Penggunaan Sepeda per Jam: Hari Kerja vs. Akhir Pekan', fontsize=16)
ax1.set_xlabel('Jam (0-23)', fontsize=12)
ax1.set_ylabel('Rata-rata Jumlah Pengguna', fontsize=12) 
ax1.set_xticks(range(0, 24))
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend(fontsize=10)
plt.tight_layout()
st.pyplot(fig1)

# --- Plot untuk Pertanyaan Bisnis 2: Penggunaan per Kategori Hari ---
st.subheader("2. Perbandingan Total Penggunaan Sepeda berdasarkan Kategori Hari")
usage_by_day_cat_data = get_usage_by_day_category(main_day_df) 

fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(
    x='kategori_hari',
    y='jumlah_pengguna',
    data=usage_by_day_cat_data,
    palette='viridis',
    ax=ax2
)
ax2.set_title('Total Penggunaan Sepeda berdasarkan Kategori Hari', fontsize=16)
ax2.set_xlabel('Kategori Hari', fontsize=12)
ax2.set_ylabel('Total Jumlah Pengguna', fontsize=12)
# Perbaikan ada di baris berikut: hapus `ha='right'`
ax2.tick_params(axis='x', rotation=15, labelsize=10)
ax2.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
st.pyplot(fig2)


# --- Plot untuk Pertanyaan Bisnis 3: Penggunaan per Musim ---
st.subheader("3. Total Penggunaan Sepeda berdasarkan Musim")

all_seasons_options = ['Semua Musim'] + sorted(day_df['season'].unique().tolist())
selected_season = st.selectbox("Pilih Musim untuk Melihat Detail Harian", all_seasons_options, key='season_selector') # Tambahkan key unik

usage_by_season_data = get_usage_by_season(main_day_df)
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.barplot(
    x='season',
    y='jumlah_pengguna',
    data=usage_by_season_data,
    palette='magma',
    ax=ax3
)
ax3.set_title('Total Penggunaan Sepeda berdasarkan Musim (Keseluruhan)', fontsize=16)
ax3.set_xlabel('Musim', fontsize=12)
ax3.set_ylabel('Total Jumlah Pengguna', fontsize=12)
ax3.tick_params(axis='x', labelsize=10)
ax3.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
st.pyplot(fig3)

# Bagian detail untuk Musim yang Dipilih (Metrik & Line Plot Harian)
st.subheader(f"Detail Penggunaan Harian untuk Musim: {selected_season}")

if selected_season == 'Semua Musim':
    filtered_season_df = main_day_df.copy() # Gunakan copy untuk menghindari SettingWithCopyWarning
    total_usage_selected_season = main_day_df['jumlah_pengguna'].sum()
else:
    # Filter main_day_df (yang sudah difilter tanggal) berdasarkan musim yang dipilih
    filtered_season_df = main_day_df[main_day_df['season'] == selected_season].copy()
    total_usage_selected_season = filtered_season_df['jumlah_pengguna'].sum()

# Menampilkan metrik total penggunaan untuk musim yang dipilih
st.metric(f"Total Penggunaan di {selected_season} (dalam rentang tanggal terpilih)", value=f"{total_usage_selected_season:,} Pengguna")

if not filtered_season_df.empty: 
    fig_daily_season, ax_daily_season = plt.subplots(figsize=(12, 6))
    sns.lineplot(
        x='tanggal',
        y='jumlah_pengguna',
        data=filtered_season_df,
        marker='o',
        linewidth=1,
        color='blue', 
        ax=ax_daily_season
    )
    ax_daily_season.set_title(f"Penggunaan Sepeda Harian di Musim {selected_season} (dalam rentang tanggal terpilih)", fontsize=16)
    ax_daily_season.set_xlabel('Tanggal', fontsize=12)
    ax_daily_season.set_ylabel('Jumlah Pengguna', fontsize=12)
    ax_daily_season.tick_params(axis='x', rotation=45, labelsize=10)
    ax_daily_season.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    st.pyplot(fig_daily_season)
else:
    # Pesan jika tidak ada data untuk kombinasi filter
    st.write("Tidak ada data penggunaan sepeda untuk rentang tanggal dan musim yang dipilih ini.")

# --- Kesimpulan ---
st.subheader("Kesimpulan Analisis")
st.write("""
Berdasarkan analisis data penggunaan sepeda dari tahun 2011 hingga 2012, berikut adalah beberapa wawasan utama:
* **Pola Penggunaan Harian:** Penggunaan sepeda pada **hari kerja menunjukkan dua puncak (pagi dan sore)** yang terkait dengan jam komuter. Sementara itu, pada **akhir pekan, pola penggunaan lebih merata dengan puncak di siang hari**, menunjukkan aktivitas rekreasi.
* **Penggunaan Berdasarkan Kategori Hari:** **Hari Kerja (Non-Libur) mendominasi total penggunaan sepeda**, menegaskan peran sepeda sebagai moda transportasi harian. Akhir pekan (non-libur) menempati posisi kedua, sedangkan hari libur memiliki penggunaan terendah.
* **Penggunaan Berdasarkan Musim:** **Musim Gugur (Fall) menunjukkan total penggunaan sepeda tertinggi**, kemungkinan besar karena kondisi cuaca yang paling ideal. Sebaliknya, **Musim Dingin (Winter) mencatat penggunaan terendah**, yang sangat dipengaruhi oleh kondisi cuaca yang tidak mendukung.

Wawasan ini dapat digunakan untuk mengoptimalkan operasional layanan bike-sharing, seperti penempatan dan perawatan sepeda, kampanye pemasaran, dan perencanaan staf, sesuai dengan pola permintaan yang bervariasi sepanjang hari, minggu, dan tahun.
""")