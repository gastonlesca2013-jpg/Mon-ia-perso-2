import streamlit as st

st.set_page_config(layout="wide", page_title="Kalyx")

# --- CSS TOTALEMENT SOMBRE ---
st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a !important; }
    [data-testid="stSidebar"] { background-color: #121212 !important; border-right: 1px solid #333; }
    div.stButton > button { background-color: #262626 !important; color: white !important; border: 1px solid #444 !important; }
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] { display: none !important; }
    .stChatMessageContent { color: white !important; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🟪 Kalyx")
    if st.button("➕ Nouvelle discussion"):
        st.session_state.messages = []
        st.rerun()

# --- LOGIQUE D'IA (Réponse à TOUTES les questions) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Demander à Kalyx..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Kalyx répond à TOUT ce que vous écrivez
        reponse = f"Kalyx a analysé votre question : '{prompt}'. En tant qu'assistant, je peux vous dire que cette question est très pertinente. Pour approfondir, il faudrait préciser le domaine, mais sachez que je suis toujours disponible pour vous répondre rapidement."
        st.markdown(reponse)
        st.session_state.messages.append({"role": "assistant", "content": reponse})
