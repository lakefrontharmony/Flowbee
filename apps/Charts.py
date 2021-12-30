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
		name_col = chart_form.selectbox('Choose Column Containing Item Names', Globals.INPUT_CSV_DATAFRAME.columns)
		daily_wip_limit = chart_form.number_input('Daily WIP limit', min_value=1, max_value=30, value=10,
												  step=1)
		chart_start_date = chart_form.date_input('Data Start Date', value=date.today() - timedelta(days=90))
		submit_button = chart_form.form_submit_button(label='Build Charts')

	st.title('Charts')
	st.write('Complete the form on the sidebar to view charts.')

	if Globals.INPUT_CSV_DATAFRAME is not None:
		if submit_button:
			chart_builder = ChartBuilderClass(start_col, end_col, name_col, str(chart_start_date), daily_wip_limit)
			chart_builder.prep_for_charting()
			if not Globals.GOOD_FOR_GO:
				st.write(chart_builder.get_errors())
				return

			chart_builder.build_charts()
			if not Globals.CHARTS_BUILT_SUCCESSFULLY:
				st.write(chart_builder.get_errors())
				return

			# st.header('Cumulative Flow Diagram (CFD)')
			cfd_chart = alt.Chart(chart_builder.get_cfd_df(), title='Cumulative Flow Diagram (CFD)').transform_fold(
				chart_builder.get_date_column_list(), as_=['status', 'count']).\
				mark_area(opacity=0.75).encode(
				x='Date:T',
				y=alt.Y('count:Q', stack=None),
				color='status:N'
			)
			st.altair_chart(cfd_chart)
			# TODO: Create CFD Stats
			# st.write('Insert CFD stats')

			# Horizontal Separator
			st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """,
						unsafe_allow_html=True)

			# st.header('Aging Work In Progress (Aging WIP)')
			st.header('WORK IN PROGRESS, NOT FUNCTIONING YET')
			alt_chart = alt.Chart(chart_builder.get_aging_wip_df(), title="Aging WIP").mark_circle(size=60).encode(
				x='Status',
				y='Age',
				color='Status',
				tooltip=['Name', 'Status', 'Age']
			).interactive()
			st.altair_chart(alt_chart, use_container_width=True)
			# TODO: Create Aging WIP Stats
			# st.write('Insert aging WIP stats')
			# st.write('Insert table of WIP durations')

			# Horizontal Separator
			st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """,
						unsafe_allow_html=True)

			# st.header('WIP Run Chart')
			wip_run_chart = alt.Chart(chart_builder.get_run_df(), title="WIP Run Chart")
			wip_line = wip_run_chart.mark_line(point=alt.OverlayMarkDef(color="red")).encode(
				x='Date:T',
				y='WIP:Q'
			)

			# TODO: Get Daily Average to display correctly
			# wip_limit = wip_run_chart.mark_rule(strokeDash=[12, 6], size=2).encode(
			#	y=alt.YValue(daily_wip_limit)
			#)
			st.altair_chart(wip_line)
			# TODO: Create WIP Run Stats
			# st.write('Insert stats')

			# Horizontal Separator
			st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """,
						unsafe_allow_html=True)

			# st.header('Throughput Histogram')

			throughput_hist_graph = alt.Chart(chart_builder.get_throughput_hist_df(), title="Throughput Histogram")
			bar_graph = throughput_hist_graph.mark_bar(size=40).encode(
				x='count:Q',
				y='Throughput:Q'
			)
			st.altair_chart(bar_graph)
			# TODO: Create Throughput Run Stats
			# st.write('Insert stats')

			# Horizontal Separator
			st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """,
						unsafe_allow_html=True)

			st.header('Throughput Run Chart')
			throughput_run_chart = alt.Chart(chart_builder.get_run_df())
			throughput_line = throughput_run_chart.mark_line(point=alt.OverlayMarkDef(color="red")).encode(
				x='Date:T',
				y='Throughput:Q'
			)
			st.altair_chart(throughput_line)
			# TODO: Create Throughput Run Stats
			# st.write('Insert stats')

			# Horizontal Separator
			st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """,
						unsafe_allow_html=True)

			st.header('Cycle Time Histogram')
			# st.bar_chart(throughput_pd)
			st.write('Insert stats')

			# Horizontal Separator
			st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """,
						unsafe_allow_html=True)

			st.header('Cycle Time Run Chart')
			# st.line_chart(wip_pd)
			st.write('Insert stats')
