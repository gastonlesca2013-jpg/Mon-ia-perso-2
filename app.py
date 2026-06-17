import streamlit as st
import google.generativeai as genai
import json
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="Kalyx", layout="wide")

# Fichier pour la persistance des données
DATA_FILE = "broadcast_data.json"

def load_broadcast():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f: return json.load(f)
        except: return {"msg": None, "img": None}
    return {"msg": None, "img": None}

def save_broadcast(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f)

# --- INITIALISATION ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_email" not in st.session_state: st.session_state.user_email = ""
if "page" not in st.session_state: st.session_state.page = "chat"
if "sidebar_visible" not in st.session_state: st.session_state.sidebar_visible = True

# --- LOGIQUE IA ---
def get_ai_response(prompt):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-pro") 
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erreur : {str(e)}"

# --- CONNEXION ---
if not st.session_state.logged_in:
    st.title("Connexion à Kalyx")
    email = st.text_input("Email")
    if st.button("Se connecter"):
        st.session_state.logged_in = True
        st.session_state.user_email = email
        st.rerun()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.title("Kalyx")
    if st.button("💬 Monia / Chat"): st.session_state.page = "chat"
    if st.button("🖼️ Générer Image"): st.session_state.page = "image"
    if st.button("📊 Activité"): st.session_state.page = "activity"
    if st.button("⚙️ Paramètres"): st.session_state.page = "settings"
    
    if st.session_state.user_email == "gastonlesca2013@gmail.com":
        st.divider()
        if st.button("👑 Panneau Admin"): st.session_state.page = "admin"

# --- LAYOUT ---
main_col, right_col = st.columns([0.8, 0.2 if st.session_state.sidebar_visible else 0.01])

with right_col:
    if st.button("↔️"): st.session_state.sidebar_visible = not st.session_state.sidebar_visible; st.rerun()
    if st.session_state.sidebar_visible:
        st.write("### Infos")
        st.write(f"Utilisateur: {st.session_state.user_email}")

with main_col:
    b_data = load_broadcast()
    if b_data["msg"]: st.warning(f"📢 INFO: {b_data['msg']}")
    if b_data["img"]: st.image(b_data["img"], caption="Alerte Admin")

    if st.session_state.page == "chat":
        st.header("Kalyx vous écoute")
        if prompt := st.chat_input("Dites quelque chose à Monia..."):
            st.chat_message("user").markdown(prompt)
            reponse = get_ai_response(prompt)
            st.chat_message("assistant").markdown(reponse)

    elif st.session_state.page == "admin":
        st.header("👑 Panneau Admin")
        new_msg = st.text_input("Message pour tous :")
        if st.button("Diffuser Message"):
            d = load_broadcast(); d["msg"] = new_msg; save_broadcast(d)
        if st.button("🔥 Alerte CANICULE"):
            d = load_broadcast(); d["img"] = "https://images.unsplash.com/photo-1530521954074-e64f6810b32d"; save_broadcast(d)
        if st.button("Tout réinitialiser"):
            save_broadcast({"msg": None, "img": None})

    elif st.session_state.page == "image":
        st.header("Générer Image")
        query = st.text_input("Description :")
        if st.button("Rechercher"):
            st.image(f"https://image.pollinations.ai/prompt/{query}")

# --- FOND D'ÉCRAN (FIXE) ---
st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    </style>
""", unsafe_allow_html=True)
