import streamlit as st
import google.generativeai as genai
import json
import os
from PIL import Image

# --- CONFIGURATION ---
st.set_page_config(page_title="Kalyx", layout="wide")

# Fichier pour la persistance (stockage local pour partager les infos)
DATA_FILE = "broadcast_data.json"
IMG_FILE = "shared_broadcast.png"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f: return json.load(f)
    return {"msg": "", "canicule": False, "show_img": False}

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f)

# --- INITIALISATION ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "right_bar" not in st.session_state: st.session_state.right_bar = True

# --- PAGE DE CONNEXION ---
if not st.session_state.logged_in:
    st.title("🔒 Connexion à Kalyx")
    email = st.text_input("Adresse Email")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter / S'inscrire"):
        if email and password:
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.title("Kalyx")
    page = st.radio("Navigation", ["Parler à Calix", "Générer Image", "Activité", "Paramètres", "Panneau Admin"])
    st.divider()
    if st.button("Déconnexion"): st.session_state.logged_in = False; st.rerun()

# --- LAYOUT PRINCIPAL ---
# On gère la barre de droite rétractable
col_main, col_right = st.columns([0.85 if st.session_state.right_bar else 1.0, 0.15 if st.session_state.right_bar else 0.01])

with col_right:
    if st.button("↔️"): st.session_state.right_bar = not st.session_state.right_bar; st.rerun()
    if st.session_state.right_bar:
        st.write("### ☀️ Météo")
        st.write("Aix-en-Provence : 28°C")

with col_main:
    data = load_data()
    
    # Alerte Canicule (Priorité haute)
    if data.get("canicule"):
        st.markdown("<h1 style='color:orange; text-align:center;'>🔥 ALERTE CANICULE !</h1>", unsafe_allow_html=True)
        st.image("https://img.freepik.com/vecteurs-premium/soleil-mignon-transpirant-buvant-verre-eau_825852-52.jpg")
        st.subheader("Hydratez-vous bien !")
    
    # Affichage Image partagée Admin
    if data.get("show_img") and os.path.exists(IMG_FILE):
        st.image(IMG_FILE, caption="Message de l'Admin")

    # --- PAGES ---
    if page == "Parler à Calix":
        st.header("Parler à Calix")
        if prompt := st.chat_input("Votre message..."):
            st.chat_message("user").markdown(prompt)
            # Logique IA ici...
            st.chat_message("assistant").markdown("Bonjour ! Je suis Calix.")

    elif page == "Panneau Admin":
        st.header("👑 Panneau Admin")
        
        # Upload Image pour tous
        uploaded_file = st.file_uploader("Envoyer une photo à tous :", type=['png', 'jpg'])
        if uploaded_file:
            with open(IMG_FILE, "wb") as f: f.write(uploaded_file.getbuffer())
            data["show_img"] = True; save_data(data)
            st.success("Photo diffusée !")
        
        # Bouton Canicule
        if st.button("☀️ Activer Alerte Canicule"):
            data["canicule"] = True; save_data(data); st.rerun()
            
        if st.button("🛑 Tout réinitialiser"):
            save_data({"msg": "", "canicule": False, "show_img": False})
            if os.path.exists(IMG_FILE): os.remove(IMG_FILE)
            st.rerun()

# --- FOND D'ÉCRAN (FIXE) ---
st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e");
        background-size: cover;
        background-attachment: fixed;
    }
    </style>
""", unsafe_allow_html=True)
