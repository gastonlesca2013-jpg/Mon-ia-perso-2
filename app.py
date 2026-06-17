import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Kalyx", layout="wide")

# --- INITIALISATION ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_email" not in st.session_state: st.session_state.user_email = ""
if "page" not in st.session_state: st.session_state.page = "chat"
if "show_right_bar" not in st.session_state: st.session_state.show_right_bar = True
if "is_pro" not in st.session_state: st.session_state.is_pro = False
if "bg_url" not in st.session_state: st.session_state.bg_url = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e"

# --- LOGIN & AUTHENTIFICATION ---
ADMIN_EMAIL = "gastonlesca2013@gmail.com"
ADMIN_PWD = "Napoléon2013!"

if not st.session_state.logged_in:
    st.title("Connexion Kalyx")
    email = st.text_input("Email")
    pwd = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        # Vérification Admin
        if email == ADMIN_EMAIL and pwd == ADMIN_PWD:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.session_state.is_admin = True
            st.rerun()
        # Vérification Utilisateur normal
        elif email and pwd:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.session_state.is_admin = False
            st.rerun()
    st.stop()

# --- SIDEBAR GAUCHE ---
with st.sidebar:
    st.markdown("### Kalyx")
    if st.button("➕ Nouvelle Discussion"): st.session_state.page = "chat"
    if st.button("🎨 Générer Image"): st.session_state.page = "image"
    if st.button("📊 Activité"): st.session_state.page = "activity"
    if st.button("⚙️ Paramètres"): st.session_state.page = "settings"
    
    # ACCÈS ADMIN (Uniquement pour vous)
    if st.session_state.is_admin:
        st.divider()
        st.markdown("### 👑 Panneau Admin")
        if st.button("👥 Voir Utilisateurs"): st.session_state.page = "admin"

# --- HEADER (Avec bouton droite à droite) ---
col_head1, col_head2 = st.columns([4, 1])
with col_head2:
    if st.button("↔️ Infos"):
        st.session_state.show_right_bar = not st.session_state.show_right_bar
        st.rerun()

# --- LAYOUT PRINCIPAL ---
if st.session_state.show_right_bar:
    main_col, right_col = st.columns([0.75, 0.25])
else:
    main_col = st.container()
    right_col = None

with main_col:
    # 1. PANNEAU ADMIN
    if st.session_state.page == "admin" and st.session_state.is_admin:
        st.header("👑 Panneau d'Administration")
        # Ici, vous verrez les emails. Pas de mots de passe pour votre sécurité.
        st.write("Liste des utilisateurs inscrits :")
        st.table({"Email": ["utilisateur1@test.com", "client@mail.com"], "Statut": ["Basique", "Pro"]})

    # 2. CHAT
    elif st.session_state.page == "chat":
        st.header("Kalyx vous écoute")
        if prompt := st.chat_input("Votre message..."):
            if "boom" in prompt.lower():
                st.session_state.bg_url = "https://www.public.fr/styles/desktop/public/2023-04/jul.jpg"
                st.rerun()
            st.write(f"Réponse IA pour {st.session_state.user_email}")

    # 3. PAIEMENT
    elif st.session_state.page == "settings":
        st.header("Mise à niveau")
        st.link_button("Payer 9,99€ (Pro)", "https://www.paypal.com")
        st.link_button("Payer 24,99€ (Illimité)", "https://www.paypal.com")

# --- BARRE DROITE ---
if right_col:
    with right_col:
        st.markdown("### ℹ️ Infos")
        st.write(f"Connecté : {st.session_state.user_email}")
        st.write(f"Statut : {'Admin' if st.session_state.is_admin else 'Utilisateur'}")
