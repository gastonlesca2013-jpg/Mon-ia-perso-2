import streamlit as st

# Configuration de la page
st.set_page_config(layout="wide", page_title="Kalyx")

# --- CSS COMPLET ET UNIFIÉ ---
st.markdown("""
    <style>
    /* Forcer la couleur de fond globale pour éliminer les zones blanches */
    .stApp { 
        background-color: #1a1a1a !important; 
    }
    
    /* Supprimer le padding par défaut de Streamlit */
    .block-container { padding-top: 0rem; padding-bottom: 0rem; }
    
    /* Barre latérale fixe et non redimensionnable */
    [data-testid="stSidebar"] { 
        background-color: #121212 !important; 
        border-right: 1px solid #333;
        min-width: 260px !important; 
        max-width: 260px !important;
    }
    
    /* Bloquer les effets de survol sur les boutons */
    div.stButton > button:hover {
        background-color: #262626 !important;
        border: none !important;
        color: white !important;
    }
    
    div.stButton > button { 
        background-color: #262626 !important; 
        color: white !important; 
        border: none !important;
        text-align: left;
    }

    /* Barre de saisie centrée */
    .stChatInput { 
        position: fixed; 
        bottom: 50px; 
        width: 60%; 
        left: 20%; 
        right: 20%;
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
# Titre principal centré verticalement
st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; height: 80vh;">
        <h2 style='color: white; font-weight: 400;'>De nouvelles idées à explorer ?</h2>
    </div>
""", unsafe_allow_html=True)

# Barre de saisie
prompt = st.chat_input("Demander à Kalyx...")
