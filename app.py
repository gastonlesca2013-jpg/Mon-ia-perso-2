import streamlit as st
import google.generativeai as genai
import json
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="Kalyx", layout="wide")

# Fichier pour la persistance des messages globaux (pour le panneau admin)
DATA_FILE = "app_data.json"

def load_broadcast():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f: return json.load(f)
    return {"message": ""}

def save_broadcast(msg):
    with open(DATA_FILE, "w") as f: json.dump({"message": msg}, f)

# --- INITIALISATION SESSION ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "page" not in st.session_state: st.session_state.page = "Parler à Calix"

# --- PAGE DE CONNEXION (OBLIGATOIRE) ---
if not st.session_state.logged_in:
    st.title("🔒 Connexion à Kalyx")
    st.write("Veuillez vous identifier pour accéder à l'application.")
    
    email = st.text_input("Adresse Email")
    password = st.text_input("Mot de passe", type="password")
    
    if st.button("Se connecter / S'inscrire"):
        if email and password:
            st.session_state.logged_in = True
            st.rerun()
    st.stop() # Arrête le script ici si non connecté

# --- SIDEBAR (NAVIGATION) ---
with st.sidebar:
    st.title("Kalyx")
    if st.button("💬 Parler à Calix"): st.session_state.page = "Parler à Calix"
    if st.button("🖼️ Générer Image"): st.session_state.page = "image"
    if st.button("📊 Activité"): st.session_state.page = "activity"
    if st.button("⚙️ Paramètres"): st.session_state.page = "settings"
    st.divider()
    if st.button("👑 Panneau Admin"): st.session_state.page = "admin"
    st.divider()
    if st.button("Déconnexion"): st.session_state.logged_in = False; st.rerun()

# --- CONTENU PRINCIPAL ---
st.markdown("<style>.stApp { background: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e'); background-size: cover; }</style>", unsafe_allow_html=True)

# Affichage du message broadcast
data = load_broadcast()
if data["message"]:
    st.warning(f"📢 Message de l'admin : {data['message']}")

# --- PAGES ---
if st.session_state.page == "Parler à Calix":
    st.header("Parler à Calix")
    if prompt := st.chat_input("Votre message à Calix..."):
        st.chat_message("user").markdown(prompt)
        try:
            # Vérification de la clé API
            if "GEMINI_API_KEY" in st.secrets:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel("gemini-1.5-pro")
                response = model.generate_content(prompt)
                st.chat_message("assistant").markdown(response.text)
            else:
                st.error("La clé API n'est pas configurée dans les secrets.")
        except Exception as e:
            st.error(f"Erreur de connexion avec l'IA : {e}")

elif st.session_state.page == "admin":
    st.header("👑 Panneau Admin")
    new_msg = st.text_input("Envoyer un message à tous les utilisateurs :")
    if st.button("Diffuser le message"):
        save_broadcast(new_msg)
        st.success("Message diffusé !")
    if st.button("Supprimer le message global"):
        save_broadcast("")
        st.rerun()

elif st.session_state.page == "image":
    st.header("Générer Image")
    query = st.text_input("Description :")
    if st.button("Rechercher"):
        st.image(f"https://image.pollinations.ai/prompt/{query}")

elif st.session_state.page == "activity":
    st.header("Activité")
    st.write("Aucune activité suspecte détectée.")

elif st.session_state.page == "settings":
    st.header("Paramètres")
    st.write("Configuration utilisateur disponible.")
