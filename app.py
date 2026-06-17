import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Kalyx", layout="wide")

# Fichier pour la persistance des données Admin (pour que tout le monde voie la même chose)
DATA_FILE = "broadcast_data.json"
IMG_FILE = "shared_broadcast.png"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f: return json.load(f)
        except: pass
    return {"msg": "", "canicule": False, "show_img": False}

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f)

# --- INITIALISATION SESSION ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "page" not in st.session_state: st.session_state.page = "Parler à Kalix"
if "right_bar" not in st.session_state: st.session_state.right_bar = True

# --- PAGE DE CONNEXION ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>Bienvenue sur Kalyx</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("### Veuillez vous identifier")
        email = st.text_input("Adresse Email")
        password = st.text_input("Mot de passe", type="password")
        if st.button("Se connecter / S'inscrire"):
            if email and password:
                st.session_state.logged_in = True
                st.rerun()
    st.stop()

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("Kalyx")
    if st.button("💬 Parler à Kalix"): st.session_state.page = "Parler à Kalix"
    if st.button("🖼️ Générer une image"): st.session_state.page = "image"
    if st.button("📊 Activité"): st.session_state.page = "activity"
    if st.button("⚙️ Paramètres"): st.session_state.page = "settings"
    st.divider()
    if st.button("👑 Panneau Admin"): st.session_state.page = "admin"
    st.divider()
    if st.button("🚪 Déconnexion"): st.session_state.logged_in = False; st.rerun()

# --- LAYOUT PRINCIPAL & BARRE RÉTRACTABLE ---
# Utilisation de colonnes dynamiques
width_main = 0.85 if st.session_state.right_bar else 1.0
width_right = 0.15 if st.session_state.right_bar else 0.01

col_main, col_right = st.columns([width_main, width_right])

with col_right:
    if st.button("↔️"): st.session_state.right_bar = not st.session_state.right_bar; st.rerun()
    if st.session_state.right_bar:
        st.write("### ☀️ Météo")
        st.write(datetime.now().strftime("%d/%m/%Y"))
        st.write("Aix-en-Provence : 28°C")

with col_main:
    data = load_data()
    
    # --- ALERTE CANICULE ---
    if data.get("canicule"):
        st.markdown("<h1 style='color:orange; text-align:center;'>🔥 ALERTE CANICULE !</h1>", unsafe_allow_html=True)
        st.image("https://img.freepik.com/vecteurs-premium/soleil-mignon-transpirant-buvant-verre-eau_825852-52.jpg")
        st.subheader("Hydratez-vous bien !")
    
    # --- AFFICHAGE IMAGE DIFFUSÉE ---
    if data.get("show_img") and os.path.exists(IMG_FILE):
        st.image(IMG_FILE, caption="Message important")

    # --- ROUTAGE DES PAGES ---
    if st.session_state.page == "Parler à Kalix":
        st.header("Parler à Kalix")
        if prompt := st.chat_input("Votre message..."):
            st.chat_message("user").markdown(prompt)
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                st.chat_message("assistant").markdown(response.text)
            except: st.error("Erreur de connexion avec l'IA. Vérifiez votre clé API.")

    elif st.session_state.page == "admin":
        st.header("👑 Panneau Admin")
        # Broadcast Message
        new_msg = st.text_input("Message à diffuser :")
        if st.button("Diffuser Message"): data["msg"] = new_msg; save_data(data)
        
        # Image Upload
        up = st.file_uploader("Image à diffuser", type=['png', 'jpg'])
        if up: 
            with open(IMG_FILE, "wb") as f: f.write(up.getbuffer())
            data["show_img"] = True; save_data(data)
        
        # Canicule Button
        if st.button("☀️ Activer Alerte Canicule"): data["canicule"] = True; save_data(data); st.rerun()
        if st.button("🛑 Tout réinitialiser"): save_data({"canicule": False, "show_img": False}); st.rerun()

    elif st.session_state.page == "image":
        st.header("Générer une image")
        if q := st.text_input("Description :"):
            if st.button("Générer"): st.image(f"https://image.pollinations.ai/prompt/{q}")

    # (Autres pages : Activité, Paramètres...)

# --- CSS FOND D'ÉCRAN ---
st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e");
        background-size: cover;
    }
    </style>
""", unsafe_allow_html=True)
