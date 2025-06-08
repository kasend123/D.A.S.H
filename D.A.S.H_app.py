import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- Konfigurasi Halaman Streamlit ---
# Mengatur judul halaman, ikon, dan layout.
st.set_page_config(
    page_title="Papan Kontrol Intelijen Media Kucing 🐾",
    page_icon="🐱", # Ikon kucing yang lucu
    layout="wide", # Layout lebar untuk tampilan dashboard yang lebih baik
    initial_sidebar_state="expanded" # Sidebar dibuka secara default
)

# --- CSS Kustom untuk Tema Kucing dan Warna Pastel ---
# Menambahkan CSS kustom untuk memberikan tampilan yang lembut, pastel, dan bertema kucing.
# Menggunakan font Inter dari Google Fonts.
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

        html, body, [class*="st-"] {
            font-family: 'Inter', sans-serif;
            color: #4B4B4B; /* Warna teks gelap lembut */
        }
        .stApp {
            background-color: #F0F2F6; /* Warna latar belakang sangat lembut */
            background-image: url('https://placehold.co/10x10/F0F2F6/F0F2F6?text=+'); /* Placeholder kecil */
            background-repeat: repeat;
        }
        .st-emotion-cache-z5fcl4 { /* Header main-content */
            background-color: #FFC0CB; /* Pink pastel untuk header */
            padding: 1rem 1rem;
            border-radius: 15px; /* Sudut membulat */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .st-emotion-cache-1avcm0n { /* Main app container */
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        .st-emotion-cache-16txt4y { /* Sidebar background */
            background-color: #D2F7DF; /* Hijau mint pastel */
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .st-emotion-cache-10qtn9e { /* Sidebar header */
            color: #3C3C3C;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #5A5A5A; /* Warna judul yang sedikit lebih gelap */
        }
        .stButton>button {
            background-color: #FFDAB9; /* Orange pastel lembut untuk tombol */
            color: #5A5A5A;
            border-radius: 10px;
            border: none;
            padding: 10px 20px;
            font-weight: bold;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #FFBF80; /* Warna sedikit lebih gelap saat hover */
            color: #3C3C3C;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transform: translateY(-2px);
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }
        .st-emotion-cache-1eqmxq9 p { /* Paragraph text */
            font-size: 1.05rem;
            line-height: 1.6;
        }
        .st-emotion-cache-1eqmxq9 .css-1dp5vir { /* Text input/text area */
            background-color: #FFFFFF;
            border-radius: 10px;
            border: 1px solid #E0E0E0;
            padding: 8px 12px;
        }
        .st-emotion-cache-16idsms p { /* File uploader text */
            color: #5A5A5A;
        }
        .st-emotion-cache-eczf16 { /* Expander header */
            background-color: #E0BBE4; /* Ungu pastel */
            border-radius: 10px;
            padding: 0.75rem 1rem;
            margin-bottom: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        .st-emotion-cache-eczf16 > div > span {
            color: #4B4B4B;
            font-weight: 600;
        }
        .st-emotion-cache-eczf16 > div > svg {
            color: #4B4B4B;
        }

        /* Styling untuk metrik */
        .metric-container {
            background-color: #FFEFD5; /* Peach pastel */
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .metric-container .st-emotion-cache-r421ms {
            color: #5A5A5A; /* Label */
            font-size: 1.1em;
            font-weight: 600;
        }
        .metric-container .st-emotion-cache-r421ms + div {
            color: #FF8C00; /* Warna value yang lebih kuat */
            font-size: 2em;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# --- Fungsi untuk Membuat Dataset Sintetis ---
def create_synthetic_data(num_rows=1000):
    """
    Membuat dataset sintetis untuk tujuan demo jika tidak ada file yang diunggah.
    """
    dates = pd.date_range(start="2024-01-01", periods=num_rows, freq="H")
    platforms = np.random.choice(["Twitter", "Instagram", "News Portal", "Facebook", "TikTok"], num_rows)
    sentiments = np.random.choice(["Positif", "Negatif", "Netral"], num_rows, p=[0.5, 0.2, 0.3])
    locations = np.random.choice(["Jakarta", "Surabaya", "Bandung", "Medan", "Yogyakarta", "Bali", "Semarang"], num_rows)
    engagement = np.random.randint(100, 5000, num_rows)
    media_types = np.random.choice(["Text", "Image", "Video", "Infographic"], num_rows)

    data = pd.DataFrame({
        "Tanggal": dates,
        "Platform": platforms,
        "Sentimen": sentiments,
        "Lokasi": locations,
        "Engagement": engagement,
        "Tipe Media": media_types
    })
    return data

# --- Header Aplikasi ---
st.title("🐾 Papan Kontrol Intelijen Media Kucing 🐾")
st.markdown("Selamat datang di papan kontrol intelijen media Anda! Unggah data Anda dan biarkan kucing-kucing kami menganalisisnya untuk insight media yang menggemaskan.")

# --- Bagian Unggah File CSV ---
st.sidebar.header("Unggah Data Anda 😺")
uploaded_file = st.sidebar.file_uploader("Pilih file CSV", type=["csv"])

data = None
if uploaded_file is not None:
    # Memuat data dari file yang diunggah
    st.sidebar.success("Meong! Data berhasil diunggah.")
    try:
        data = pd.read_csv(uploaded_file)
        # Pastikan kolom Tanggal dalam format datetime
        data["Tanggal"] = pd.to_datetime(data["Tanggal"], errors='coerce')
        # Hapus baris dengan Tanggal yang tidak valid setelah konversi
        data.dropna(subset=["Tanggal"], inplace=True)
    except Exception as e:
        st.error(f"Meong! Terjadi kesalahan saat memuat file: {e}. Pastikan itu adalah CSV yang valid.")
        data = None # Reset data jika ada kesalahan
else:
    st.sidebar.info("Tidak ada file yang diunggah. Menggunakan data sintetis untuk demo.")
    data = create_synthetic_data()

# Tampilkan pratinjau data
if data is not None and not data.empty:
    st.subheader("Pratinjau Data Kucing 📊")
    st.dataframe(data.head())

    st.markdown("---")

    # --- Bagian Visualisasi Data Interaktif ---
    st.header("Visualisasi Data Interaktif 📈")

    # 1. Sentiment Breakdown
    st.subheader("1. Sebaran Sentimen (Sentiment Breakdown) 😽")
    sentiment_counts = data["Sentimen"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentimen", "Jumlah"]
    fig_sentiment = px.pie(sentiment_counts, values="Jumlah", names="Sentimen",
                           title="Distribusi Sentimen Terhadap Topik",
                           color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_sentiment.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig_sentiment, use_container_width=True)
    st.markdown("#### Insight Kucing AI 💡")
    st.info("""
    - Mayoritas sentimen terhadap merek/kampanye ini adalah **Positif**. Ini menunjukkan penerimaan publik yang baik.
    - Sentimen **Negatif** berada pada persentase kecil, namun perlu dipantau untuk mengidentifikasi penyebabnya.
    - Sentimen **Netral** bisa menjadi peluang untuk mengkonversi audiens dengan konten yang lebih menarik.
    """)
    st.markdown("---")

    # 2. Engagement Trend Over Time
    st.subheader("2. Tren Engagement dari Waktu ke Waktu 🐾")
    # Agregasi data per hari untuk tren engagement
    data["Tanggal_Hari"] = data["Tanggal"].dt.date
    daily_engagement = data.groupby("Tanggal_Hari")["Engagement"].sum().reset_index()
    fig_engagement_trend = px.line(daily_engagement, x="Tanggal_Hari", y="Engagement",
                                   title="Tren Total Engagement Harian",
                                   color_discrete_sequence=["#FFDAB9"]) # Warna pastel orange
    fig_engagement_trend.update_xaxes(title_text="Tanggal")
    fig_engagement_trend.update_yaxes(title_text="Total Engagement")
    st.plotly_chart(fig_engagement_trend, use_container_width=True)
    st.markdown("#### Insight Kucing AI 💡")
    st.info("""
    - Terlihat puncak engagement pada tanggal-tanggal tertentu, yang mungkin berkorelasi dengan peluncuran kampanye atau peristiwa khusus.
    - Adanya penurunan engagement setelah periode puncak menunjukkan perlunya strategi konten berkelanjutan.
    - Fluktuasi harian yang signifikan bisa menandakan sensitivitas audiens terhadap berita atau tren terbaru.
    """)
    st.markdown("---")

    # 3. Platform Engagements
    st.subheader("3. Engagement Berdasarkan Platform 😺")
    platform_engagement = data.groupby("Platform")["Engagement"].sum().reset_index()
    platform_engagement = platform_engagement.sort_values(by="Engagement", ascending=False)
    fig_platform_engagement = px.bar(platform_engagement, x="Platform", y="Engagement",
                                      title="Total Engagement per Platform",
                                      color="Platform",
                                      color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_platform_engagement.update_xaxes(title_text="Platform")
    fig_platform_engagement.update_yaxes(title_text="Total Engagement")
    st.plotly_chart(fig_platform_engagement, use_container_width=True)
    st.markdown("#### Insight Kucing AI 💡")
    st.info("""
    - **Twitter** dan **Instagram** menunjukkan engagement tertinggi, mengindikasikan platform-platform ini paling efektif untuk menjangkau audiens.
    - **News Portal** memiliki engagement yang solid, menunjukkan bahwa berita dan artikel masih relevan bagi audiens.
    - Platform dengan engagement rendah mungkin memerlukan evaluasi ulang strategi atau fokus pada tipe konten yang berbeda.
    """)
    st.markdown("---")

    # 4. Media Type Mix
    st.subheader("4. Komposisi Tipe Media 😻")
    media_type_counts = data["Tipe Media"].value_counts().reset_index()
    media_type_counts.columns = ["Tipe Media", "Jumlah"]
    fig_media_type_mix = px.pie(media_type_counts, values="Jumlah", names="Tipe Media",
                                title="Proporsi Tipe Media",
                                color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_media_type_mix.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig_media_type_mix, use_container_width=True)
    st.markdown("#### Insight Kucing AI 💡")
    st.info("""
    - Konten **Video** dan **Image** mendominasi proporsi media, menunjukkan preferensi audiens terhadap format visual.
    - Meskipun **Text** memiliki proporsi lebih kecil, perannya dalam menyampaikan informasi mendalam tetap krusial.
    - **Infographic** sebagai tipe media yang sedang berkembang dapat ditingkatkan untuk menyajikan data kompleks secara visual.
    """)
    st.markdown("---")

    # 5. Top 5 Locations by Engagement
    st.subheader("5. 5 Lokasi Teratas Berdasarkan Engagement 🌍")
    location_engagement = data.groupby("Lokasi")["Engagement"].sum().reset_index()
    top_5_locations = location_engagement.sort_values(by="Engagement", ascending=False).head(5)
    fig_top_locations = px.bar(top_5_locations, x="Lokasi", y="Engagement",
                                title="Top 5 Lokasi Berdasarkan Total Engagement",
                                color="Lokasi",
                                color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_top_locations.update_xaxes(title_text="Lokasi")
    fig_top_locations.update_yaxes(title_text="Total Engagement")
    st.plotly_chart(fig_top_locations, use_container_width=True)
    st.markdown("#### Insight Kucing AI 💡")
    st.info("""
    - **Jakarta** dan **Surabaya** secara konsisten menunjukkan engagement tertinggi, menjadikannya target utama untuk kampanye lokal.
    - Memahami demografi dan preferensi di lokasi teratas ini dapat mengoptimalkan strategi konten.
    - Adanya lokasi-lokasi lain dalam Top 5 menunjukkan potensi pasar yang bisa dieksplorasi lebih lanjut.
    """)
    st.markdown("---")

    # Tambahkan metrik umum di sidebar
    st.sidebar.subheader("Statistik Ringkas 📈")
    total_engagement = data["Engagement"].sum()
    unique_platforms = data["Platform"].nunique()
    most_common_sentiment = data["Sentimen"].mode()[0]

    st.sidebar.markdown(f"""
        <div class="metric-container">
            <p>Total Engagement</p>
            <p>{total_engagement:,}</p>
        </div>
        <div class="metric-container">
            <p>Platform Unik</p>
            <p>{unique_platforms}</p>
        </div>
        <div class="metric-container">
            <p>Sentimen Paling Umum</p>
            <p>{most_common_sentiment}</p>
        </div>
    """, unsafe_allow_html=True)

else:
    st.warning("Mohon unggah file CSV atau tunggu data sintetis dimuat untuk melihat dashboard.")

# --- Footer ---
st.markdown("---")
st.markdown("Papan Kontrol Kucing Dibuat dengan 💖 oleh Tim Kucing Cerdas 🐱")
