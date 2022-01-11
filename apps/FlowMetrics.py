import streamlit as st
import pandas as pd
from FlowCalcClass import FlowCalcClass

import Globals


def app():
    st.title('Flow Metrics')
    if Globals.INPUT_CSV_DATAFRAME is not None:
        sprint_info_file = st.sidebar.file_uploader("Select Sprint Info File", type='csv')
        if sprint_info_file is not None:
            Globals.SPRINT_INFO_DATAFRAME = pd.read_csv(sprint_info_file)
            Globals.SPRINT_INFO_DATAFRAME.columns = Globals.SPRINT_INFO_DATAFRAME.columns.str.replace(' ', '')
            Globals.SPRINT_INFO_DATAFRAME['StartDate'] = pd.to_datetime(Globals.SPRINT_INFO_DATAFRAME['StartDate'],
                                                                        format='%Y-%m-%d')
            Globals.SPRINT_INFO_DATAFRAME['EndDate'] = pd.to_datetime(Globals.SPRINT_INFO_DATAFRAME['EndDate'],
                                                                        format='%Y-%m-%d')

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
            # ToDo: Stop submission if the start and end sprint are the same column name. Causes errors downstream.
            submit_button = flow_form.form_submit_button(label='Calc My Flow')
        else:
            st.write('Please select a Sprint Info File input csv to continue.')
            return
    else:
        st.write('Please select an input csv file to continue.')
        return

    if not submit_button:
        st.write('Complete the form on the sidebar to view results of flow metrics.')
        return

    calculator = FlowCalcClass(start_col, end_col, start_sprint, end_sprint, daily_wip_limit, names_field, categories_field, False, '')
    calculator.prep_for_metrics()
    if not Globals.GOOD_FOR_GO:
        st.write(calculator.get_error_msgs())
        return
    calculator.run_flow_metrics()

    st.header('Assumptions made during calculations')
    st.write(calculator.get_flow_metric_assumptions())
    st.header('General Statistics of Metrics')
    st.write(Globals.FLOW_METRIC_STATS)
    st.header('Completed Items')
    st.write(calculator.get_completed_item_names())
    st.header('Flow Metric Results')
    st.write(Globals.FLOW_METRIC_RESULTS)
    st.header('Categorical Results')
    st.write(Globals.FLOW_METRIC_CATEGORY_RESULTS)
