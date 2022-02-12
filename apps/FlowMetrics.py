import streamlit as st
import pandas as pd
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

    sprint_info_file = st.sidebar.file_uploader("Select Sprint Info File", type='csv')
    if sprint_info_file is None:
        with open('Files/SprintData.csv') as file:
            Globals.SPRINT_INFO_DATAFRAME = pd.read_csv(file)
    else:
        Globals.SPRINT_INFO_DATAFRAME = pd.read_csv(sprint_info_file)

    Globals.SPRINT_INFO_DATAFRAME.columns = Globals.SPRINT_INFO_DATAFRAME.columns.str.replace(' ', '')
    try:
        Globals.SPRINT_INFO_DATAFRAME['StartDate'] = pd.to_datetime(Globals.SPRINT_INFO_DATAFRAME['StartDate'],
                                                                    format='%Y-%m-%d')
        Globals.SPRINT_INFO_DATAFRAME['EndDate'] = pd.to_datetime(Globals.SPRINT_INFO_DATAFRAME['EndDate'],
                                                                  format='%Y-%m-%d')
    except ValueError:
        st.write('Error parsing Sprint Data Dates. Make sure dates are YYYY-MM-DD format.')
        return

    flow_form = st.sidebar.form('Monte Carlo Submit')
    start_col = flow_form.selectbox('Choose Start Status', Globals.INPUT_CSV_DATAFRAME.columns)
    end_col = flow_form.selectbox('Choose End Status', Globals.INPUT_CSV_DATAFRAME.columns)
    Globals.SPRINT_INFO_DATAFRAME.sort_values(by=['StartDate'], ascending=False, inplace=True, ignore_index=True)
    start_sprint = flow_form.selectbox('Choose Start Sprint', Globals.SPRINT_INFO_DATAFRAME['SprintName'])
    end_sprint = flow_form.selectbox('Choose End Sprint', Globals.SPRINT_INFO_DATAFRAME['SprintName'])
    names_field = flow_form.selectbox('Do you have item names in a column?', Globals.INPUT_CSV_DATAFRAME.columns)
    categories_field = flow_form.selectbox('Do you have categories to group results?', Globals.INPUT_CSV_DATAFRAME.columns)
    daily_wip_limit = flow_form.number_input('Daily WIP limit', min_value=1, max_value=30, value=10,
                                                step=1)
    submit_button = flow_form.form_submit_button(label='Calc My Flow')

    if not submit_button:
        st.write('Complete the form on the sidebar to view results of flow metrics.')
        return

    if start_col == end_col:
        st.write('Please make sure the Start and End Status Columns are different')
        return

    calculator = FlowCalcClass(start_col, end_col, start_sprint, end_sprint, daily_wip_limit, names_field, categories_field, False, '')
    calculator.prep_for_metrics()
    if calculator.prep_errors_were_found():
        st.header(calculator.get_error_msgs())
        return

    calculator.run_flow_metrics()
    if calculator.calc_errors_were_found():
        st.header('Errors were found during calculations')
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
