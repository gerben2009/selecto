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
            if not current_person_name:
                st.error("vul een naam in")
            elif current_person_name in groep_details["persoonsvoorkeuren"]:
                st.error("Persoon bestaat al")
            else:
                st.session_state.current_person_name = current_person_name
                st.switch_page("pages/add_choices.py")

    st.markdown(
        f"[Link naar deze groep](/group_overview?groep_id={st.session_state.groep_id})"
    )

    if st.button(
        (
            f"Optimaliseer met {n_personen} personen"
            if not groep_details["optimised"]
            else "Bekijk resultaten van optimalisatie"
        ),
        type="primary",
        use_container_width=True,
        disabled=(n_personen < 2),
    ):
        if len(groep_details["persoonsvoorkeuren"]) == 0:
            st.error("Voeg eerst personen toe")
        else:
            st.switch_page("pages/optim.py")


# if "groep_id" in st.query_params:
#     st.session_state.groep_id = st.query_params.groep_id

if "groep_id" in st.session_state:
    st.query_params["groep_id"] = st.session_state["groep_id"]

elif "groep_id" in st.query_params:
    st.session_state["groep_id"] = st.query_params["groep_id"]

# read groep
# if "groep_id" in st.session_state:
if "groep_id" in st.query_params:

    try:
        with open(st.query_params.groep_id + ".json", "r") as f:
            groep_details = json.load(f)
            render_group_overview(groep_details)
    except FileNotFoundError:
        st.error("Groep niet gevonden!")
else:
    st.error("Groep niet gevonden!")
