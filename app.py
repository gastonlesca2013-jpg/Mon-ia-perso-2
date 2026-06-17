import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Kalyx", layout="wide")

# --- INITIALISATION DES ÉTATS (LA MÉMOIRE) ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_email" not in st.session_state: st.session_state.user_email = ""
if "messages" not in st.session_state: st.session_state.messages = []
if "page" not in st.session_state: st.session_state.page = "chat"
if "show_right_bar" not in st.session_state: st.session_state.show_right_bar = True
if "is_pro" not in st.session_state: st.session_state.is_pro = False
if "bg_url" not in st.session_state: st.session_state.bg_url = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e"

# --- LOGIN & ADMIN ---
ADMIN_EMAIL = "gastonlesca2013@gmail.com"
ADMIN_PWD = "Napoléon2013!"

if not st.session_state.logged_in:
    st.title("Connexion à Kalyx")
    email = st.text_input("Email")
    pwd = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if email == ADMIN_EMAIL and pwd == ADMIN_PWD:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.rerun()
        elif email and pwd: # Utilisateur standard
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.rerun()
    st.stop()

# --- CSS GLOBAL ---
st.markdown(f"""
    <style>
    .stApp {{ background: url("{st.session_state.bg_url}"); background-size: cover; background-attachment: fixed; }}
    [data-testid="stSidebar"] {{ background-color: rgba(0,0,0,0.85) !important; }}
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR GAUCHE (NAVIGATION) ---
with st.sidebar:
    st.markdown("### Kalyx")
    if st.button("➕ Nouvelle Discussion"): st.session_state.page = "chat"; st.rerun()
    if st.button("🎨 Générer Image"): st.session_state.page = "image"; st.rerun()
    if st.button("📊 Activité"): st.session_state.page = "activity"; st.rerun()
    if st.button("⚙️ Paramètres"): st.session_state.page = "settings"; st.rerun()
    
    if st.session_state.user_email == ADMIN_EMAIL:
        st.divider()
        st.markdown("### 👑 Panneau Admin")
        if st.button("👥 Voir Utilisateurs"): st.session_state.page = "admin"; st.rerun()

# --- LAYOUT PRINCIPAL ---
# Bouton pour toggler la barre droite (en haut à droite)
col1, col2 = st.columns([0.9, 0.1])
with col2:
    if st.button("↔️"):
        st.session_state.show_right_bar = not st.session_state.show_right_bar
        st.rerun()

# Division colonnes (si barre droite activée)
if st.session_state.show_right_bar:
    main_col, right_col = st.columns([0.8, 0.2])
else:
    main_col = st.container()
    right_col = None

# --- LOGIQUE CONTENU ---
with main_col:
    # 1. PAGE CHAT (Monia)
    if st.session_state.page == "chat":
        st.header("Kalyx vous écoute")
        # IA LOGIC
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel("gemini-1.5-flash")
        except: st.error("Clé API manquante.")

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])
        
        if prompt := st.chat_input("Votre message..."):
            # COMMANDE BOOM
            if "boom" in prompt.lower():
                st.session_state.bg_url = "https://static.skyrock.fm/static/0.skyrock.fm/art/pic.99965315.2.jpg"
                st.rerun()
            
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)
            
            with st.chat_message("assistant"):
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

    # 2. PAGE ADMIN (Seulement pour toi)
    elif st.session_state.page == "admin" and st.session_state.user_email == ADMIN_EMAIL:
        st.header("👑 Panneau Administration")
        st.write(f"Gestion des utilisateurs connectés. (Admin: {st.session_state.user_email})")
        # Simulation d'affichage des logs utilisateurs
        st.table({"Utilisateur": ["user1@gmail.com", "autre@hotmail.fr"], "Activité": ["Chat", "Image Gen"]})

# --- BARRE DROITE ---
if right_col:
    with right_col:
        st.markdown("### ℹ️ Infos")
        st.write(f"Connecté : {st.session_state.user_email}")
        st.write(f"Date : {datetime.now().strftime('%d/%m/%Y')}")
