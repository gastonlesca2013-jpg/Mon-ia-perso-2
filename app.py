import streamlit as st
import google.generativeai as genai
import os

# Configuration de la page
st.set_page_config(page_title="Kalyx", layout="wide")

# Initialisation de la session
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "email" not in st.session_state: st.session_state.email = ""
if "page" not in st.session_state: st.session_state.page = "Parler à Kalix"

# --- CONNEXION ---
if not st.session_state.logged_in:
    st.title("🔒 Connexion")
    email = st.text_input("Adresse Email")
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
        else:
            st.error("Identifiants incorrects.")
    st.stop()

# --- SIDEBAR (Barre de tâches) ---
with st.sidebar:
    st.title("Kalyx")
    if st.button("💬 Parler à Kalix"): st.session_state.page = "Parler à Kalix"
    if st.button("🖼️ Générer Image"): st.session_state.page = "image"
    if st.button("📊 Activité"): st.session_state.page = "activity"
    
    # Bouton Admin remplaçant Paramètres pour vous uniquement
    if st.session_state.email == "gastonlesca2013@gmail.com":
        if st.button("👑 Panneau Admin"): st.session_state.page = "admin"
    else:
        st.write("---") # Espace pour les autres

    st.divider()
    if st.button("Déconnexion"):
        st.session_state.logged_in = False
        st.rerun()

# --- LOGIQUE PRINCIPALE ---
if st.session_state.page == "Parler à Kalix":
    st.header("Parler à Kalix")
    if prompt := st.chat_input("Votre message..."):
        st.chat_message("user").markdown(prompt)
        try:
            # Récupération de la clé API via Secrets
            api_key = st.secrets["GEMINI_API_KEY"]
            genai.configure(api_key=api_key)
            
            # Utilisation d'un modèle plus robuste
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            st.chat_message("assistant").markdown(response.text)
        except KeyError:
            st.error("ERREUR : La clé 'GEMINI_API_KEY' n'est pas définie dans les 'Secrets' de votre application.")
        except Exception as e:
            st.error(f"Erreur technique (Copiez ceci pour déboguer) : {e}")

elif st.session_state.page == "admin" and st.session_state.email == "gastonlesca2013@gmail.com":
    st.header("👑 Panneau Admin")
    st.success("Accès autorisé.")
    if st.button("Alerte Canicule"): st.warning("Alerte diffusée à tous.")
