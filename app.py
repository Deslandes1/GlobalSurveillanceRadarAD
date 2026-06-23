import streamlit as st

# 1. Initialisation de l'état (si ce n'est pas déjà fait)
if "ai_response" not in st.session_state:
    st.session_state.ai_response = ""

# 2. Zone de saisie et déclencheur
user_question = st.text_input("Posez une question sur les contacts radar :")

if st.button("Analyze"):
    if user_question:
        with st.spinner("L'analyste IA examine les données..."):
            # Appel de votre fonction (assurez-vous qu'elle lève une erreur ou renvoie un texte clair)
            try:
                donnees_radar = "..." # Vos données ADS-B
                resultat = ai_analysis(user_question, donnees_radar)
                st.session_state.ai_response = resultat
            except Exception as e:
                st.session_state.ai_response = f"❌ Erreur lors de l'appel API : {str(e)}"
        
        # Forcer le rafraîchissement pour mettre à jour l'UI
        st.rerun()

# 3. Rendu de la réponse : TOUJOURS en dehors du bloc du bouton !
st.write("---")
st.subheader("Analyse de l'Analyste IA")

if st.session_state.ai_response:
    st.write(st.session_state.ai_response)
else:
    st.info("💡 Cliquez sur 'Analyze' pour obtenir une réponse de l'IA...")
