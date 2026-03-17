import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="EduAI - Chat Belajar Pintar",
    page_icon="🤖",
    layout="centered"
)

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Konfigurasi API Key bermasalah.")
    st.stop()

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .chat-bubble { padding: 15px; border-radius: 15px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Aku EduAI. Materi apa yang ingin kamu diskusikan atau buatkan analoginya hari ini?"}
    ]

st.title("🤖 EduAI: Smart Tutor")
st.caption("Asisten belajar dengan analogi cerdas. Riwayat chat ini hanya bisa dilihat olehmu.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Tanyakan sesuatu (Contoh: Apa itu Mitosis?)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Sedang berpikir..."):
            try:
                system_context = (
                    "Kamu adalah EduAI, asisten belajar SMA. "
                    "Gunakan bahasa santai, berikan analogi, dan jelaskan poin per poin. "
                    "Gunakan riwayat chat sebelumnya jika relevan."
                )
                chat = model.start_chat(history=[])
                full_prompt = f"{system_context}\n\nRiwayat Chat:\n{st.session_state.messages}\n\nUser baru saja bertanya: {prompt}"
                
                response = model.generate_content(full_prompt)
                full_response = response.text
                
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"Gagal mendapatkan respon: {e}")
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = [{"role": "assistant", "content": "Riwayat dihapus. Ada yang bisa kubantu lagi?"}]
    st.rerun()