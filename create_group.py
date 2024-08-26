import streamlit as st
import json
from uuid import uuid4

st.title("Selecto")


def render_create_group():
    # Render create group page

    st.header("Wat is de groepsnaam?")
    groep_name = st.text_input("Groepsnaam")

    # initialise with 5 options
    st.header("Welke opties moeten er verdeeld worden?")

    if "n_opties" not in st.session_state:
        st.session_state.n_opties = 4
        st.session_state.opties = {}

    for i_optie in range(1, st.session_state.n_opties + 1):
        optie_name = "Optie " + str(i_optie)
        st.session_state.opties[optie_name] = st.text_input(optie_name)

    if st.button("Optie toevoegen"):
        st.session_state.n_opties += 1
        st.rerun()

    if st.button("Maak groep", type="primary", use_container_width=True):
        # filter out empty opties
        opties = sorted(
            [optie for optie in st.session_state.opties.values() if len(optie) > 0]
        )

        if len(opties) < 2:
            st.error("Vul tenminste 2 opties in!")
        else:
            st.session_state.groep_id = uuid4().hex
            with open(st.session_state.groep_id + ".json", "w") as f:
                json.dump(
                    {
                        "groep_name": groep_name,
                        "persoonsvoorkeuren": {},
                        "opties": opties,
                    },
                    f,
                )
            st.rerun()
