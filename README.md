🐾 D.A.S.H: Data Analysis & Smart Highlighting 🐾
Deskripsi Singkat & Tujuan Proyek
Proyek "D.A.S.H: Data Analysis & Smart Highlighting" adalah sebuah aplikasi dashboard interaktif yang dibangun menggunakan Streamlit untuk menganalisis data media. Dashboard ini dirancang khusus untuk memberikan insight cepat dan mendalam tentang kinerja media dan strategi konten, yang sangat relevan dalam konteks Produksi Media dan pemasaran digital.

Tujuan utama proyek ini adalah untuk:
- Menganalisis dan memvisualisasikan data media (sentimen, engagement, platform, tipe media, lokasi) dari berbagai sumber.
- Menyediakan antarmuka yang intuitif bagi pengguna untuk mengunggah dan menjelajahi dataset mereka sendiri.
- Mengintegrasikan kemampuan kecerdasan buatan (AI) untuk menghasilkan insight naratif yang ringkas dan relevan dari setiap visualisasi data.
- Memberikan opsi untuk mengunduh laporan PDF yang merangkum hasil analisis dan insight AI.
- Membantu pembuat konten dan pemasar membuat keputusan strategis yang lebih baik berdasarkan data yang ada.

Fitur-Fitur Utama Aplikasi Dashboard
- Antarmuka Pengguna (UI/UX) yang Intuitif & Bertema Kucing: Dashboard didesain dengan tema kucing yang lucu dan palet warna pastel tunggal (oranye/coklat lembut) yang memberikan pengalaman pengguna yang menyenangkan dan kohesif.
- Unggah Data CSV: Pengguna dapat dengan mudah mengunggah file CSV mereka sendiri untuk analisis data yang dipersonalisasi. Aplikasi dilengkapi dengan pra-pemrosesan data untuk menangani format kolom dan nilai yang hilang.
- Panduan Penggunaan Interaktif: Tersedia bagian "Cara Menggunakan Dashboard Ini" yang bisa diperluas untuk panduan langkah demi langkah.
- Visualisasi Data Interaktif: Menyajikan minimal 5 chart interaktif menggunakan Plotly untuk insight media yang mendalam:

  - Sentiment Breakdown: Distribusi sentimen (Positif/Negatif/Netral).
  - Engagement Trend Over Time: Fluktuasi engagement konten dari waktu ke waktu.
  - Platform Engagements: Perbandingan kinerja engagement di berbagai platform.
  - Media Type Mix: Analisis proporsi tipe media (Teks, Gambar, Video, Infografis, Carousel).
  - Top 5 Locations by Engagement: Identifikasi lokasi geografis dengan engagement tertinggi.
    
- Insight Naratif Bertenaga AI: Setiap chart dilengkapi dengan setidaknya 3 insight kunci yang dihasilkan secara dinamis oleh model AI (melalui integrasi OpenRouter AI). Ini memberikan interpretasi data yang mendalam dan relevan.
- Pilihan Model AI: Pengguna dapat memilih model AI yang berbeda dari OpenRouter melalui sidebar untuk personalisasi insight.
- Unduh Laporan PDF: Kemampuan untuk mengunduh laporan PDF ringkas yang berisi semua visualisasi kunci dan insight naratif yang dihasilkan AI.
- Desain Responsif: Memastikan tampilan yang optimal di berbagai ukuran layar dan perangkat.

Tech Stack yang Digunakan
- Framework Aplikasi Web: Streamlit
- Analisis Data: Pandas
- Visualisasi Data Interaktif: Plotly Express
- Pembangkitan Data Sintetis: NumPy
- Integrasi AI (LLM): OpenAI SDK untuk mengakses OpenRouter AI
- Pembuatan Laporan PDF: fpdf2 (FPDF)
- Manajemen Kode Sumber: GitHub
- Deployment Aplikasi: Streamlit Community Cloud

Cara Menjalankan Aplikasi (Lokal)
1. Kloning Repositori:
git clone https://github.com/kasend123/D.A.S.H

2. Instal Dependensi:
Pastikan file requirements.txt Anda berisi semua library yang dibutuhkan:
streamlit
pandas
plotly
numpy
openai
fpdf

3. Kemudian instal:
pip install -r requirements.txt

Konfigurasi OpenRouter API Key:
- Dapatkan kunci API Anda dari OpenRouter.ai.
- Buat folder .streamlit di direktori root proyek Anda.
- Di dalam .streamlit, buat file secrets.toml dan tambahkan baris berikut (ganti dengan kunci Anda yang sebenarnya):
- OPENROUTER_API_KEY = "sk-YOUR_ACTUAL_OPENROUTER_API_KEY_HERE" Atau, Anda bisa memasukkan kunci API langsung di kolom input pada sidebar aplikasi saat menjalankannya secara lokal.

Jalankan Aplikasi Streamlit:
streamlit run app.py

Link Aplikasi yang Sudah Di-Deploy
Anda dapat melihat versi yang sudah di-deploy dari dashboard ini di:
https://meowmeowmeow.streamlit.app/#insight-kucing-ai

Dibuat dengan 💖 oleh Tim Kucing Cerdas 🐱
