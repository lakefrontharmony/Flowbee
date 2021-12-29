import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
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
			ready_test = [0, 1, 1, 2, 4, 6, 8, 9, 10, 11]
			in_progress_test = [0, 0, 1, 1, 2, 2, 4, 5, 6, 6]
			closed_test = [0, 0, 0, 0, 1, 1, 2, 3, 4, 4]
			dict_test = {'Ready': ready_test, 'InProgress': in_progress_test, 'Closed': closed_test}
			df_test = pd.DataFrame(dict_test)
			st.area_chart(df_test)
			with st.expander('Stats:'):
				st.write('Insert CFD stats')

			# Horizontal Separator
			st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """,
						unsafe_allow_html=True)

			st.header('Aging Work In Progress (Aging WIP)')
			aging_wip_df = pd.DataFrame({'Name': ['Feature-1', 'Feature-2', 'Feature-3', 'Feature-4', 'Feature-5'],
										 'Status': ['3-Done', '2-In Progress', '2-In Progress', '1-Ready', '2-In Progress'],
										 'Age': [15, 20, 4, 1, 8]})
			alt_chart = alt.Chart(aging_wip_df).mark_circle(size=60).encode(
				x='Status',
				y='Age',
				color='Name',
				tooltip=['Name', 'Status', 'Age']
			).interactive()
			st.altair_chart(alt_chart, use_container_width=True)
			with st.expander('Stats:'):
				st.write('Insert aging WIP stats')
				st.write('Insert table of WIP durations')

			# Horizontal Separator
			st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """,
						unsafe_allow_html=True)

			st.header('WIP Run Chart')
			wip_pd = pd.DataFrame({'Date': ['2021-12-01', '2021-12-02', '2021-12-03', '2021-12-04', '2021-12-05'],
								   'WIP': [15, 15, 13, 17, 13],
								   'WIP Limit': [daily_wip_limit, daily_wip_limit, daily_wip_limit, daily_wip_limit,
												 daily_wip_limit]})
			wip_pd = wip_pd.set_index('Date')
			st.line_chart(wip_pd)
			with st.expander('Stats:'):
				st.write('Insert stats')

			# Horizontal Separator
			st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """,
						unsafe_allow_html=True)

			st.header('Throughput Histogram')
			throughput_numbers = [20, 10, 5, 3, 1, 0, 0, 1, 0, 0, 1]
			throughput_pd = pd.DataFrame(throughput_numbers, columns=['Throughput'])
			st.bar_chart(throughput_pd)
			with st.expander('Stats:'):
				st.write('Insert stats')

			# Horizontal Separator
			st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """,
						unsafe_allow_html=True)

			st.header('Throughput Run Chart')
			st.line_chart(wip_pd)
			with st.expander('Stats:'):
				st.write('Insert stats')

			# Horizontal Separator
			st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """,
						unsafe_allow_html=True)

			st.header('Cycle Time Histogram')
			st.bar_chart(throughput_pd)
			with st.expander('Stats:'):
				st.write('Insert stats')

			# Horizontal Separator
			st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """,
						unsafe_allow_html=True)

			st.header('Cycle Time Run Chart')
			st.line_chart(wip_pd)
			with st.expander('Stats:'):
				st.write('Insert stats')
