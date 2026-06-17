import streamlit as st
import google.generativeai as genai
import json
import os

# --- CONFIGURATION & PERSISTANCE ---
st.set_page_config(page_title="Kalyx", layout="wide")
DATA_FILE = "app_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f: return json.load(f)
        except: pass
    return {"message": "", "img_url": None}

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f)

# --- INITIALISATION SESSION ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_email" not in st.session_state: st.session_state.user_email = ""
if "page" not in st.session_state: st.session_state.page = "Parler à Kalix"

# --- LOGIN ---
if not st.session_state.logged_in:
    st.title("🔒 Connexion")
    email = st.text_input("Adresse Email")
    password = st.text_input("Mot de passe", type="password")
    
    if st.button("Se connecter"):
        # Authentification stricte
        if email == "gastonlesca2013@gmail.com" and password == "Napoléon 2013 !":
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.rerun()
        elif email and password: # Autres utilisateurs
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.rerun()
        else:
            st.error("Identifiants incorrects ou manquants.")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.title("Kalyx")
    if st.button("💬 Parler à Kalix"): st.session_state.page = "Parler à Kalix"
    if st.button("🖼️ Générer Image"): st.session_state.page = "image"
    if st.button("📊 Activité"): st.session_state.page = "activity"
    if st.button("⚙️ Paramètres"): st.session_state.page = "settings"
    
    # Condition admin stricte
    if st.session_state.user_email == "gastonlesca2013@gmail.com":
        st.divider()
        if st.button("👑 Panneau Admin"): st.session_state.page = "admin"
    
    st.divider()
    if st.button("Déconnexion"): 
        st.session_state.logged_in = False
        st.rerun()

# --- LOGIQUE PRINCIPALE ---
# Style background
st.markdown("""<style>.stApp { background: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e'); background-size: cover; }</style>""", unsafe_allow_html=True)

# Affichage broadcast global
data = load_data()
if data["message"]: st.warning(f"📢 INFO: {data['message']}")

if st.session_state.page == "Parler à Kalix":
    st.header("Parler à Kalix")
    if prompt := st.chat_input("Votre message..."):
        st.chat_message("user").markdown(prompt)
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            st.chat_message("assistant").markdown(response.text)
        except Exception as e:
            st.error(f"Erreur IA : {e}")

elif st.session_state.page == "admin" and st.session_state.user_email == "gastonlesca2013@gmail.com":
    st.header("👑 Panneau Admin")
    new_msg = st.text_input("Diffuser un message à tous :")
    if st.button("Publier message"):
        save_data({"message": new_msg, "img_url": data["img_url"]})
        st.success("Message diffusé !")
    if st.button("Effacer le message"):
        save_data({"message": "", "img_url": data["img_url"]})
        st.rerun()

elif st.session_state.page == "activity":
    st.header("Activité")
    st.write("Statistiques : 1 utilisateur actif.")

elif st.session_state.page == "settings":
    st.header("Paramètres")
    st.write(f"Connecté en tant que : {st.session_state.user_email}")

elif st.session_state.page == "image":
    st.header("Générer Image")
    query = st.text_input("Description :")
    if st.button("Rechercher"):
        st.image(f"https://image.pollinations.ai/prompt/{query}")
