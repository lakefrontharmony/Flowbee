import streamlit as st
import pandas as pd
from datetime import timedelta, datetime
from SimulationCalcClass import SimulationCalcClass
import Globals


def app():
    st.title('Monte Carlo Simulations')

    uploaded_file = st.sidebar.file_uploader("Select Date File", type='csv')
    if uploaded_file is not None:
        Globals.INPUT_CSV_DATAFRAME = Globals.build_date_csv_file(uploaded_file)
    else:
        st.write('Please select a UTF-8 CSV file with "Flow" data to continue.')
        st.subheader('Expected format of CSV File:')
        display_example_csv_dataframe()
        return

    mc_form = st.sidebar.form('Monte Carlo Submit')
    start_col = mc_form.selectbox('Choose Start Status', Globals.INPUT_CSV_DATAFRAME.columns)
    end_col = mc_form.selectbox('Choose End Status', Globals.INPUT_CSV_DATAFRAME.columns)
    hist_duration = mc_form.selectbox('Choose Historical Duration for Monte Carlo', list(Globals.HIST_TIMEFRAME.keys()))
    sim_start_date = mc_form.date_input('Simulation Start Date', value=Globals.SIM_START_DATE)
    sim_end_date = mc_form.date_input('Simulation End Date', value=Globals.SIM_END_DATE)
    items_to_complete = mc_form.number_input('How Many items to complete? (Set to 0 to use # of In-Progress for Sim)',
                                             min_value=0, max_value=250, value=20, step=1)
    Globals.NUM_SIMULATION_ITERATIONS = mc_form.number_input('How Many iterations to run?', min_value=1000,
                                                             max_value=50000, value=10000, step=1000)
    submit_button = mc_form.form_submit_button(label='Run Simulation')

    if not submit_button:
        st.write('Complete the information on the sidebar to see results of a Monte Carlo simulation')
        return

    if start_col == end_col:
        st.write('Please make sure the Start and End Status Columns are different')
        return

    simulator = SimulationCalcClass(hist_duration, start_col, end_col, str(sim_start_date), str(sim_end_date),
                                    items_to_complete, datetime.today())
    simulator.prep_for_simulation()
    if not Globals.GOOD_FOR_GO:
        return
    simulator.run_mc_simulations(Globals.NUM_SIMULATION_ITERATIONS)

    if not Globals.SIMULATIONS_SUCCESSFUL:
        st.header('Error During simulations')
        return

    st.write(Globals.WORKING_PERCENTILES)
    st.header('Assumptions made during simulation')
    st.write(simulator.get_monte_carlo_assumptions())

    st.header('General Statistics of Simulations')
    st.write(Globals.MC_SIMULATION_STATS.astype(str))

    # Display "How Many" data
    st.header(f'How Many items will we complete by {sim_end_date}?')
    st.write(f'This grid helps you state, "After running {Globals.NUM_SIMULATION_ITERATIONS} simulations, '
             f'XX or more items completed in YY% of cases."')
    st.write(Globals.HOW_MANY_PERCENTILES.astype(str))
    # Results dataframe
    st.bar_chart(build_how_many_disp_df())

    # Display "When" data
    st.header(f'When will we finish {simulator.get_num_items_to_simulate()} items?')
    st.write(f'This grid helps you state, '
             f'"After running {Globals.NUM_SIMULATION_ITERATIONS} simulations, '
             f'{simulator.get_num_items_to_simulate()} or more items completed by yyyy-mm-dd"')
    st.write(Globals.WHEN_PERCENTILES.astype(str))
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


def display_example_csv_dataframe():
    st.write('You can as many date columns as your process needs, but they must be sequential and grouped together '
             '(no other columns between date columns).')
    st.write('You can also add additional columns for grouping or naming')
    example_df = pd.DataFrame([['Name of item', 'In Progress Date (YYYY-MM-DD)', 'Done Date (YYYY-MM-DD)',
                                'Yes or Blank', 'Category Name'],
                               ['Improve Sales', '2021-12-15', '2022-01-15', '', 'Strategic'],
                               ['Decrease Call Return Time', '2021-06-20', '2021-07-15', 'Yes', 'Maintenance']],
                              columns=['Name', 'In Progress', 'Done', 'Cancelled?', 'Grouping'])
    st.write(example_df)
