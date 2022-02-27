import streamlit as st
import pandas as pd
from datetime import date, timedelta
from FlowCalcClass import FlowCalcClass
import Globals


def app():
    st.title('Flow Metrics')

    uploaded_file = st.sidebar.file_uploader("Select Date File", type='csv')
    if uploaded_file is not None:
        Globals.INPUT_CSV_DATAFRAME = Globals.build_date_csv_file(uploaded_file)
    else:
        st.write('Please select a UTF-8 CSV file with "Flow" data to continue.')
        st.subheader('Expected format of CSV File:')
        display_example_csv_dataframe()
        return

    flow_form = st.sidebar.form('Monte Carlo Submit')
    start_col = flow_form.selectbox('Choose Start Status', Globals.INPUT_CSV_DATAFRAME.columns)
    end_col = flow_form.selectbox('Choose End Status', Globals.INPUT_CSV_DATAFRAME.columns)
    start_date = flow_form.date_input('Calculation Start Date', value=(date.today() - timedelta(days=13)))
    end_date = flow_form.date_input('Calculation End Date', value=date.today())
    names_field = flow_form.selectbox('Do you have item names in a column?', Globals.INPUT_CSV_DATAFRAME.columns)
    categories_field = flow_form.selectbox('Do you have categories to group results?', Globals.INPUT_CSV_DATAFRAME.columns)
    daily_wip_limit = flow_form.number_input('Daily WIP limit', min_value=1, max_value=30, value=10,
                                                step=1)
    submit_button = flow_form.form_submit_button(label='Calc My Flow')

    if not submit_button:
        st.header('Complete the form on the sidebar to view results of flow metrics.')
        return

    if start_col == end_col:
        st.header('Please make sure the Start and End Status Columns are different')
        return

    calculator = FlowCalcClass(start_col, end_col, str(start_date), str(end_date), daily_wip_limit, names_field, categories_field, False, '')
    calculator.prep_for_metrics()
    if calculator.prep_errors_were_found():
        st.header('Errors were found during calculations')
        st.header(calculator.get_error_msgs())
        return

    calculator.run_flow_metrics()
    if calculator.calc_errors_were_found():
        st.header('Errors were found during calculations')
        st.header(calculator.get_error_msgs())
        return

    st.header('Assumptions made during calculations')
    st.write(calculator.get_flow_metric_assumptions())
    st.header('General Statistics of Metrics')
    st.write(calculator.get_flow_metric_stats().astype(str))
    st.header('Completed Items')
    st.write(calculator.get_completed_item_names())
    st.header('Flow Metric Results')
    st.write(calculator.get_flow_metric_results().astype(str))
    st.header('Categorical Results')
    st.write(calculator.get_flow_metric_category_results().astype(str))


def display_example_csv_dataframe():
    st.write('You can as many date columns as your process needs, but they must be sequential and grouped together '
             '(no other columns between date columns).')
    st.write('You can also add additional columns for grouping or naming')
    st.write('Cancelled items should be denoted with either a "Cancelled" column, or a "Status" column which has'
             '"Yes" or "Cancelled" for the applicable rows.')
    example_df = pd.DataFrame([['Name of item', 'In Progress Date (YYYY-MM-DD)', 'Done Date (YYYY-MM-DD)',
                                'Yes or Blank', 'Category Name'],
                               ['Improve Sales', '2021-12-15', '2022-01-15', '', 'Strategic'],
                               ['Decrease Call Return Time', '2021-06-20', '2021-07-15', 'Yes', 'Maintenance']],
                              columns=['Name', 'In Progress', 'Done', 'Cancelled', 'Grouping'])
    st.write(example_df)


def display_example_sprint_csv_dataframe():
    example_df = pd.DataFrame([['Name of Sprint', 'YYYY-MM-DD', 'YYYY-MM-DD'],
                               ['2201.1', '2022-01-19', '2022-02-01'],
                               ['2201.2', '2022-02-02', '2022-02-15']],
                              columns=['SprintName', 'StartDate', 'EndDate'])
    st.write(example_df)
