import streamlit as st

# Configuration de la page
st.set_page_config(layout="wide", page_title="Kalyx")

# --- CSS FINAL : IDENTITÉ VISUELLE & ZÉRO BLANC ---
st.markdown("""
    <style>
    /* 1. FOND GLOBAL SOMBRE (ARRIÈRE-PLAN TEXTE) */
    .stApp { background-color: #1a1a1a !important; }
    
    /* 2. ÉLIMINATION TOTALE DU BLANC (HEADER & FOOTER) */
    header { background-color: transparent !important; }
    footer { visibility: hidden; }
    
    /* 3. BARRE LATÉRALE FIXE ET LOGO */
    [data-testid="stSidebar"] { 
        background-color: #121212 !important; 
        border-right: 1px solid #333;
        min-width: 260px !important; 
        max-width: 260px !important;
    }
    
    .sidebar-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 20px;
    }
    
    .logo-img {
        width: 35px;
        height: 35px;
        object-fit: contain;
    }
    
    .brand-name {
        color: white;
        font-size: 20px;
        font-weight: bold;
    }

    /* 4. BOUTONS FIXES (SANS EFFET NOIR AU SURVOL) */
    div.stButton > button { 
        background-color: #262626 !important; 
        color: white !important; 
        border: none !important;
        text-align: left;
    }
    div.stButton > button:hover {
        background-color: #262626 !important;
        border: none !important;
        color: white !important;
    }

    /* 5. ZONE DE SAISIE SOMBRE (SANS CARRÉ BLANC) */
    [data-testid="stChatInputContainer"] { 
        background-color: #1a1a1a !important;
        border-top: none !important;
    }
    
    [data-testid="stChatInput"] { 
        background-color: #262626 !important;
        border: 1px solid #333 !important;
        border-radius: 25px !important;
    }
    
    [data-testid="stChatInput"] textarea {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- BARRE LATÉRALE (SIDEBAR) ---
with st.sidebar:
    # Intégration du logo fourni à gauche du nom
    logo_url = "http://googleusercontent.com/image_collection/image_retrieval/11398957632741036184"
