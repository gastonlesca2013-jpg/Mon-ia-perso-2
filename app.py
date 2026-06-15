import streamlit as st

# Configuration de la page
st.set_page_config(layout="wide", page_title="Kalyx")

# --- CSS CORRIGÉ POUR UNIFIER TOUT L'ARRIÈRE-PLAN ---
st.markdown("""
    <style>
    /* 1. Forcer le fond de toute l'application en gris très foncé */
    .stApp { 
        background-color: #1a1a1a !important; 
    }
    
    /* 2. Éliminer les zones blanches en haut et en bas */
    header { background-color: transparent !important; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* 3. Barre latérale fixe (non redimensionnable) */
    [data-testid="stSidebar"] { 
        background-color: #121212 !important; 
        border-right: 1px solid #333;
        min-width: 260px !important; 
        max-width: 260px !important;
    }
    
    /* 4. Style des boutons sans changement de couleur au survol */
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

    /* 5. Barre de saisie (Chat Input) */
    .stChatInput { 
        position: fixed; 
        bottom: 50px; 
        width: 60%; 
        left: 20%; 
        right: 20%;
    }
    
    /* Le fond du chat input lui-même */
    [data-testid="stChatInput"] { 
        background-color: #262626 !important; 
        border: none !important;
    }

    /* Logo K */
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

# --- CONTENU PRINCIPAL ---
st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; height: 80vh;">
        <h2 style='color: white; font-weight: 400;'>De nouvelles idées à explorer ?</h2>
    </div>
""", unsafe_allow_html=True)

# Barre de saisie
prompt = st.chat_input("Demander à Kalyx...")
