import streamlit as st
import numpy as np
from scipy.optimize import linear_sum_assignment
import pandas as pd
from time import sleep


def optimise_choices(groep_details):

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

    st.header("Optimaliseren...")
    pbar = st.progress(0)

    for i in range(11):
        sleep(np.random.uniform(0.05, 0.4))
        pbar.progress(i * 10)

    # Solve the assignment problem using the Hungarian algorithm
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    st.success("Optimalisatie succesvol!")

    # Output the results
    total_score = -cost_matrix[row_ind, col_ind].sum()
    assignments = [(people[row], options[col]) for row, col in zip(row_ind, col_ind)]

    st.header("Verdeling na optimalisatie")

    assingment_results = pd.DataFrame(assignments, columns=["Persoon", "Uitkomst"])
    assingment_results["Plek"] = [
        str(cost_matrix[people.index(person), options.index(option)] + 1) + "e voorkeur"
        for (person, option) in assignments
    ]
    st.dataframe(assingment_results, hide_index=True)

    st.write(f"Totale score: {total_score}")
