import streamlit as st
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, firestore
import json

# --- 1. INISIALISASI FIREBASE (DATABASE) ---
# Mengambil file JSON dari Streamlit Secrets
if not firebase_admin._apps:
    key_dict = json.loads(st.secrets["FIREBASE_JSON"]) # Kita simpan isi file JSON di Secrets nanti
    cred = credentials.Certificate(key_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# --- 2. KONFIGURASI AI ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 3. UI LOGIN SEDERHANA (Agar Chat Tidak Tercampur) ---
st.set_page_config(page_title="EduAI Persistent", layout="centered")

st.sidebar.title("🔑 Akses Belajar")
user_id = st.sidebar.text_input("Masukkan Username/ID kamu:", placeholder="Contoh: budi_keren")

if not user_id:
    st.info("Silakan masukkan Username di samping untuk melihat riwayat chat kamu.")
    st.stop() # Berhenti di sini jika belum isi username

# --- 4. FUNGSI DATABASE (AMBIL & SIMPAN DATA) ---
def load_chat_history(uid):
    # Mengambil chat dari koleksi 'chats' di Firebase berdasarkan user_id
    doc_ref = db.collection("chats").document(uid)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get("messages", [])
    return [{"role": "assistant", "content": f"Halo {uid}! Senang bertemu kembali. Mau tanya materi apa hari ini?"}]

def save_chat_history(uid, messages):
    # Menyimpan/Update chat ke Firebase
    db.collection("chats").document(uid).set({"messages": messages})

# --- 5. LOGIKA CHAT ---
# Load chat saat user ID dimasukkan
if "messages" not in st.session_state or st.session_state.get("current_user") != user_id:
    st.session_state.messages = load_chat_history(user_id)
    st.session_state.current_user = user_id

st.title(f"🤖 EduAI: Ruang Belajar {user_id}")

# Tampilkan chat lama
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input chat baru
if prompt := st.chat_input("Tanyakan materi sekolah..."):
    # Simpan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respon AI
    with st.chat_message("assistant"):
        with st.spinner("Mencari analogi..."):
            system_context = "Kamu EduAI, asisten belajar SMA. Gunakan analogi."
            # Kirim semua riwayat ke AI
            response = model.generate_content(f"{system_context}\n\nHistory: {st.session_state.messages}")
            full_response = response.text
            st.markdown(full_response)
            
            # Simpan pesan AI
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
            # SIMPAN PERMANEN KE DATABASE
            save_chat_history(user_id, st.session_state.messages)

if st.sidebar.button("Hapus Riwayat"):
    db.collection("chats").document(user_id).delete()
    st.rerun()