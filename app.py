import streamlit as st
import google.generativeai as genai

# Configuration de la page en mode large pour un rendu optimal
st.set_page_config(page_title="Kalyx", page_icon="💎", layout="wide")

# --- STYLE CSS REPRIS DE GEMINI (SOMBRE PREMIUM & BULLES BLANCHES) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

    /* Fond ultra sombre général et police premium */
    html, body, .stApp, p, span, div, li {
        font-family: 'Inter', sans-serif !important;
        background-color: #131314 !important;
    }

    /* Écriture blanche et lisible pour tout le chat */
    .stMarkdown p, li, span {
        color: #FFFFFF !important; 
        font-size: 16px !important;
        line-height: 1.6 !important;
    }

    /* --- EFFET BULLES ÉPURÉES SOMBRES --- */
    [data-testid="stChatMessage"] {
        background-color: #1E1F20 !important; /* Teinte grise officielle des bulles Gemini */
        border-radius: 20px !important;
        padding: 18px 24px !important;
        margin-bottom: 14px !important;
        border: none !important;
    }

    /* Personnalisation de la barre de navigation latérale gauche */
    [data-testid="stSidebar"] {
        background-color: #1E1F20 !important;
        border-right: 1px solid #2D2F31 !important;
    }

    /* Forcer la couleur des boutons de l'historique en blanc */
    .stButton > button {
        color: #FFFFFF !important;
        background-color: transparent !important;
        border: 1px solid #3C4043 !important;
        text-align: left !important;
        justify-content: flex-start !important;
    }
    
    .stButton > button:hover {
        background-color: #2D2F31 !important;
        border-color: #A8C7FA !important;
    }

    /* Barre de recherche du bas */
    div[data-testid="stChatInput"] textarea {
        background-color: #1E1
