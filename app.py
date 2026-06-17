import streamlit as st
import google.generativeai as genai
import json
import os

# Configuration de la page
st.set_page_config(page_title="Kalyx", layout="wide")

# Vérification de sécurité pour les Secrets
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Erreur : La clé GEMINI_API_KEY n'est pas configurée dans les Settings Streamlit.")
    st.stop()

# Configuration IA
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def get_model():
    # On utilise un modèle standard
    return genai.GenerativeModel('gemini-1.5-flash')

# --- RESTE DU CODE (Exemple structure) ---
st.title("Kalyx")

# Gestion de l'affichage image (Correction de l'erreur MediaFileStorage)
data = {"img_url": ""} # Simulation de tes données
if data.get("img_url") and data["img_url"].startswith("http"):
    st.image(data["img_url"])
else:
    st.info("Aucune image à afficher.")

# Chat
if prompt := st.chat_input("Discuter avec Monia"):
    try:
        model = get_model()
        response = model.generate_content(prompt)
        st.write(response.text)
    except Exception as e:
        st.error(f"Erreur IA : {e}")
