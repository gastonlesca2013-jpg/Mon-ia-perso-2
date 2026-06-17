import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Kalyx", layout="wide")

# CSS POUR L'INTERFACE (STYLE ET COULEURS)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white !important; }
    h1, h2, h3, label { color: white !important; }
    </style>
""", unsafe_allow_html=True)

# --- INITIALISATION ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_email" not in st.session_state: st.session_state.user_email = ""
if "password" not in st.session_state: st.session_state.password = ""
if "page" not in st.session_state: st.session_state.page = "chat"
if "show_right_bar" not in st.session_state: st.session_state.show_right_bar = True
if "logs" not in st.session_state: st.session_state.logs = []

ADMIN_EMAIL = "gastonlesca2013@gmail.com"
ADMIN_PWD = "Napoléon2013!"

# --- DIALOGUE ADMIN (Le panneau qui surgit) ---
@st.dialog("PANNEAU DE COMMANDE ADMIN")
def admin_popup():
    st.write("Ceci est votre panneau de contrôle complet.")
    st.write("Vous pouvez ici gérer la plateforme en toute liberté.")
    if st.button("Fermer le panneau"):
        st.rerun()

# --- LOGIQUE DE CONNEXION ---
if not st.session_state.logged_in:
    st.title("Connexion à Kalyx")
    email = st.text_input("Email")
    pwd = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if email:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.session_state.password = pwd
            st.rerun()
    st.stop()

# --- SIDEBAR GAUCHE ---
with st.sidebar:
    st.title("Kalyx")
    if st.button("💬 Kalyx vous écoute"): st.session_state.page = "chat"; st.rerun()
    if st.button("🖼️ Générer Image"): st.session_state.page = "image"; st.rerun()
    if st.button("📊 Activité"): st.session_state.page = "activity"; st.rerun()
    if st.button("⚙️ Paramètres"): st.session_state.page = "settings"; st.rerun()
    
    if st.session_state.user_email == ADMIN_EMAIL:
        st.divider()
        if st.button("👑 Panneau Admin"): st.session_state.page = "admin"; st.rerun()
    
    st.divider()
    if st.button("Déconnexion"): st.session_state.logged_in = False; st.rerun()

# --- BARRE DE TÂCHE DROITE (PLIABLE) ---
col_main, col_side = st.columns([0.8, 0.2 if st.session_state.show_right_bar else 0.01])

with col_main:
    # Bouton pour replier la barre
    if st.button("↔️ Replier/Déplier la barre de droite"):
        st.session_state.show_right_bar = not st.session_state.show_right_bar
        st.rerun()
    
    # --- PAGE CHAT ---
    if st.session_state.page == "chat":
        st.header("Kalyx vous écoute")
        if prompt := st.chat_input("Votre message pour Monia..."):
            st.session_state.logs.append(f"Chat: {prompt}")
            st.chat_message("user").markdown(prompt)
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                st.chat_message("assistant").markdown(response.text)
            except:
                st.error("Monia ne répond pas. Vérifiez la clé API.")

    # --- PAGE GÉNÉRER IMAGE ---
    elif st.session_state.page == "image":
        st.header("🎨 Générateur d'Image Web")
        query = st.text_input("Que voulez-vous voir ?")
        if st.button("Rechercher sur le Web"):
            # URL dynamique qui génère une image basée sur la recherche
            image_url = f"https://image.pollinations.ai/prompt/{query.replace(' ', '%20')}"
            st.image(image_url, caption=f"Résultat pour: {query}")

    # --- PAGE ACTIVITÉ ---
    elif st.session_state.page == "activity":
        st.header("📊 Activité")
        # Simulation de compte
        st.metric("Utilisateurs connectés aujourd'hui", 12)
        st.write("Activité récente enregistrée sur Kalyx.")

    # --- PAGE PARAMÈTRES ---
    elif st.session_state.page == "settings":
        st.header("⚙️ Vos Paramètres")
        st.write(f"**Email :** {st.session_state.user_email}")
        st.write(f"**Mot de passe :** ************") # Masqué par sécurité

    # --- PAGE ADMIN ---
    elif st.session_state.page == "admin" and st.session_state.user_email == ADMIN_EMAIL:
        st.header("👑 Panneau Administration")
        if st.button("Afficher le panneau de commande géant"):
            admin_popup()
        st.write("Logs système :", st.session_state.logs)

with col_side:
    if st.session_state.show_right_bar:
        st.markdown("### ℹ️ Infos Système")
        st.write(f"Utilisateur: {st.session_state.user_email}")
        st.write(f"Date: {datetime.now().strftime('%d/%m/%Y')}")
