import streamlit as st
import base64

# Configuration de la page
st.set_page_config(layout="wide", page_title="Kalyx")

# --- CSS POUR UNIFORMISER LE NOIR/GRIS SOMBRE ---
st.markdown("""
    <style>
    /* 1. Fond global de l'application */
    .stApp { background-color: #1a1a1a !important; }
    
    /* 2. Suppression des zones blanches en haut et en bas */
    header { background-color: #1a1a1a !important; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* 3. Sidebar : Fond fixe et suppression de l'effet de survol */
    [data-testid="stSidebar"] { 
        background-color: #121212 !important; 
        border-right: 1px solid #333;
    }
    
    /* Force les boutons à rester gris foncé et empêche le changement de couleur au survol */
    div.stButton > button { 
        background-color: #262626 !important; 
        color: white !important; 
        border: none !important;
        transition: none !important;
    }
    
    div.stButton > button:hover {
        background-color: #262626 !important; /* Maintient la même couleur */
        border: none !important;
        color: white !important;
    }
    
    /* 4. Barre de saisie : Suppression du blanc */
    div[data-testid="stChatInputContainer"] {
        background-color: #1a1a1a !important;
        border-top: none !important;
    }
    
    [data-testid="stChatInput"] { 
        background-color: #262626 !important;
        border: 1px solid #333 !important;
        color: white !important;
    }
    
    /* Texte dans la zone de saisie */
    textarea { color: white !important; }
    
    /* Titre central */
    h2 { color: white !important; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR AVEC LOGO ---
with st.sidebar:
    # Ajustez le chemin de votre logo si nécessaire
    st.image("image_8281ff.jpg", width=40) 
    st.write("### Kalyx")
    
    st.button("➕ Nouvelle discussion", use_container_width=True)
    st.button("📄 Nouveau notebook", use_container_width=True)
    st.markdown("<br><p style='color: gray; font-size: 0.8em;'>Récents</p>", unsafe_allow_html=True)
    st.button("• achat casquettes", use_container_width=True)
    st.button("• bonjour", use_container_width=True)

# --- CONTENU PRINCIPAL ---
st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; height: 70vh;">
        <h2>De nouvelles idées à explorer ?</h2>
    </div>
""", unsafe_allow_html=True)

# Barre de saisie
prompt = st.chat_input("Demander à Kalyx...")
