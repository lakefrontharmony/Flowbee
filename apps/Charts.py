import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta
import Globals
from ChartBuilderClass import ChartBuilderClass


def app():
	if Globals.INPUT_CSV_DATAFRAME is not None:
		chart_form = st.sidebar.form('Charts Form')
		start_col = chart_form.selectbox('Choose Start Status', Globals.INPUT_CSV_DATAFRAME.columns)
		end_col = chart_form.selectbox('Choose End Status', Globals.INPUT_CSV_DATAFRAME.columns)
		daily_wip_limit = chart_form.number_input('Daily WIP limit', min_value=1, max_value=30, value=10,
												 step=1)
		chart_start_date = chart_form.date_input('Data Start Date', value=date.today() - timedelta(days=90))
		submit_button = chart_form.form_submit_button(label='Build Charts')

	st.title('Charts')
	st.write('Complete the form on the sidebar to view charts.')

	if Globals.INPUT_CSV_DATAFRAME is not None:
		if submit_button:
			chart_builder = ChartBuilderClass(start_col, end_col, str(chart_start_date), daily_wip_limit)
			chart_builder.prep_for_charting()
			if not Globals.GOOD_FOR_GO:
				# TODO: Display errors
				st.write('Errors during chart preparation')
				return

			chart_builder.build_charts()
			if not Globals.CHARTS_BUILT_SUCCESSFULLY:
				# TODO: Display errors
				st.write('Errors during chart builds')
				return

			st.header('Cumulative Flow Diagram (CFD)')
			st.write('Insert CFD')
			st.write('Insert CFD stats')

			st.header('Aging Work In Progress (Aging WIP)')
			st.write('Insert chart')
			st.write('Insert aging WIP stats')
			st.write('Insert table of WIP durations')

			st.header('WIP Run Chart')
			st.write('Insert Chart')
			st.write('Insert stats')

			st.header('Throughput Histogram')
			st.write('Insert chart')
			st.write('Insert stats')

			st.header('Throughput Run Chart')
			st.write('Insert chart')
			st.write('Insert stats')

			st.header('Cycle Time Histogram')
			st.write('Insert chart')
			st.write('Insert stats')

			st.header('Cycle Time Run Chart')
			st.write('Insert chart')
			st.write('Insert stats')
