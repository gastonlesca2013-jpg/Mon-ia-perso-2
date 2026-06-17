import streamlit as st
import google.generativeai as genai
import json
import os
import socket

# --- CONFIGURATION ---
st.set_page_config(page_title="Kalyx", layout="wide")

# Fichier pour la persistance des données (pour que tout le monde voie la même chose)
DATA_FILE = "broadcast_data.json"

def load_broadcast():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f: return json.load(f)
        except: return {"msg": None, "img": None, "canicule": False}
    return {"msg": None, "img": None, "canicule": False}

def save_broadcast(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f)

# --- INITIALISATION ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_email" not in st.session_state: st.session_state.user_email = ""
if "page" not in st.session_state: st.session_state.page = "Parler à Cadix"

# --- LOGIN ---
if not st.session_state.logged_in:
    st.title("Connexion à Kalyx")
    email = st.text_input("Adresse Email")
    pwd = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if email:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.rerun()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.title("Kalyx")
    if st.button("💬 Parler à Cadix"): st.session_state.page = "Parler à Cadix"
    if st.button("🖼️ Générer Image"): st.session_state.page = "image"
    if st.button("📊 Activité"): st.session_state.page = "activity"
    if st.button("⚙️ Paramètres"): st.session_state.page = "settings"
    
    if st.session_state.user_email == "gastonlesca2013@gmail.com":
        st.divider()
        if st.button("👑 Panneau Admin"): st.session_state.page = "admin"
    st.divider()
    if st.button("Déconnexion"): st.session_state.logged_in = False; st.rerun()

# --- LAYOUT DROITE (MÉTÉO) ---
col_main, col_right = st.columns([0.8, 0.2])

with col_right:
    st.write("### ☀️ Météo")
    st.write("Aix-en-Provence: 28°C")
    st.write("État: Ensoleillé")

# --- CONTENU PRINCIPAL ---
with col_main:
    # Charger les infos broadcast
    b_data = load_broadcast()
    
    # Affichage de l'alerte Canicule si activée par l'admin
    if b_data.get("canicule"):
        st.image("https://img.freepik.com/vecteurs-premium/soleil-mignon-transpirant-buvant-verre-eau_825852-52.jpg", 
                 caption="ALERTE CANICULE ! Prenez soin de vous !")
    
    # Affichage message standard
    if b_data["msg"]: st.warning(f"📢 INFO: {b_data['msg']}")

    # --- PAGES ---
    if st.session_state.page == "Parler à Cadix":
        st.header("Parler à Cadix")
        if prompt := st.chat_input("Votre message..."):
            st.chat_message("user").markdown(prompt)
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel("gemini-1.5-pro")
                response = model.generate_content(prompt)
                st.chat_message("assistant").markdown(response.text)
            except: st.error("Erreur API. Vérifiez la clé dans les Secrets.")

    elif st.session_state.page == "admin":
        st.header("👑 Panneau Admin")
        new_msg = st.text_input("Message pour tous :")
        if st.button("Diffuser Message"):
            d = load_broadcast(); d["msg"] = new_msg; save_broadcast(d)
        
        # Le bouton Canicule
        if st.button("☀️ Activer Alerte Canicule"):
            d = load_broadcast(); d["canicule"] = True; save_broadcast(d)
            
        if st.button("Tout réinitialiser (Canicule + Message)"):
            save_broadcast({"msg": None, "img": None, "canicule": False})

    elif st.session_state.page == "image":
        st.header("Générer Image")
        query = st.text_input("Description :")
        if st.button("Rechercher"):
            st.image(f"https://image.pollinations.ai/prompt/{query}")

    elif st.session_state.page == "activity":
        st.header("Activité")
        st.write("Nombre de connexions enregistrées : 1 (Admin)")

    elif st.session_state.page == "settings":
        st.header("Paramètres")
        st.write(f"Email : {st.session_state.user_email}")
        st.write(f"IP : {socket.gethostbyname(socket.gethostname())}")

# --- FOND D'ÉCRAN ---
st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e");
        background-size: cover;
        background-attachment: fixed;
    }
    </style>
""", unsafe_allow_html=True)
