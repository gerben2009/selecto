import streamlit as st

st.title("top 5")


if "groep_id" not in st.session_state:
    # Render create group page

    # initialise with 5 options
    if "n_options" not in st.session_state:
        st.session_state.n_options = 5
        st.session_state.options = {}

    for i_optie in range(1, st.session_state.n_options + 1):
        optie_name = "Optie " + str(i_optie)
        st.session_state.options[optie_name] = st.text_input(optie_name)

    if st.button("Optie toevoegen"):
        st.session_state.n_options += 1
        st.rerun()

    if st.button("Begin een groep"):
        st.session_state.groep_id = "89u489uy"
        st.rerun()
elif "current_person_name" not in st.session_state:
    # Render add person page

    st.text("Vul je naam in")
    current_person_name = st.text_input("Naam")
    if st.button("volgende"):
        st.session_state.current_person_name = current_person_name
        st.rerun()

else:
    # Render fill in choices page

    st.title(st.session_state.current_person_name + ", vul je voorkeur in")

    # filter out empty opties
    all_opties = sorted(
        [optie for optie in st.session_state.options.values() if len(optie) > 0]
    )

    # at most 5 voorkeuren can be set
    n_voorkeuren = min(len(all_opties), 5)

    already_selected_voorkeuren = []

    for i_voorkeur in range(n_voorkeuren):

        opties_for_this_box = all_opties.copy()
        # for already_selected_voorkeur in already_selected_voorkeuren:
        #     opties_for_this_box.remove(already_selected_voorkeur)

        st.selectbox(str(i_voorkeur + 1) + "e keus", opties_for_this_box)
        st.button("Versturen")
