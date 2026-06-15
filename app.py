import streamlit as st

# Configuration de la page pour un rendu sombre
st.set_page_config(layout="wide", page_title="Kalyx")

# --- STYLE CSS PERSONNALISÉ POUR LE LOOK "KALYX" ---
st.markdown("""
    <style>
    /* Fond principal sombre */
    .stApp { background-color: #1a1a1a; color: white; }
    
    /* Barre latérale */
    [data-testid="stSidebar"] { background-color: #121212; border-right: 1px solid #333; }
    
    /* Zone de saisie en bas */
    .stChatInput { position: fixed; bottom: 20px; width: 60%; left: 20%; }
    
    /* Boutons et éléments */
    div.stButton > button { background-color: #2a2a2a; border-radius: 20px; border: none; color: white; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR (Barre de gauche) ---
with st.sidebar:
    st.image("https://via.placeholder.com/50", caption="Kalyx") # Remplacez par votre logo
    st.button("➕ Nouvelle discussion")
    st.button("📝 Nouveau notebook")
    st.write("---")
    st.write("**Récents**")
    st.button("achat casquettes")
    st.button("bonjour")

# --- CONTENU PRINCIPAL ---
st.markdown("<h1 style='text-align: center; margin-top: 100px;'>De nouvelles idées à explorer ?</h1>", unsafe_allow_html=True)

# --- ZONE DE SAISIE (Bottom) ---
prompt = st.chat_input("Demander à Kalyx")

if prompt:
    st.write(f"Vous avez demandé : {prompt}")
