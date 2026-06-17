import streamlit as st
import google.generativeai as genai
import json
import os
import socket

# --- CONFIGURATION ---
st.set_page_config(page_title="Kalyx", layout="wide")

# Fichier pour la persistance des données (Broadcast)
DATA_FILE = "broadcast_data.json"

def load_broadcast():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f: return json.load(f)
        except: return {"msg": None, "img": None, "effect": None}
    return {"msg": None, "img": None, "effect": None}

def save_broadcast(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f)

# --- INITIALISATION ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_email" not in st.session_state: st.session_state.user_email = ""
if "page" not in st.session_state: st.session_state.page = "chat"
if "users_db" not in st.session_state: st.session_state.users_db = set() # Pour compter les accès

# --- CONNEXION ---
if not st.session_state.logged_in:
    st.title("Connexion à Kalyx")
    email = st.text_input("Email")
    pwd = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter / S'inscrire"):
        if email:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.session_state.users_db.add(email) # Ajoute à la liste des accès
            st.rerun()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.title("Kalyx")
    if st.button("💬 Monia - Chat"): st.session_state.page = "chat"
    if st.button("🖼️ Générer Image"): st.session_state.page = "image"
    if st.button("📊 Activité"): st.session_state.page = "activity"
    if st.button("⚙️ Paramètres"): st.session_state.page = "settings"
    
    if st.session_state.user_email == "gastonlesca2013@gmail.com":
        st.divider()
        if st.button("👑 Panneau Admin"): st.session_state.page = "admin"
    
    st.divider()
    if st.button("Déconnexion"): st.session_state.logged_in = False; st.rerun()

# --- LOGIQUE PRINCIPALE ---
b_data = load_broadcast()

# Gestion des effets visuels globaux
if b_data.get("effect") == "skull":
    st.markdown("<h1 style='text-align: center; font-size: 100px;'>💀</h1>", unsafe_allow_html=True)
elif b_data.get("effect") == "canicule":
    st.image("https://images.unsplash.com/photo-1530521954074-e64f6810b32d")

# --- PAGES ---
if st.session_state.page == "chat":
    st.header("Monia - Chat")
    if b_data["msg"]: st.warning(f"📢 INFO: {b_data['msg']}")
    if b_data["img"]: st.image(b_data["img"])

    prompt = st.chat_input("Dites quelque chose à Monia...")
    if prompt:
        if "boom" in prompt.lower():
            d = load_broadcast(); d["effect"] = "skull"; save_broadcast(d)
            st.rerun()
        
        st.chat_message("user").markdown(prompt)
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel("gemini-1.5-pro")
            response = model.generate_content(prompt)
            st.chat_message("assistant").markdown(response.text)
        except: st.error("Erreur API.")

elif st.session_state.page == "activity":
    st.header("📊 Activité")
    st.metric("Nombre d'utilisateurs uniques aujourd'hui", len(st.session_state.users_db))

elif st.session_state.page == "settings":
    st.header("⚙️ Paramètres")
    st.write(f"Email : {st.session_state.user_email}")
    st.write(f"Adresse IP (Connexion) : {socket.gethostbyname(socket.gethostname())}")
    st.write("Mot de passe système : [PROTÉGÉ PAR LE SYSTÈME]")

elif st.session_state.page == "admin":
    st.header("👑 Panneau Admin (Contrôle Total)")
    
    # Gestion Broadcast
    new_msg = st.text_input("Message à diffuser :")
    if st.button("Diffuser Message"):
        d = load_broadcast(); d["msg"] = new_msg; save_broadcast(d)
    
    # Upload Image
    uploaded_file = st.file_uploader("Envoyer une photo à tout le monde :", type=["jpg", "png"])
    if uploaded_file and st.button("Diffuser l'image"):
        d = load_broadcast(); d["img"] = uploaded_file.read(); save_broadcast(d)
    
    # Boutons Farfelus
    st.subheader("Boutons Farfelus")
    c1, c2, c3 = st.columns(3)
    if c1.button("🔥 Alerte Canicule"): 
        d = load_broadcast(); d["effect"] = "canicule"; save_broadcast(d)
    if c2.button("💀 Activer Skull"): 
        d = load_broadcast(); d["effect"] = "skull"; save_broadcast(d)
    if c3.button("🔄 Reset Tout"): 
        save_broadcast({"msg": None, "img": None, "effect": None})

# --- FOND D'ÉCRAN ---
st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e");
        background-size: cover;
    }
    </style>
""", unsafe_allow_html=True)
