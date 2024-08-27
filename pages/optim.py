import streamlit as st
import numpy as np
from scipy.optimize import linear_sum_assignment
import pandas as pd
from time import sleep
import json


def errorBack(msg):
    st.error(msg)
    sleep(1)
    st.switch_page("main.py")


def optimise_choices():
    try:
        with open(st.session_state.groep_id + ".json", "r") as f:
            groep_details = json.load(f)
    except AttributeError or FileNotFoundError:
        errorBack("Groep niet gevonden!")

    st.title("Selecto")

    table = pd.DataFrame.from_dict(groep_details["persoonsvoorkeuren"], orient="index")

    st.header("Scorematrix")
    # st.write(table)

    table = table.stack().reset_index()
    table.columns = ["persoon", "plek", "optie"]

    table2 = table.pivot(columns="optie", index="persoon", values="plek").astype(int)
    st.dataframe(
        "Plek " + (table2 + 1).astype(str),
    )

    people = list(table2.index)
    options = list(table2.columns)
    cost_matrix = table2.values

    if not groep_details["optimised"]:
        st.header("Optimaliseren...")
        pbar = st.progress(0)

        for i in range(11):
            sleep(np.random.uniform(0.05, 0.4))
            pbar.progress(i * 10)

        # Solve the assignment problem using the Hungarian algorithm
        row_ind, col_ind = linear_sum_assignment(cost_matrix)

        st.success("Optimalisatie succesvol!")

        # save the results
        groep_details["opt_row_ind"] = (row_ind).tolist()
        groep_details["opt_col_ind"] = (col_ind).tolist()
        groep_details["optimised"] = True

        with open(st.session_state.groep_id + ".json", "w") as f:
            json.dump(groep_details, f)
    else:
        row_ind = groep_details["opt_row_ind"]
        col_ind = groep_details["opt_col_ind"]

    st.header("Verdeling na optimalisatie")

    total_score = -cost_matrix[row_ind, col_ind].sum()
    assignments = [(people[row], options[col]) for row, col in zip(row_ind, col_ind)]

    assingment_results = pd.DataFrame(assignments, columns=["Persoon", "Uitkomst"])
    assingment_results["Plek"] = [
        str(cost_matrix[people.index(person), options.index(option)] + 1) + "e voorkeur"
        for (person, option) in assignments
    ]
    st.dataframe(assingment_results, hide_index=True)

    st.write(f"Totale score: {total_score}")


optimise_choices()
