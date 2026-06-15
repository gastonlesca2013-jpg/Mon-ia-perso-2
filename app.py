import streamlit as st

# Configuration de la page
st.set_page_config(layout="wide", page_title="Kalyx")

# --- CSS FINAL POUR UNIFORMITÉ TOTALE ---
st.markdown("""
    <style>
    /* 1. Fond global sombre */
    .stApp { background-color: #1a1a1a !important; }
    
    /* 2. Masquer les éléments blancs par défaut */
    header { background-color: transparent !important; }
    footer { visibility: hidden; }
    
    /* 3. Barre latérale fixe */
    [data-testid="stSidebar"] { 
        background-color: #121212 !important; 
        border-right: 1px solid #333;
        min-width: 260px !important; 
        max-width: 260px !important;
    }
    
    /* 4. Boutons gris fixes (pas de changement au survol) */
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

    /* 5. CORRECTION DE LA BARRE DE SAISIE (Suppression du blanc) */
    .stChatInput { 
        position: fixed; 
        bottom: 50px; 
        width: 60%; 
        left: 20%; 
        right: 20%;
    }
    
    /* Force le fond de la zone de saisie en gris sombre */
    [data-testid="stChatInput"] { 
        background-color: #262626 !important; 
        border: 1px solid #333 !important;
        border-radius: 25px !important;
    }
    
    /* Change la couleur du texte à l'intérieur */
    [data-testid="stChatInput"] textarea {
        color: white !important;
    }

    .logo-box { background-color: #7b2cbf; color: white; width: 25px; height: 25px; display: inline-flex; align-items: center; justify-content: center; border-radius: 4px; margin-right: 10px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<div><span class='logo-box'>K</span> Kalyx</div>", unsafe_allow_html=True)
    st.write("")
    st.button("➕ Nouvelle discussion", use_container_width=True)
    st.button("📄 Nouveau notebook", use_container_width=True)
    st.markdown("<br><p style='color: gray; font-size: 0.8em;'>Récents</p>", unsafe_allow_html=True)
    st.button("• achat casquettes", use_container_width=True)
    st.button("• bonjour", use_container_width=True)

# --- CONTENU ---
st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; height: 80vh;">
        <h2 style='color: white; font-weight: 400;'>De nouvelles idées à explorer ?</h2>
    </div>
""", unsafe_allow_html=True)

# Barre de saisie
prompt = st.chat_input("Demander à Kalyx...")
