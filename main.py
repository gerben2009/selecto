import streamlit as st
import json
from create_group import render_create_group
from group_overview import render_group_overview
from add_choices import render_add_choices
from optim import optimise_choices

if "groep_id" in st.query_params:
    st.session_state.groep_id = st.query_params.groep_id


# read groep
if "groep_id" in st.session_state:
    try:
        with open(st.session_state.groep_id + ".json", "r") as f:
            groep_details = json.load(f)
            if "current_action" in st.session_state:
                if st.session_state.current_action == "add_choices":
                    render_add_choices(groep_details)
                if st.session_state.current_action == "optim":
                    optimise_choices(groep_details)
                if st.session_state.current_action == "overview":
                    render_group_overview(groep_details)
            else:
                render_group_overview(groep_details)
    except FileNotFoundError:
        st.error("Groep niet gevonden!")
        render_create_group()
else:
    render_create_group()
