import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from openai import OpenAI # Import OpenAI SDK
from fpdf import FPDF # Import FPDF untuk membuat PDF

# --- Konfigurasi Halaman Streamlit ---
# Mengatur judul halaman, ikon, dan layout.
st.set_page_config(
    page_title="Papan Kontrol Intelijen Media Kucing 🐾",
    page_icon="🐱", # Ikon kucing yang lucu
    layout="wide", # Layout lebar untuk tampilan dashboard yang lebih baik
    initial_sidebar_state="expanded" # Sidebar dibuka secara default
)

# --- CSS Kustom untuk Tema Kucing dan Warna Pastel (Satu Hue: Orange/Brown) ---
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
            text_align: center;
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

# --- AI Integration Function ---
@st.cache_data(show_spinner="Kucing AI sedang berpikir... 🧠")
def get_ai_insight(model_name, api_key, prompt_text, chart_data_str):
    """
    Generates AI insights using OpenRouter AI.
    """
    if not api_key:
        return "Insight AI requires OpenRouter API Key. Please enter it in the sidebar."

    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a media intelligence expert. Provide concise and actionable insights (max 3 key insights) based on the provided data, relevant to media production or content strategy. Focus on key findings, emerging trends, or data anomalies. Output should be a bulleted list."},
                {"role": "user", "content": f"{prompt_text}\n\nData for analysis:\n{chart_data_str}"}
            ],
            temperature=0.7,
            max_tokens=200,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Meong! Failed to get AI insight: {e}"

# --- Function to Generate PDF Report ---
def generate_pdf_report(data, insights):
    """
    Generates a PDF report containing dashboard overview and AI insights.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Laporan Intelijen Media D.A.S.H", 0, 1, "C")
    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    pdf.multi_cell(0, 10, "Laporan ini merangkum analisis data media dari dashboard D.A.S.H, termasuk visualisasi kunci dan insight yang dihasilkan AI.")
    pdf.ln(10)

    # Section for overall statistics
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Statistik Ringkas:", 0, 1, "L")
    pdf.set_font("Arial", "", 12)
    
    # Calculate stats from data
    total_engagement = data["Engagements"].sum()
    unique_platforms = data["Platform"].nunique()
    most_common_sentiment = data["Sentiment"].mode()[0] if not data["Sentiment"].empty else "Tidak Ada Data Sentimen"
    
    pdf.multi_cell(0, 7, f"- Total Engagement: {total_engagement:,}")
    pdf.multi_cell(0, 7, f"- Platform Unik: {unique_platforms}")
    pdf.multi_cell(0, 7, f"- Sentimen Paling Umum: {most_common_sentiment}")
    pdf.ln(10)

    # Sections for each visualization and its AI insights
    charts_and_insights_mapping = {
        "Sebaran Sentimen (Sentiment Breakdown)": insights.get("sentiment", "Tidak ada insight."),
        "Tren Engagement dari Waktu ke Waktu": insights.get("engagement_trend", "Tidak ada insight."),
        "Engagement Berdasarkan Platform": insights.get("platform_engagement", "Tidak ada insight."),
        "Komposisi Tipe Media": insights.get("media_type_mix", "Tidak ada insight."),
        "5 Lokasi Teratas Berdasarkan Engagement": insights.get("top_locations", "Tidak ada insight."),
    }

    for title, insight_text in charts_and_insights_mapping.items():
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"Visualisasi: {title}", 0, 1, "L")
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 7, "Insight AI:")
        if isinstance(insight_text, str) and insight_text.strip() and "Meong! Failed to get AI insight" not in insight_text:
            # Add some padding or formatting for insights
            pdf.set_left_margin(pdf.get_x() + 10) # Indent
            # FPDF has basic text rendering. Bullet points might need manual handling if the AI generates unicode bullets.
            # For simplicity, just print the text.
            pdf.multi_cell(0, 7, insight_text)
            pdf.set_left_margin(10) # Reset indent
        else:
            pdf.multi_cell(0, 7, "Tidak ada insight AI yang tersedia atau ada kesalahan dalam menghasilkan insight.")
        pdf.ln(10)

    # Output the PDF as bytes
    return pdf.output(dest='S').encode('latin-1') # Use latin-1 for byte representation


# --- Application Header ---
st.title("🐾 D.A.S.H: Data Analysis & Smart Highlighting 🐾")
st.markdown("Selamat datang di papan kontrol intelijen media Anda! Unggah data Anda dan biarkan kucing-kucing kami menganalisisnya untuk insight media yang menggemaskan.")

# --- How to Use Section ---
with st.expander("❓ Cara Menggunakan Dashboard Ini 🐾"):
    st.markdown("""
    Dashboard **D.A.S.H (Data Analysis & Smart Highlighting)** dirancang untuk membantu Anda mendapatkan insight dari data media Anda dengan mudah. Ikuti langkah-langkah berikut untuk memulai:

    1.  **Unggah Data Anda:**
        * Di sidebar kiri, cari bagian "Unggah Data Anda 😺".
        * Klik tombol "Pilih file CSV" dan unggah file CSV Anda.
        * **Pastikan file CSV Anda memiliki kolom-kolom berikut:** `Date`, `Platform`, `Sentiment`, `Location`, `Engagements`, `Media_Type`.
        * Setelah berhasil diunggah, Anda akan melihat status pembersihan data di sidebar. Jika ada masalah, pesan error akan muncul.

    2.  **Jelajahi Pratinjau Data:**
        * Setelah data berhasil dimuat dan dibersihkan, Anda akan melihat tabel "Pratinjau Data Kucing" yang menampilkan beberapa baris pertama dari dataset Anda. Ini memastikan data sudah siap untuk analisis.

    3.  **Konfigurasi AI:**
        * Di sidebar kiri, masukkan **OpenRouter API Key** Anda.
        * Pilih model AI yang ingin Anda gunakan.

    4.  **Analisis Visualisasi Interaktif:**
        * Gulir ke bawah untuk melihat berbagai chart interaktif yang menampilkan insight penting dari data Anda.
        * Setiap chart dirancang untuk memberikan gambaran cepat tentang aspek tertentu dari kinerja media Anda (misalnya, distribusi sentimen, tren engagement, kinerja platform).
        * Anda bisa mengarahkan kursor ke elemen-elemen chart untuk melihat detail lebih lanjut (fitur interaktif Plotly).

    5.  **Dapatkan Insight dari Kucing AI:**
        * Di bawah setiap chart, Anda akan menemukan bagian "Insight Kucing AI 💡" yang berisi rangkuman naratif dari temuan penting, tren yang muncul, atau anomali data. Insight ini dihasilkan secara dinamis oleh model AI yang Anda pilih.

    6.  **Periksa Statistik Ringkas:**
        * Di sidebar kiri, Anda juga dapat melihat "Statistik Ringkas" yang menampilkan metrik-metrik penting seperti total engagement, jumlah platform unik, dan sentimen paling umum.

    Selamat menjelajahi dan semoga D.A.S.H membantu analisis media Anda! 🌟
    """)
st.markdown("---")

# --- Bagian Unggah File CSV ---
st.sidebar.header("Unggah Data Anda 😺")
uploaded_file = st.sidebar.file_uploader("Pilih file CSV", type=["csv"])

data = None
if uploaded_file is not None:
    try:
        raw_data = pd.read_csv(uploaded_file)
        st.sidebar.success("Meong! File CSV berhasil diunggah.")
        data = clean_and_preprocess_data(raw_data.copy())
        if data is None or data.empty:
            st.error("Meong! Data kosong atau tidak valid setelah pembersihan. Mohon periksa file CSV Anda.")
            data = None
    except Exception as e:
        st.error(f"Meong! Terjadi kesalahan saat memuat atau membersihkan file: {e}. Pastikan itu adalah CSV yang valid dan memiliki format kolom yang diharapkan.")
        data = None
else:
    st.sidebar.info("Tidak ada file yang diunggah. Menggunakan data sintetis untuk demo.")
    data = create_synthetic_data()

# --- AI Configuration in Sidebar ---
st.sidebar.header("Konfigurasi AI 🧠")
openrouter_api_key = st.sidebar.text_input(
    "OpenRouter API Key",
    type="password",
    help="Dapatkan kunci API Anda dari OpenRouter.ai (gratis untuk sebagian besar model).",
    value=st.secrets.get("OPENROUTER_API_KEY", "")
)
if not openrouter_api_key:
    st.sidebar.warning("Masukkan OpenRouter API Key Anda di atas untuk mengaktifkan insight AI.")

ai_model = st.sidebar.selectbox(
    "Pilih Model AI",
    ["google/gemini-pro", "openai/gpt-3.5-turbo", "mistralai/mistral-7b-instruct"],
    help="Pilih model AI yang akan digunakan untuk menghasilkan insight. Model 'google/gemini-pro' atau 'openai/gpt-3.5-turbo' disarankan."
)

# Initialize a dictionary to store all AI insights
all_insights = {}

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
                           color_discrete_sequence=single_hue_pastel_colors)
    fig_sentiment.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig_sentiment, use_container_width=True)
    st.markdown("#### Insight Kucing AI 💡")
    
    prompt_sentiment = (
        "Analyze the sentiment distribution data provided below. "
        "Provide 3 concise and actionable key insights relevant to media production or content strategy. "
        "Highlight the dominant sentiment, implications of negative sentiment, and opportunities related to neutral sentiment. "
        "Format insights as a bulleted list."
    )
    sentiment_data_str = sentiment_counts.to_string(index=False)
    ai_insight_sentiment = get_ai_insight(ai_model, openrouter_api_key, prompt_sentiment, sentiment_data_str)
    st.info(ai_insight_sentiment)
    all_insights["sentiment"] = ai_insight_sentiment # Store insight
    st.markdown("---")

    # 2. Engagement Trend Over Time
    st.subheader("2. Tren Engagement dari Waktu ke Waktu 🐾")
    data["Date_Day"] = data["Date"].dt.date
    daily_engagement = data.groupby("Date_Day")["Engagements"].sum().reset_index()
    fig_engagement_trend = px.line(daily_engagement, x="Date_Day", y="Engagements",
                                   title="Tren Total Engagement Harian",
                                   color_discrete_sequence=[single_hue_pastel_colors[0]])
    fig_engagement_trend.update_xaxes(title_text="Tanggal")
    fig_engagement_trend.update_yaxes(title_text="Total Engagement")
    st.plotly_chart(fig_engagement_trend, use_container_width=True)
    st.markdown("#### Insight Kucing AI 💡")

    prompt_engagement_trend = (
        "Analyze the daily engagement trend data. "
        "Provide 3 concise and actionable key insights for media content strategy. "
        "Identify significant peaks or drops, discuss potential causes, and suggest actions for consistent engagement. "
        "Focus on content performance over time. Format insights as a bulleted list."
    )
    engagement_trend_data_str = daily_engagement.to_string(index=False)
    ai_insight_engagement_trend = get_ai_insight(ai_model, openrouter_api_key, prompt_engagement_trend, engagement_trend_data_str)
    st.info(ai_insight_engagement_trend)
    all_insights["engagement_trend"] = ai_insight_engagement_trend # Store insight
    st.markdown("---")

    # 3. Platform Engagements
    st.subheader("3. Engagement Berdasarkan Platform 😺")
    platform_engagement = data.groupby("Platform")["Engagements"].sum().reset_index()
    platform_engagement = platform_engagement.sort_values(by="Engagements", ascending=False)
    fig_platform_engagement = px.bar(platform_engagement, x="Platform", y="Engagements",
                                      title="Total Engagement per Platform",
                                      color="Platform",
                                      color_discrete_sequence=single_hue_pastel_colors)
    fig_platform_engagement.update_xaxes(title_text="Platform")
    fig_platform_engagement.update_yaxes(title_text="Total Engagement")
    st.plotly_chart(fig_platform_engagement, use_container_width=True)
    st.markdown("#### Insight Kucing AI 💡")

    prompt_platform_engagement = (
        "Analyze the engagement performance across different platforms. "
        "Provide 3 concise and actionable key insights for platform-specific content strategy. "
        "Identify top-performing platforms, underperforming ones, and suggest content adaptations for each. "
        "Format insights as a bulleted list."
    )
    platform_engagement_data_str = platform_engagement.to_string(index=False)
    ai_insight_platform_engagement = get_ai_insight(ai_model, openrouter_api_key, prompt_platform_engagement, platform_engagement_data_str)
    st.info(ai_insight_platform_engagement)
    all_insights["platform_engagement"] = ai_insight_platform_engagement # Store insight
    st.markdown("---")

    # 4. Media Type Mix
    st.subheader("4. Komposisi Tipe Media 😻")
    media_type_counts = data["Media_Type"].value_counts().reset_index()
    media_type_counts.columns = ["Tipe Media", "Jumlah"]
    fig_media_type_mix = px.pie(media_type_counts, values="Jumlah", names="Tipe Media",
                                title="Proporsi Tipe Media",
                                color_discrete_sequence=single_hue_pastel_colors)
    fig_media_type_mix.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig_media_type_mix, use_container_width=True)
    st.markdown("#### Insight Kucing AI 💡")

    prompt_media_type_mix = (
        "Analyze the proportion of different media types in the content. "
        "Provide 3 concise and actionable key insights relevant to content format preferences. "
        "Highlight dominant media types, suggest opportunities for less used types, and discuss content format strategy. "
        "Format insights as a bulleted list."
    )
    media_type_data_str = media_type_counts.to_string(index=False)
    ai_insight_media_type_mix = get_ai_insight(ai_model, openrouter_api_key, prompt_media_type_mix, media_type_data_str)
    st.info(ai_insight_media_type_mix)
    all_insights["media_type_mix"] = ai_insight_media_type_mix # Store insight
    st.markdown("---")

    # 5. Top 5 Locations by Engagement
    st.subheader("5. 5 Lokasi Teratas Berdasarkan Engagement 🌍")
    location_engagement = data.groupby("Location")["Engagements"].sum().reset_index()
    top_5_locations = location_engagement.sort_values(by="Engagements", ascending=False).head(5)
    fig_top_locations = px.bar(top_5_locations, x="Location", y="Engagements",
                                title="Top 5 Lokasi Berdasarkan Total Engagement",
                                color="Location",
                                color_discrete_sequence=single_hue_pastel_colors)
    fig_top_locations.update_xaxes(title_text="Lokasi")
    fig_top_locations.update_yaxes(title_text="Total Engagement")
    st.plotly_chart(fig_top_locations, use_container_width=True)
    st.markdown("#### Insight Kucing AI 💡")

    prompt_top_locations = (
        "Analyze the top 5 geographical locations by engagement. "
        "Provide 3 concise and actionable key insights relevant to audience targeting or local content production. "
        "Identify the most engaged regions, discuss potential reasons for their high engagement, and suggest localized strategies. "
        "Format insights as a bulleted list."
    )
    top_locations_data_str = top_5_locations.to_string(index=False)
    ai_insight_top_locations = get_ai_insight(ai_model, openrouter_api_key, prompt_top_locations, top_locations_data_str)
    st.info(ai_insight_top_locations)
    all_insights["top_locations"] = ai_insight_top_locations # Store insight
    st.markdown("---")

    # Tambahkan metrik umum di sidebar
    st.sidebar.subheader("Statistik Ringkas 📈")
    total_engagement = data["Engagements"].sum()
    unique_platforms = data["Platform"].nunique()
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

    # --- Download PDF Button ---
    st.markdown("---")
    st.subheader("Unduh Laporan 📥")
    # Hanya aktifkan tombol unduh jika API key tersedia dan data tidak kosong
    # Dan pastikan semua insight AI sudah ada (meskipun mungkin ada error internal di insight itu sendiri)
    if openrouter_api_key and data is not None and not data.empty and all(k in all_insights for k in ["sentiment", "engagement_trend", "platform_engagement", "media_type_mix", "top_locations"]):
        pdf_bytes = generate_pdf_report(data, all_insights)
        st.download_button(
            label="Unduh Laporan PDF 📄",
            data=pdf_bytes,
            file_name="Laporan_Intelijen_Media_DASH.pdf",
            mime="application/pdf",
            help="Unduh laporan ringkas dalam format PDF yang berisi insight AI."
        )
    else:
        st.info("Masukkan OpenRouter API Key dan unggah data untuk mengaktifkan fitur unduh laporan PDF.")


else:
    st.warning("Mohon unggah file CSV yang valid atau tunggu data sintetis dimuat untuk melihat dashboard.")

# --- Footer ---
st.markdown("---")
st.markdown("Papan Kontrol Kucing Dibuat dengan 💖 oleh Tim Kucing Cerdas 🐱")
