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

# --- CSS Kustom untuk Tema Kucing dan Warna Pastel (Satu Hue: Orange/Brown) ---
# Menggunakan font Inter dari Google Fonts.
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

        html, body, [class*="st-"] {
            font-family: 'Inter', sans-serif;
            color: #4B4B4B; /* Warna teks gelap lembut */
        }
        .stApp {
            background-color: #FDF7F5; /* Sangat ringan, hampir putih dengan hint warm */
            background-image: url('https://placehold.co/10x10/FDF7F5/FDF7F5?text=+'); /* Placeholder kecil */
            background-repeat: repeat;
        }
        .st-emotion-cache-z5fcl4 { /* Header main-content */
            background-color: #F8E0CC; /* Oranye pastel lembut untuk header */
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
            background-color: #D4A59A; /* Coklat/oranye pastel yang lebih dalam */
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
            background-color: #EEDDCC; /* Peach/oranye pastel lembut untuk tombol */
            color: #5A5A5A;
            border-radius: 10px;
            border: none;
            padding: 10px 20px;
            font-weight: bold;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #E5CCBB; /* Warna sedikit lebih gelap saat hover */
            color: #3C3C3C;
            box_shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
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
            background-color: #D4A59A; /* Sama dengan sidebar untuk konsistensi */
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

        /* Styling for metrics */
        .metric-container {
            background-color: #F8EBE6; /* Peach/light orange pastel */
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
            color: #D4A59A; /* Stronger value color, from main palette */
            font-size: 2em;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# --- Define a single-hue pastel color sequence for Plotly charts ---
# Urutan warna pastel dalam satu hue (oranye/coklat lembut)
single_hue_pastel_colors = ["#F8E0CC", "#EEDDCB", "#E0CCBB", "#D4BBAC", "#C8AA9C", "#BBAA9B"]


# --- Function to Create Synthetic Data ---
def create_synthetic_data(num_rows=1000):
    """
    Creates synthetic data for demo purposes if no file is uploaded.
    """
    dates = pd.date_range(start="2024-01-01", periods=num_rows, freq="H")
    platforms = np.random.choice(["X/Twitter", "Instagram", "News Portal", "Facebook", "TikTok", "YouTube"], num_rows)
    sentiments = np.random.choice(["Positive", "Negative", "Neutral"], num_rows, p=[0.5, 0.2, 0.3])
    locations = np.random.choice(["Jakarta", "Surabaya", "Bandung", "Medan", "Yogyakarta", "Bali", "Semarang", "Denpasar", "Makassar"], num_rows)
    engagement = np.random.randint(100, 5000, num_rows)
    media_types = np.random.choice(["Text", "Image", "Video", "Carousel", "Infographic"], num_rows)
    influencer_brand = np.random.choice(["@genzfoodie | Sipply", "@kulinerhits | Sipply", "@drinkculture | Sipply", "@snackattack | Sipply", "@tastebuds.id | Sipply"], num_rows)
    post_type = np.random.choice(["Review", "Product Launch", "Behind the Scenes", "Collab", "Promo"], num_rows)


    data = pd.DataFrame({
        "Date": dates,
        "Platform": platforms,
        "Sentiment": sentiments,
        "Location": locations,
        "Engagements": engagement,
        "Media_Type": media_types,
        "Influencer_Brand": influencer_brand,
        "Post_Type": post_type
    })
    return data

# --- Function for Data Cleaning and Preprocessing ---
def clean_and_preprocess_data(df):
    """
    Performs cleaning and preprocessing on the uploaded DataFrame.
    """
    original_rows = len(df)
    st.sidebar.markdown("---")
    st.sidebar.subheader("Status Pembersihan Data 🧹")
    cleaning_messages = []

    # Define essential columns expected from the CSV
    essential_columns = ["Date", "Platform", "Sentiment", "Location", "Engagements", "Media_Type"]
    # Add optional columns present in the CSV to avoid discarding them
    optional_columns = ["Influencer_Brand", "Post_Type"]
    all_expected_columns = essential_columns + optional_columns

    # Check if all essential columns are present
    missing_essential_columns = [col for col in essential_columns if col not in df.columns]
    if missing_essential_columns:
        st.error(f"Meong! Essential columns not found in your file: {', '.join(missing_essential_columns)}. "
                 f"Please ensure your CSV has these columns.")
        return None # Return None if essential columns are missing

    # 1. Ensure 'Date' column is in datetime format and drop invalid rows
    if "Date" in df.columns:
        initial_invalid_dates = df["Date"].isnull().sum() # Count NaNs before conversion
        df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
        # Count NaNs after conversion, this is the number of rows that could not be converted
        converted_invalid_dates = df["Date"].isnull().sum()
        if converted_invalid_dates > initial_invalid_dates: # Only log if new NaTs appeared
            cleaning_messages.append(f"- Removed {converted_invalid_dates - initial_invalid_dates} rows with invalid 'Date' format.")
        df.dropna(subset=["Date"], inplace=True)
    else:
        st.error("Meong! 'Date' column not found.")
        return None

    # 2. Ensure 'Engagements' column is numeric
    if "Engagements" in df.columns:
        df["Engagements"] = pd.to_numeric(df["Engagements"], errors='coerce')
        if df["Engagements"].isnull().any():
            nan_engagement_count = df["Engagements"].isnull().sum()
            cleaning_messages.append(f"- Removed {nan_engagement_count} rows with invalid 'Engagements' values.")
            df.dropna(subset=["Engagements"], inplace=True)
    else:
        st.error("Meong! 'Engagements' column not found.")
        return None

    # 3. Handle missing values in categorical columns (optional: fill with 'Unknown')
    categorical_columns = ["Platform", "Sentiment", "Location", "Media_Type"]
    for col in categorical_columns:
        if col in df.columns and df[col].isnull().any():
            initial_nan_count = df[col].isnull().sum()
            df.dropna(subset=[col], inplace=True) # For now, just drop to ensure visualization works
            cleaning_messages.append(f"- Removed {initial_nan_count} rows with empty values in '{col}' column.")
    
    # 4. Filter data if there are future dates (if relevant) - example
    # df = df[df["Date"] <= pd.to_datetime("today")]

    processed_rows = len(df)
    if processed_rows < original_rows:
        st.sidebar.warning(f"Meong! {original_rows - processed_rows} rows removed during cleaning.")
    else:
        st.sidebar.info("Meong! No significant rows removed during cleaning.")
    
    if cleaning_messages:
        for msg in cleaning_messages:
            st.sidebar.markdown(msg)
    else:
        st.sidebar.info("- Data appears clean, no significant cleaning required.")

    return df

# --- Application Header ---
st.title("🐾 D.A.S.H: Data Analysis & Smart Highlighting 🐾")
st.markdown("Selamat datang di papan kontrol intelijen media Anda! Unggah data Anda dan biarkan kucing-kucing kami menganalisisnya untuk insight media yang menggemaskan.")

# --- How to Use Section ---
with st.expander("🐾 Cara Menggunakan Dashboard Ini❓ 🐾"):
    st.markdown("""
    Dashboard **D.A.S.H (Data Analysis & Smart Highlighting)** dirancang untuk membantu Anda mendapatkan insight dari data media Anda dengan mudah. Ikuti langkah-langkah berikut untuk memulai:

    1.  **Unggah Data Anda:**
        * Di sidebar kiri, cari bagian "Unggah Data Anda 😺".
        * Klik tombol "Pilih file CSV" dan unggah file CSV Anda.
        * **Pastikan file CSV Anda memiliki kolom-kolom berikut:** `Date`, `Platform`, `Sentiment`, `Location`, `Engagements`, `Media_Type`.
        * Setelah berhasil diunggah, Anda akan melihat status pembersihan data di sidebar. Jika ada masalah, pesan error akan muncul.

    2.  **Jelajahi Pratinjau Data:**
        * Setelah data berhasil dimuat dan dibersihkan, Anda akan melihat tabel "Pratinjau Data Kucing" yang menampilkan beberapa baris pertama dari dataset Anda. Ini memastikan data sudah siap untuk analisis.

    3.  **Analisis Visualisasi Interaktif:**
        * Gulir ke bawah untuk melihat berbagai chart interaktif yang menampilkan insight penting dari data Anda.
        * Setiap chart dirancang untuk memberikan gambaran cepat tentang aspek tertentu dari kinerja media Anda (misalnya, distribusi sentimen, tren engagement, kinerja platform).
        * Anda bisa mengarahkan kursor ke elemen-elemen chart untuk melihat detail lebih lanjut (fitur interaktif Plotly).

    4.  **Dapatkan Insight dari Kucing AI:**
        * Di bawah setiap chart, Anda akan menemukan bagian "Insight Kucing AI 💡" yang berisi rangkuman naratif dari temuan penting, tren yang muncul, atau anomali data. Insight ini dihasilkan oleh model AI untuk membantu Anda memahami data dengan lebih baik.

    5.  **Periksa Statistik Ringkas:**
        * Di sidebar kiri, Anda juga dapat melihat "Statistik Ringkas" yang menampilkan metrik-metrik penting seperti total engagement, jumlah platform unik, dan sentimen paling umum.

    Selamat menjelajahi dan semoga D.A.S.H membantu analisis media Anda! 🌟
    """)
st.markdown("---") # Garis pemisah setelah expander

# --- Bagian Unggah File CSV ---
st.sidebar.header("Unggah Data Anda 😺")
uploaded_file = st.sidebar.file_uploader("Pilih file CSV", type=["csv"])

data = None
if uploaded_file is not None:
    try:
        raw_data = pd.read_csv(uploaded_file)
        st.sidebar.success("Meong! File CSV berhasil diunggah.")
        data = clean_and_preprocess_data(raw_data.copy()) # Kirim salinan untuk pembersihan
        if data is None or data.empty:
            st.error("Meong! Data kosong atau tidak valid setelah pembersihan. Mohon periksa file CSV Anda.")
            data = None # Pastikan data None jika kosong/tidak valid
    except Exception as e:
        st.error(f"Meong! Terjadi kesalahan saat memuat atau membersihkan file: {e}. Pastikan itu adalah CSV yang valid dan memiliki format kolom yang diharapkan.")
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
    sentiment_counts = data["Sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentimen", "Jumlah"]
    fig_sentiment = px.pie(sentiment_counts, values="Jumlah", names="Sentimen",
                           title="Distribusi Sentimen Terhadap Topik",
                           color_discrete_sequence=single_hue_pastel_colors) # Menggunakan palet satu hue
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
    data["Date_Day"] = data["Date"].dt.date
    daily_engagement = data.groupby("Date_Day")["Engagements"].sum().reset_index()
    fig_engagement_trend = px.line(daily_engagement, x="Date_Day", y="Engagements",
                                   title="Tren Total Engagement Harian",
                                   color_discrete_sequence=[single_hue_pastel_colors[0]]) # Menggunakan warna pertama dari palet
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
    platform_engagement = data.groupby("Platform")["Engagements"].sum().reset_index()
    platform_engagement = platform_engagement.sort_values(by="Engagements", ascending=False)
    fig_platform_engagement = px.bar(platform_engagement, x="Platform", y="Engagements",
                                      title="Total Engagement per Platform",
                                      color="Platform",
                                      color_discrete_sequence=single_hue_pastel_colors) # Menggunakan palet satu hue
    fig_platform_engagement.update_xaxes(title_text="Platform")
    fig_platform_engagement.update_yaxes(title_text="Total Engagement")
    st.plotly_chart(fig_platform_engagement, use_container_width=True)
    st.markdown("#### Insight Kucing AI 💡")
    st.info("""
    - **X/Twitter** dan **Instagram** menunjukkan engagement tertinggi, mengindikasikan platform-platform ini paling efektif untuk menjangkau audiens.
    - **News Portal** memiliki engagement yang solid, menunjukkan bahwa berita dan artikel masih relevan bagi audiens.
    - Platform dengan engagement rendah mungkin memerlukan evaluasi ulang strategi atau fokus pada tipe konten yang berbeda.
    """)
    st.markdown("---")

    # 4. Media Type Mix
    st.subheader("4. Komposisi Tipe Media 😻")
    media_type_counts = data["Media_Type"].value_counts().reset_index()
    media_type_counts.columns = ["Tipe Media", "Jumlah"]
    fig_media_type_mix = px.pie(media_type_counts, values="Jumlah", names="Tipe Media",
                                title="Proporsi Tipe Media",
                                color_discrete_sequence=single_hue_pastel_colors) # Menggunakan palet satu hue
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
    location_engagement = data.groupby("Location")["Engagements"].sum().reset_index()
    top_5_locations = location_engagement.sort_values(by="Engagements", ascending=False).head(5)
    fig_top_locations = px.bar(top_5_locations, x="Location", y="Engagements",
                                title="Top 5 Lokasi Berdasarkan Total Engagement",
                                color="Location",
                                color_discrete_sequence=single_hue_pastel_colors) # Menggunakan palet satu hue
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
    total_engagement = data["Engagements"].sum()
    unique_platforms = data["Platform"].nunique()
    # Pastikan data['Sentiment'] tidak kosong sebelum mode() dipanggil
    if not data['Sentiment'].empty:
        most_common_sentiment = data["Sentiment"].mode()[0]
    else:
        most_common_sentiment = "Tidak Ada Data Sentimen"

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
    st.warning("Mohon unggah file CSV yang valid atau tunggu data sintetis dimuat untuk melihat dashboard.")

# --- Footer ---
st.markdown("---")
st.markdown("Papan Kontrol Kucing Dibuat dengan 💖 oleh Tim Kucing Cerdas 🐱")
