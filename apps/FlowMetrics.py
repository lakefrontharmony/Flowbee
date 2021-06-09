import streamlit as st
import pandas as pd
import numpy as np

import Globals


def app():

    if Globals.INPUT_CSV_DATAFRAME is not None:
        sprint_info_file = st.sidebar.file_uploader("Select Sprint Info File", type='csv')
        if sprint_info_file is not None:
            Globals.SPRINT_INFO_DATAFRAME = pd.read_csv(sprint_info_file)
            Globals.SPRINT_INFO_DATAFRAME.columns = Globals.SPRINT_INFO_DATAFRAME.columns.str.replace(' ', '')

            flow_form = st.sidebar.form('Monte Carlo Submit')
            start_col = flow_form.selectbox('Choose Start Status', Globals.INPUT_CSV_DATAFRAME.columns)
            end_col = flow_form.selectbox('Choose End Status', Globals.INPUT_CSV_DATAFRAME.columns)
            Globals.SPRINT_INFO_DATAFRAME.sort_values(by=['StartDate'], ascending=False, inplace=True, ignore_index=True)
            start_sprint = flow_form.selectbox('Choose Start Sprint', Globals.SPRINT_INFO_DATAFRAME['SprintName'])
            end_sprint = flow_form.selectbox('Choose End Sprint', Globals.SPRINT_INFO_DATAFRAME['SprintName'])
            categories_field = flow_form.selectbox('Do you have categories to group results?', Globals.INPUT_CSV_DATAFRAME.columns)
            daily_wip_limit = flow_form.number_input('Daily WIP limit', min_value=1, max_value=30, value=10,
                                                        step=1)
            submit_button = flow_form.form_submit_button(label='Calc My Flow')

    st.title('Flow Metrics')
    st.write('Complete the form on the sidebar to view results of flow metrics.')

    if Globals.INPUT_CSV_DATAFRAME is not None:
        if sprint_info_file is not None:
            if submit_button:
                st.write(f'start col:{start_col}, end col:{end_col}, start sprint:{start_sprint}, end sprint:{end_sprint}, '
                      f'using categories col:{categories_field}, and daily wip of {daily_wip_limit} items')