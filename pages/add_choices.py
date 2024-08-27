import streamlit as st
import json
from time import sleep


def errorBack(msg):
    st.error(msg)
    sleep(1)
    st.switch_page("main.py")


def render_add_choices():
    if not (
        "current_person_name" in st.session_state and "groep_id" in st.session_state
    ):
        errorBack("Informatie niet gevonden!")

    try:
        with open(st.session_state.groep_id + ".json", "r") as f:
            groep_details = json.load(f)
    except FileNotFoundError:
        errorBack("Groep niet gevonden!")

    st.title(st.session_state.current_person_name + ", vul je voorkeur in")

    # at most 5 voorkeuren can be set
    voorkeuren = {}

    already_selected_voorkeuren = []

    for i_voorkeur in range(len(groep_details["opties"])):

        opties_for_this_box = groep_details["opties"].copy()
        # for already_selected_voorkeur in already_selected_voorkeuren:
        #     opties_for_this_box.remove(already_selected_voorkeur)

        voorkeuren[i_voorkeur] = st.selectbox(
            str(i_voorkeur + 1) + "e keus", opties_for_this_box
        )

    if st.button("Versturen", type="primary"):
        # check duplicates
        print(voorkeuren)
        if len(set(voorkeuren.values())) < len(voorkeuren):
            st.error("Elke optie mag slechts 1x voorkomen!")
        else:
            groep_details["persoonsvoorkeuren"][
                st.session_state.current_person_name
            ] = voorkeuren

            with open(st.session_state.groep_id + ".json", "w") as f:
                json.dump(groep_details, f)

            st.success("Opgeslagen!")
            sleep(1)

            st.switch_page("pages/group_overview.py")


render_add_choices()
