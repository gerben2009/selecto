import streamlit as st
import json


def render_group_overview(groep_details):
    st.title("Voorkeuren van " + groep_details["groep_name"])

    # st.subheader("Personen op dit moment in groep")
    n_personen = len(groep_details["persoonsvoorkeuren"])
    if n_personen == 0:
        st.markdown("_er zijn nog geen personen in deze groep._")
    else:
        st.caption("Deelnemers:")
    for persoon in groep_details["persoonsvoorkeuren"]:
        st.markdown("* " + persoon)

    col1, col2 = st.columns([3, 1])
    with col1:
        current_person_name = st.text_input(
            "Voeg een persoon toe", placeholder="Naam", label_visibility="collapsed"
        )
    with col2:
        if st.button("Voeg persoon toe"):
            if current_person_name in groep_details["persoonsvoorkeuren"]:
                st.error("Persoon bestaat al")
            else:
                st.session_state.current_person_name = current_person_name
                st.session_state.current_action = "add_choices"
                st.rerun()

    st.markdown(f"[Link naar deze groep](/?groep_id={st.session_state.groep_id})")

    if st.button(
        f"Optimaliseer met {n_personen} personen",
        type="primary",
        use_container_width=True,
        disabled=(n_personen < 2),
    ):
        if len(groep_details["persoonsvoorkeuren"]) == 0:
            st.error("Voeg eerst personen toe")
        else:
            st.session_state.current_action = "optim"
            st.rerun()
