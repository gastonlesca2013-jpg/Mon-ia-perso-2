import streamlit as st
import base64
import requests

# Configuration de la page
st.set_page_config(layout="wide", page_title="Kalyx")

# --- FONCTION POUR CHARGER LE LOGO ---
def get_image_as_base64(url):
    try:
        response = requests.get(url)
        return base64.b64encode(response.content).decode()
    except:
        return ""

# URL de votre logo
logo_url = "https://images.unsplash.com/photo-1635322967697-380535593845?q=80&w=100&auto=format&fit=crop" # Remplacez par votre URL réelle si nécessaire
logo_base64 = get_image_as_base64(logo_url)

# --- CSS FINAL : LOGO FIXÉ + DESIGN ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #1a1a1a !important; }}
    footer {{ visibility: hidden; }}
    
    /* Barre latérale */
    [data-testid="stSidebar"] {{ 
        background-color: #121212 !important; 
        border-right: 1px solid #333;
        min-width: 260px !important; 
        max-width: 260px !important;
    }}
    
    /* En-tête avec logo */
    .sidebar-header {{
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 10px;
        margin-bottom: 20px;
    }}
    
    .logo-img {{
        width: 30px;
        height: 30px;
        border-radius: 5px;
    }}
    
    .brand-name {{
        color: white;
        font-size: 22px;
        font-weight: bold;
    }}

    /* Fix zone saisie */
    [data-testid="stChatInputContainer"] {{ 
        background-color: #1a1a1a !important;
    }}
    [data-testid="stChatInput"] {{ 
        background-color: #262626 !important;
        border: 1px solid #333 !important;
        border-radius: 25px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR AVEC LOGO ---
with st.sidebar:
    st.markdown(f"""
        <div class='sidebar-header'>
            <img src='data:image/png;base64,{logo_base64}' class='logo-img'>
            <span class='brand-name'>Kalyx</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.button("➕ Nouvelle discussion", use_container_width=True)
    st.button("📄 Nouveau notebook", use_container_width=True)
    st.markdown("<br><p style='color: gray; font-size: 0.8em;'>Récents</p>", unsafe_allow_html=True)
    st.button("• achat casquettes", use_container_width=True)
    st.button("• bonjour", use_container_width=True)

# --- CONTENU ---
st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; height: 75vh;">
        <h2 style='color: white; font-weight: 400;'>De nouvelles idées à explorer ?</h2>
    </div>
""", unsafe_allow_html=True)

prompt = st.chat_input("Demander à Kalyx...")
