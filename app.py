import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Kalyx", layout="wide")

# Dossier pour les images partagées
BROADCAST_IMG = "shared_broadcast.png"

# --- SIDEBAR (NAVIGATION) ---
with st.sidebar:
    st.title("Kalyx")
    # Menu Navigation
    page = st.radio("Navigation", ["Parler à Kalix", "Générer Image", "Activité", "Paramètres", "Panneau Admin"])

# --- COLONNE DE DROITE (MÉTÉO & INFOS) ---
col_main, col_right = st.columns([0.8, 0.2])

with col_right:
    st.write("### ☀️ Infos")
    st.write(f"**Date :** {datetime.now().strftime('%d/%m/%Y')}")
    st.write("**Météo :** Aix-en-Provence, 25°C")
    st.divider()

# --- LOGIQUE PRINCIPALE ---
with col_main:
    # --- PAGE : PARLER À KALIX ---
    if page == "Parler à Kalix":
        st.header("Parler à Kalix")
        
        # Affichage image broadcastée par l'admin
        if os.path.exists(BROADCAST_IMG):
            st.image(BROADCAST_IMG, caption="Message important de l'Admin")

        # Upload image pour le chat (le "+" demandé)
        uploaded_file = st.file_uploader("➕ Ajouter une image à votre message", type=['png', 'jpg', 'jpeg'])
        
        if prompt := st.chat_input("Votre message à Kalix..."):
            st.chat_message("user").markdown(prompt)
            if uploaded_file:
                st.image(uploaded_file, width=200)
            
            try:
                # Utilisation de gemini-1.5-flash pour éviter l'erreur 404
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                st.chat_message("assistant").markdown(response.text)
            except Exception as e:
                st.error(f"Erreur IA : {e}")

    # --- PAGE : PANNEAU ADMIN ---
    elif page == "Panneau Admin":
        st.header("👑 Panneau Admin")
        
        st.subheader("Diffuser une image à tous")
        admin_file = st.file_uploader("Choisir une image", type=['png', 'jpg'])
        if admin_file:
            with open(BROADCAST_IMG, "wb") as f:
                f.write(admin_file.getbuffer())
            st.success("Image diffusée avec succès !")
            
        if st.button("Effacer l'image diffusée"):
            if os.path.exists(BROADCAST_IMG):
                os.remove(BROADCAST_IMG)
                st.rerun()

    # --- PAGES EXISTANTES (Garder opérationnelles) ---
    elif page == "Générer Image":
        st.header("Générateur d'image")
        query = st.text_input("Que voulez-vous générer ?")
        if st.button("Générer"):
            st.image(f"https://image.pollinations.ai/prompt/{query}")

    elif page == "Activité":
        st.header("Activité")
        st.write("Aucun log détecté.")

    elif page == "Paramètres":
        st.header("Paramètres")
        st.write("Configuration générale.")
