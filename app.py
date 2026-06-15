import streamlit as st

# Configuration de la page
st.set_page_config(layout="wide", page_title="Kalyx")

# --- CSS FINAL : UNIFICATION TOTALE ---
st.markdown("""
    <style>
    /* 1. Fond global sombre (force tout l'arrière-plan) */
    .stApp { background-color: #1a1a1a !important; }
    
    /* 2. Suppression des zones blanches par défaut */
    header { background-color: transparent !important; }
    footer { visibility: hidden; }
    
    /* 3. Forcer le fond du conteneur Streamlit en gris sombre */
    .block-container { 
        background-color: #1a1a1a !important; 
    }
    
    /* 4. FIX FINAL : Cible précisément la barre de saisie et son environnement */
    /* On force la couleur de fond de tout le conteneur de saisie */
    [data-testid="stChatInputContainer"] { 
        background-color: #1a1a1a !important;
        border-top: none !important;
    }
    
    /* On force la couleur du champ lui-même */
    [data-testid="stChatInput"] { 
        background-color: #262626 !important;
        border: 1px solid #333 !important;
        border-radius: 25px !important;
    }

    /* 5. Barre latérale fixe */
    [data-testid="stSidebar"] { 
        background-color: #121212 !important; 
        border-right: 1px solid #333;
    }
    
    /* Boutons */
    div.stButton > button { 
        background-color: #262626 !important; 
        color: white !important; 
        border: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🟪 Kalyx")
    st.button("➕ Nouvelle discussion", use_container_width=True)
    st.button("📄 Nouveau notebook", use_container_width=True)
    st.markdown("<br><p style='color: gray; font-size: 0.8em;'>Récents</p>", unsafe_allow_html=True)
    st.button("• achat casquettes", use_container_width=True)
    st.button("• bonjour", use_container_width=True)

# --- CONTENU ---
st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; height: 70vh;">
        <h2 style='color: white; font-weight: 400;'>De nouvelles idées à explorer ?</h2>
    </div>
""", unsafe_allow_html=True)

# Barre de saisie
prompt = st.chat_input("Demander à Kalyx...")
