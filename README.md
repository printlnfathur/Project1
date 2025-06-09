# Analisis Data Penggunaan Sepeda: Memahami Pola dan Tren (2011-2012)

## Deskripsi Proyek

Proyek ini bertujuan untuk menganalisis data penggunaan sepeda dari Capital Bikeshare di Washington, D.C., selama periode 2011 hingga 2012. Analisis dilakukan untuk memahami pola dan tren penggunaan sepeda, serta faktor-faktor yang mempengaruhinya, guna memberikan wawasan yang dapat mendukung optimasi operasional layanan bike-sharing. Hasil analisis divisualisasikan dalam bentuk dashboard interaktif menggunakan Streamlit.

## Sumber Data

Dataset yang digunakan dalam proyek ini adalah [Bike Sharing Dataset](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset) dari UCI Machine Learning Repository, yang mencakup data penggunaan sepeda harian (`day.csv`) dan per jam (`hour.csv`).

## Pertanyaan Bisnis

Proyek ini berusaha menjawab tiga pertanyaan bisnis utama:

1.  Bagaimana pola penggunaan sepeda harian (distribusi penggunaan per jam) bervariasi antara hari kerja dan akhir pekan?
2.  Bagaimana perbandingan total penggunaan sepeda pada hari kerja (`workingday`), hari libur (`holiday`), dan akhir pekan (`weekday`) selama satu tahun penuh?
3.  Musim manakah yang menunjukkan penggunaan sepeda tertinggi dan terendah?

## Metodologi Analisis

Proses analisis data melibatkan langkah-langkah berikut:

1.  **Data Wrangling:**
    * Memuat dataset (`day.csv` dan `hour.csv`).
    * Memeriksa missing values dan duplikasi data (tidak ditemukan duplikasi atau missing values pada dataset yang digunakan).
    * Melakukan penyesuaian nama kolom agar lebih intuitif.
    * Mengonversi kolom tanggal (`dteday`) menjadi tipe data `datetime`.
    * Mengubah nilai-nilai numerik kategorikal (misalnya, `season`, `yr`, `mnth`, `weekday`, `workingday`, `holiday`, `weathersit`) menjadi label teks yang lebih mudah dibaca untuk mempermudah interpretasi dan visualisasi.
2.  **Exploratory Data Analysis (EDA):**
    * Melakukan analisis deskriptif dan pengelompokan data (`groupby`, `mean`, `sum`) untuk menjawab setiap pertanyaan bisnis.
    * Membuat visualisasi data yang sesuai (line plot, bar plot) untuk menyajikan temuan secara intuitif.
3.  **Analisis Lanjutan (Time Series Decomposition):**
    * Menerapkan dekomposisi deret waktu pada data penggunaan sepeda harian (`jumlah_pengguna`) menggunakan `statsmodels` untuk memisahkan komponen tren, musiman, dan residual. Ini dilakukan untuk mendapatkan wawasan lebih dalam tentang pola jangka panjang dan pola berulang dalam penggunaan sepeda.
4.  **Kesimpulan:**
    * Merangkum semua temuan utama dan memberikan jawaban yang jelas atas pertanyaan bisnis.

## Temuan Kunci

Berikut adalah ringkasan temuan utama dari analisis:

* **Pola Penggunaan Harian:**
    * Pada **hari kerja**, penggunaan sepeda menunjukkan dua puncak yang jelas (pagi dan sore), yang terkait dengan jam sibuk komuter.
    * Pada **akhir pekan**, pola penggunaan lebih merata sepanjang hari dengan satu puncak di siang hari, mengindikasikan penggunaan yang lebih bersifat rekreasi.

* **Penggunaan Berdasarkan Kategori Hari:**
    * **Hari Kerja (Non-Libur)** mencatat total penggunaan sepeda tertinggi, menegaskan perannya sebagai moda transportasi harian.
    * **Akhir Pekan (Non-Libur)** berada di posisi kedua, sementara **Hari Libur** memiliki total penggunaan terendah.

* **Penggunaan Berdasarkan Musim:**
    * **Musim Gugur (Fall)** adalah musim dengan total penggunaan sepeda tertinggi, kemungkinan karena kondisi cuaca yang paling ideal.
    * **Musim Dingin (Winter)** mencatat penggunaan terendah, sangat dipengaruhi oleh kondisi cuaca ekstrem.

* **Tren Keseluruhan (dari Time Series Decomposition):**
    * Terdapat **tren peningkatan yang jelas** dalam penggunaan sepeda harian dari tahun 2011 ke 2012, menunjukkan pertumbuhan popularitas layanan.
    * Adanya **pola musiman tahunan yang kuat** yang mempengaruhi penggunaan sepeda (puncak di musim semi/panas/gugur, lembah di musim dingin).

## Cara Menjalankan Proyek

1.  **Unduh File Proyek:**
    Pastikan Anda telah mengunduh semua file proyek berikut ke satu folder di komputer lokal Anda:
    * `dashboard.py`
    * `Project_1.py`
    * `day.csv`
    * `hour.csv`
    * `requirements.txt`
    * `README.md` (file ini sendiri)

2.  **Instal Dependensi:**
    Pastikan Anda memiliki Python (disarankan versi 3.8 atau lebih baru) terinstal di komputer Anda. Buka terminal atau command prompt, navigasikan ke folder tempat Anda menyimpan file proyek, lalu instal semua *library* yang diperlukan menggunakan `pip`:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Jalankan Dashboard Streamlit:**
    Setelah semua dependensi terinstal, jalankan aplikasi Streamlit dari terminal atau command prompt di folder yang sama:
    ```bash
    streamlit run dashboard.py
    ```
    Dashboard interaktif akan otomatis terbuka di browser web default Anda.
