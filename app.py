import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="EduAI - Chat Belajar Pintar",
    page_icon="🤖",
    layout="centered"
)

# --- INTEGRASI API ---
try:
    # Ambil API Key dari Streamlit Secrets
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error("Konfigurasi API Key bermasalah.")
    st.stop()

# --- CSS CUSTOM UNTUK TAMPILAN CHAT ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .chat-bubble { padding: 15px; border-radius: 15px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- INISIALISASI SESSION STATE (TEMPAT MENYIMPAN RIWAYAT) ---
# Kode ini memastikan riwayat chat tersimpan selama tab browser tidak direfresh/tutup
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Aku EduAI. Materi apa yang ingin kamu diskusikan hari ini?"}
    ]

# --- TAMPILAN HEADER ---
st.title("🤖 EduAI: Asisten Belajar")
st.caption("Dibuat oleh Albertus Kevin Tandiono XII-1/2 & Satrio Wicaksono Agung Wibowo XII-1/33")

# --- MENAMPILKAN RIWAYAT CHAT ---
# Loop untuk menampilkan semua pesan yang tersimpan di session_state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- INPUT CHAT ---
if prompt := st.chat_input("Tanyakan sesuatu (Contoh: Apa itu Mitosis?)"):
    
    # 1. Tambahkan pesan user ke riwayat
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 2. Tampilkan pesan user di layar
    with st.chat_message("user"):
        st.markdown(prompt)

    # 3. Proses Jawaban dari AI
    with st.chat_message("assistant"):
        with st.spinner("Sedang berpikir..."):
            try:
                # Instruksi sistem agar AI tetap konsisten pada perannya
                system_context = (
                    "Kamu adalah EduAI, asisten belajar SMA. "
                    "Gunakan bahasa santai, berikan analogi, dan jelaskan poin per poin. "
                    "Gunakan riwayat chat sebelumnya jika relevan."
                )
                
                # Mengirim seluruh riwayat chat agar AI punya konteks pembicaraan sebelumnya
                # Gemini start_chat memudahkan pengelolaan history
                chat = model.start_chat(history=[])
                full_prompt = f"{system_context}\n\nRiwayat Chat:\n{st.session_state.messages}\n\nUser baru saja bertanya: {prompt}"
                
                response = model.generate_content(full_prompt)
                full_response = response.text
                
                st.markdown(full_response)
                
                # 4. Tambahkan jawaban AI ke riwayat agar tersimpan
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"Gagal mendapatkan respon: {e}")

# Tombol untuk Hapus Riwayat (Opsional)
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = [{"role": "assistant", "content": "Riwayat dihapus. Ada yang bisa kubantu lagi?"}]
    st.rerun()