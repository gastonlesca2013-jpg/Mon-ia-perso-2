import streamlit as st
import google.generativeai as genai
import os
import json

# --- CONFIGURATION ---
st.set_page_config(page_title="Kalyx", layout="wide")
DATA_FILE = "app_data.json"

# --- GESTION DES DONNÉES (ADMIN) ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f: return json.load(f)
    return {"msg": "", "alert": False}

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f)

# --- SESSION ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "email" not in st.session_state: st.session_state.email = ""
if "page" not in st.session_state: st.session_state.page = "Parler à Kalix"
if "right_bar" not in st.session_state: st.session_state.right_bar = True

# --- LOGIN ---
if not st.session_state.logged_in:
    st.title("🔒 Connexion")
    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if email == "gastonlesca2013@gmail.com" and password == "Napoléon 2013 !":
            st.session_state.logged_in = True
            st.session_state.email = email
            st.rerun()
        elif email and password:
            st.session_state.logged_in = True
            st.session_state.email = email
            st.rerun()
    st.stop()

# --- SIDEBAR GAUCHE ---
with st.sidebar:
    st.title("Kalyx")
    if st.button("💬 Parler à Kalix"): st.session_state.page = "Parler à Kalix"
    if st.button("🖼️ Générer Image"): st.session_state.page = "image"
    if st.button("📊 Activité"): st.session_state.page = "activity"
    if st.button("⚙️ Paramètres"): st.session_state.page = "settings"
    
    if st.session_state.email == "gastonlesca2013@gmail.com":
        st.divider()
        if st.button("👑 Panneau Admin"): st.session_state.page = "admin"
    
    st.divider()
    if st.button("🚪 Déconnexion"): st.session_state.logged_in = False; st.rerun()

# --- STYLE ---
st.markdown("""<style>.stApp { background: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e'); background-size: cover; }</style>""", unsafe_allow_html=True)

# --- LAYOUT (MAIN + SIDEBAR DROITE RÉTRACTABLE) ---
col_main, col_right = st.columns([0.8 if st.session_state.right_bar else 1.0, 0.2 if st.session_state.right_bar else 0.05])

with col_right:
    if st.button("↔️"): st.session_state.right_bar = not st.session_state.right_bar; st.rerun()
    if st.session_state.right_bar:
        st.write("### ☀️ Infos")
        st.write("Aix-en-Provence : 25°C")

with col_main:
    data = load_data()
    if data["alert"]: st.warning("🔥 ALERTE CANICULE EN COURS")
    if data["msg"]: st.info(f"📢 Admin: {data['msg']}")

    # ROUTAGE PAGES
    if st.session_state.page == "Parler à Kalix":
        st.header("Parler à Kalix")
        if prompt := st.chat_input("Votre message..."):
            st.chat_message("user").markdown(prompt)
            try:
                # Utilisation de gemini-pro (stable)
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt)
                st.chat_message("assistant").markdown(response.text)
            except Exception as e:
                st.error(f"Erreur IA : {e}")

    elif st.session_state.page == "admin" and st.session_state.email == "gastonlesca2013@gmail.com":
        st.header("👑 Panneau Admin")
        new_msg = st.text_input("Diffuser message :")
        if st.button("Diffuser"): data["msg"] = new_msg; save_data(data)
        if st.button("Alerte Canicule"): data["alert"] = True; save_data(data)
        if st.button("Réinitialiser tout"): save_data({"msg": "", "alert": False})

    elif st.session_state.page == "image":
        st.header("Générer Image")
        q = st.text_input("Description :")
        if st.button("Générer"): st.image(f"https://image.pollinations.ai/prompt/{q}")
    
    elif st.session_state.page == "activity":
        st.header("Activité")
        st.write(f"Utilisateur : {st.session_state.email}")
