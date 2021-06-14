import streamlit as st
import pandas as pd
import numpy as np
from datetime import timedelta
from SimulationCalcClass import SimulationCalcClass

import Globals


def app():
    if Globals.INPUT_CSV_DATAFRAME is not None:
        mc_form = st.sidebar.form('Monte Carlo Submit')
        start_col = mc_form.selectbox('Choose Start Status', Globals.INPUT_CSV_DATAFRAME.columns)
        end_col = mc_form.selectbox('Choose End Status', Globals.INPUT_CSV_DATAFRAME.columns)
        hist_duration = mc_form.selectbox('Choose Historical Duration for Monte Carlo', list(Globals.HIST_TIMEFRAME.keys()))
        sim_start_date = mc_form.date_input('Simulation Start Date', value=Globals.SIM_START_DATE)
        sim_end_date = mc_form.date_input('Simulation End Date', value=Globals.SIM_END_DATE)
        items_to_complete = mc_form.number_input('How Many items to complete?', min_value=0, max_value=50, value=20,
                                                    step=1)
        Globals.NUM_SIMULATION_ITERATIONS = mc_form.number_input('How Many iterations to run?', min_value=1000, max_value=50000,
                                                    value=10000,
                                                    step=1000)
        submit_button = mc_form.form_submit_button(label='Run Simulation')

    st.title('Monte Carlo Simulations')
    st.write('Complete the information on the sidebar to see results of a Monte Carlo simulation')

    if Globals.INPUT_CSV_DATAFRAME is not None:
        if submit_button:
            simulator = SimulationCalcClass(hist_duration, start_col, end_col, str(sim_start_date), str(sim_end_date), items_to_complete)
            simulator.prep_for_simulation()
            if not Globals.GOOD_FOR_GO:
                return
            simulator.run_mc_simulations(Globals.NUM_SIMULATION_ITERATIONS)

            st.header('Assumptions made during simulation')
            st.write(simulator.get_monte_carlo_assumptions())

            st.header('General Statistics of Simulations')
            st.write(Globals.MC_SIMULATION_STATS)

            # Display "How Many" data
            st.header(f'How Many items will we complete by {sim_end_date}?')
            st.write('This grid helps you state, "With xx% confidence I can say we will complete "yy" items"')
            st.write(Globals.HOW_MANY_PERCENTILES)
            # Results dataframe
            st.bar_chart(build_how_many_disp_df())

            # Display "When" data
            st.header(f'When will we finish {items_to_complete} items?')
            st.write(f'This grid helps you state, '
                     f'"With xx% confidence I can say we will complete {items_to_complete} items by yyyy/mm/dd"')
            st.write(Globals.WHEN_PERCENTILES)
            # Results dataframe
            st.bar_chart(build_when_disp_df())


def build_how_many_disp_df():
    how_many_results = Globals.HOW_MANY_SIM_OUTPUT.value_counts(sort=False).to_frame().reset_index()
    how_many_results.columns = ['Count', 'Output']
    # Convert the Count to an index of the df and then drop the 'Count' column
    how_many_results = how_many_results.set_index(how_many_results['Count'])
    return how_many_results.drop(['Count'], axis=1)


def build_when_disp_df():
    when_results = Globals.WHEN_SIM_OUTPUT.value_counts(sort=False).to_frame().reset_index()
    when_results.columns = ['End_date', 'Output']
    when_results['End_date'] = when_results['End_date'].apply(lambda duration:
                                                              Globals.SIM_START_DATE + timedelta(days=duration))
    # Convert the End_date to an index of the df and then drop the 'End_date' column
    when_results = when_results.set_index(when_results['End_date'])
    return when_results.drop(['End_date'], axis=1)
