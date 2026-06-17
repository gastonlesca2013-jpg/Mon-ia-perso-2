import streamlit as st
import google.generativeai as genai
import json
import os
import socket

# --- CONFIGURATION ---
st.set_page_config(page_title="Kalyx", layout="wide")

# Fichier de persistance (pour que l'Admin contrôle l'interface de tous)
DATA_FILE = "broadcast_data.json"
IMG_FILE = "shared_broadcast.png"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f: return json.load(f)
        except: pass
    return {"canicule": False, "show_img": False}

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f)

# --- INITIALISATION SESSION ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "page" not in st.session_state: st.session_state.page = "Parler à Kalix"
if "right_bar" not in st.session_state: st.session_state.right_bar = True

# --- PAGE DE CONNEXION / INSCRIPTION ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>Bienvenue sur Kalyx</h1>", unsafe_allow_html=True)
    col_c, col_form, col_r = st.columns([1, 2, 1])
    with col_form:
        mode = st.radio("Choisissez votre action :", ["Se connecter", "S'inscrire"])
        email = st.text_input("Adresse Email")
        password = st.text_input("Mot de passe", type="password")
        if st.button("Valider"):
            if email and password:
                st.session_state.logged_in = True
                st.rerun()
    st.stop()

# --- SIDEBAR (BOUTONS SÉPARÉS) ---
with st.sidebar:
    st.title("Kalyx")
    
    if st.button("💬 Parler à Kalix"): st.session_state.page = "Parler à Kalix"
    if st.button("🖼️ Générer une image"): st.session_state.page = "image"
    if st.button("📊 Activité"): st.session_state.page = "activity"
    if st.button("⚙️ Paramètres"): st.session_state.page = "settings"
    
    st.divider() # Séparation visuelle
    
    if st.button("👑 Panneau Admin"): st.session_state.page = "admin"
    
    st.divider()
    if st.button("Déconnexion"): st.session_state.logged_in = False; st.rerun()

# --- LAYOUT PRINCIPAL (Barre météo à droite rétractable) ---
col_main, col_right = st.columns([0.85 if st.session_state.right_bar else 1.0, 0.15 if st.session_state.right_bar else 0.01])

with col_right:
    if st.button("↔️"): st.session_state.right_bar = not st.session_state.right_bar; st.rerun()
    if st.session_state.right_bar:
        st.write("### ☀️ Météo")
        st.write("Aix-en-Provence : 28°C")

with col_main:
    data = load_data()
    
    # --- LOGIQUE AFFICHAGE CANICULE ---
    if data.get("canicule"):
        st.markdown("<h1 style='color:orange; text-align:center;'>🔥 ALERTE CANICULE !</h1>", unsafe_allow_html=True)
        st.image("https://img.freepik.com/vecteurs-premium/soleil-mignon-transpirant-buvant-verre-eau_825852-52.jpg")
        st.subheader("Hydratez-vous bien !")
    
    # --- LOGIQUE AFFICHAGE IMAGE PARTAGÉE ---
    if data.get("show_img") and os.path.exists(IMG_FILE):
        st.image(IMG_FILE, caption="Message de l'Admin")

    # --- PAGES ---
    if st.session_state.page == "Parler à Kalix":
        st.header("Parler à Kalix")
        if prompt := st.chat_input("Votre message..."):
            st.chat_message("user").markdown(prompt)
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel("gemini-1.5-pro")
                response = model.generate_content(prompt)
                st.chat_message("assistant").markdown(response.text)
            except: st.error("Erreur de connexion IA.")

    elif st.session_state.page == "admin":
        st.header("👑 Panneau Admin")
        
        # 1. Upload Image
        uploaded_file = st.file_uploader("Diffuser une image à tous :", type=['png', 'jpg'])
        if uploaded_file:
            with open(IMG_FILE, "wb") as f: f.write(uploaded_file.getbuffer())
            data["show_img"] = True; save_data(data)
            st.success("Image diffusée !")
        
        # 2. Bouton Canicule
        if st.button("☀️ Activer Alerte Canicule"):
            data["canicule"] = True; save_data(data); st.rerun()
            
        # 3. Reset
        if st.button("🛑 Tout réinitialiser"):
            save_data({"canicule": False, "show_img": False})
            if os.path.exists(IMG_FILE): os.remove(IMG_FILE)
            st.rerun()

    elif st.session_state.page == "image":
        st.header("Générateur d'image")
        query = st.text_input("Que voulez-vous générer ?")
        if st.button("Générer"):
            st.image(f"https://image.pollinations.ai/prompt/{query}")

    elif st.session_state.page == "activity":
        st.header("Activité")
        st.write("Utilisateurs connectés : 1 (Admin)")

    elif st.session_state.page == "settings":
        st.header("Paramètres")
        st.write(f"Utilisateur : Connecté")
        st.write(f"IP : {socket.gethostbyname(socket.gethostname())}")

# --- STYLE FOND D'ÉCRAN ---
st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e");
        background-size: cover;
        background-attachment: fixed;
    }
    </style>
""", unsafe_allow_html=True)
