import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(
    page_title="EduAI - Interactive Learning Companion",
    page_icon="🤖",
    layout="centered"
)

st.markdown("""
    <style>
    /* Mengatur background dan font */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Styling Judul Utama */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(#00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
    }
    
    /* Styling Subtitle */
    .sub-title {
        text-align: center;
        color: #a0a0a0;
        margin-bottom: 30px;
    }

    /* Styling Kotak Hasil AI */
    .res-box {
        background-color: #1e2130;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #4facfe;
        margin-top: 20px;
        line-height: 1.6;
    }

    /* Input Field Styling */
    .stTextInput > div > div > input {
        background-color: #262730;
        color: white;
        border-radius: 10px;
        border: 1px solid #4facfe;
    }
    </style>
""", unsafe_allow_html=True)

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("API Key tidak ditemukan. Pastikan sudah menyetel Secret Management.")
    st.stop()

def get_ai_response(user_query):
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    system_instruction = (
        "Anda adalah EduAI, asisten belajar untuk siswa SMA di Indonesia. "
        "Tugas Anda adalah menjelaskan konsep materi yang ditanyakan dengan: "
        "1. Bahasa yang mudah dipahami (santai tapi sopan). "
        "2. Gunakan analogi kehidupan sehari-hari yang relevan dengan anak muda. "
        "3. Berikan poin-poin penjelasan yang jelas. "
        "4. Berikan satu contoh soal singkat di akhir. "
        "Gunakan format Markdown yang rapi."
    )
    
    response = model.generate_content(f"{system_instruction}\n\nPertanyaan Siswa: {user_query}")
    return response.text

st.markdown('<h1 class="main-title">EduAI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Ubah materi sulit jadi analogi yang asyik!</p>', unsafe_allow_html=True)

with st.container():
    topic = st.text_input("Apa yang ingin kamu pelajari hari ini?", placeholder="Misal: Hukum Termodinamika atau Mitosis")
    btn_tanya = st.button("Jelaskan Sekarang ✨")

if btn_tanya:
    if topic:
        with st.spinner('Sedang merangkai analogi cerdas untukmu...'):
            try:
                hasil_penjelasan = get_ai_response(topic)
                st.markdown(f'<div class="res-box">{hasil_penjelasan}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
    else:
        st.warning("Masukkan topik materi terlebih dahulu ya!")

st.markdown("---")
st.caption("EduAI Project - Tugas Informatika Kelas 12 | Built with Streamlit & Gemini 2.5 Flash")