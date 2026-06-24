# Modifie ta zone de saisie comme ceci :
if prompt := st.chat_input("Pose ta question à Gropi..."):
    # 1. Vérification de sécurité : on n'envoie rien si c'est vide
    if not prompt.strip():
        st.warning("Veuillez entrer un message valide.")
    else:
        # Affiche le message de l'utilisateur
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. Gestion de l'appel à l'IA avec sécurité
        try:
            with st.chat_message("assistant"):
                response = model.generate_content(prompt)
                full_response = response.text
                st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Erreur lors de la connexion à l'IA : {e}")
