import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import date, timedelta
import Globals
from ChartBuilderClass import ChartBuilderClass


def app():
	st.title('Charts')

	if Globals.INPUT_CSV_DATAFRAME is not None:
		chart_form = st.sidebar.form('Charts Form')
		start_col = chart_form.selectbox('Choose Start Status', Globals.INPUT_CSV_DATAFRAME.columns)
		end_col = chart_form.selectbox('Choose End Status', Globals.INPUT_CSV_DATAFRAME.columns)
		name_col = chart_form.selectbox('Choose Column Containing Item Names', Globals.INPUT_CSV_DATAFRAME.columns)
		daily_wip_limit = chart_form.number_input('Daily WIP limit', min_value=1, max_value=30, value=10,
												  step=1)
		use_start_date = chart_form.checkbox('Check to specify a starting date below:')
		chart_start_date = chart_form.date_input('Data Start Date', value=date.today() - timedelta(days=90))
		submit_button = chart_form.form_submit_button(label='Build Charts')
	else:
		st.write('Please select an input csv file to continue.')
		return

	if not submit_button:
		st.write('Complete the form on the sidebar to view charts.')
		return

	# This markdown fixes the tooltip overlay for charts when you go to full screen mode.
	st.markdown('<style>#vg-tooltip-element{z-index: 1000051}</style>',
				unsafe_allow_html=True)

	# =========================================
	# Build Chart Data
	# =========================================
	chart_builder = ChartBuilderClass(start_col, end_col, name_col, use_start_date, str(chart_start_date), daily_wip_limit)
	chart_builder.prep_for_charting()
	if not Globals.GOOD_FOR_GO:
		st.write(chart_builder.get_errors())
		return

	chart_builder.build_charts()
	if not Globals.CHARTS_BUILT_SUCCESSFULLY:
		st.write(chart_builder.get_errors())
		return

	st.write(build_helpful_tips())

	# Horizontal Separator
	st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """,
				unsafe_allow_html=True)

	st.header('Raw reference Data:')
	st.write(chart_builder.get_clean_df())

	# Horizontal Separator
	st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """,
				unsafe_allow_html=True)

	# =========================================
	# Flow and In-Progress Charts
	# =========================================
	# ===== CUMULATIVE FLOW DIAGRAM (CFD) =====
	cfd_df = chart_builder.get_cfd_df()
	cfd_columns = cfd_df.columns.tolist()
	cfd_chart = alt.Chart(cfd_df, title='Cumulative Flow Diagram (CFD)').transform_fold(
		chart_builder.get_date_column_list(), as_=['Status', 'Count'])
	cfd_lines = cfd_chart.mark_area(opacity=0.75).encode(
		x=alt.X('Date:T', title='Date'),
		y=alt.Y('Count:Q', stack=None),
		color=alt.Color('Status:N', legend=alt.Legend(title='Categories')),
		tooltip=cfd_columns
	).interactive()

	cfd_vectors = alt.Chart(chart_builder.get_cfd_vectors()).mark_line().encode(
		x=alt.X('Date:T', title='Date'),
		y=alt.Y('Count:Q', title='Trajectory'),
		color=alt.Color('Status:N')
	).interactive()
	# stack these two charts vertically, not overlaid
	st.altair_chart(cfd_lines & cfd_vectors)
	# TODO: Enhance CFD Stats
	# show_cfd_stats = st.checkbox('Show CFD Stats')
	st.write(chart_builder.get_cfd_df())

	# Horizontal Separator
	st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """,
				unsafe_allow_html=True)

	# ===== AGING WIP =====
	aging_df = chart_builder.get_aging_wip_df()
	aging_columns = aging_df.columns.tolist()
	aging_chart = alt.Chart(aging_df, title="Aging WIP")
	aging_wip = aging_chart.mark_circle(size=60).encode(
		x=alt.X('Status', title='Status'),
		y=alt.Y('Age', title='Age'),
		color='Status',
		tooltip=aging_columns
	).interactive()
	cycle_time_85_confidence_y = aging_chart.mark_rule(strokeDash=[12, 6], size=2, color='red').encode(
		y='CycleTime85:Q'
	)
	cycle_time_50_confidence_y = aging_chart.mark_rule(strokeDash=[12, 6], size=2, color='green').encode(
		y='CycleTime50:Q'
	)
	cycle_time_average_y = aging_chart.mark_rule(strokeDash=[12, 6], size=2, color='black').encode(
		y='CycleTimeAvg:Q'
	)
	label_85 = aging_chart.mark_text(align='right', baseline='bottom', dx=40, color='red').encode(
		alt.X('Status', aggregate='max'),
		alt.Y('CycleTime85:Q'),
		alt.Text('CycleTime85:Q')
	)
	label_50 = aging_chart.mark_text(align='right', baseline='bottom', dx=60, color='green').encode(
		alt.X('Status', aggregate='max'),
		alt.Y('CycleTime50:Q'),
		alt.Text('CycleTime50:Q')
	)
	label_avg = aging_chart.mark_text(align='right', baseline='bottom', dx=40, color='black').encode(
		alt.X('Status', aggregate='max'),
		alt.Y('CycleTimeAvg:Q'),
		alt.Text('CycleTimeAvg:Q')
	)
	st.altair_chart(aging_wip + cycle_time_85_confidence_y + cycle_time_50_confidence_y + cycle_time_average_y +
					label_85 + label_50 + label_avg, use_container_width=True)
	# TODO: Enhance Aging WIP Stats
	st.write(chart_builder.get_aging_wip_df())

	# Horizontal Separator
	st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """,
				unsafe_allow_html=True)

	# ===== WIP RUN CHART =====
	wip_run_chart = alt.Chart(chart_builder.get_run_df(), title="WIP Run Chart")
	wip_line = wip_run_chart.mark_line(point=alt.OverlayMarkDef(color="red")).encode(
		x=alt.X('Date:T', title='Date'),
		y=alt.Y('WIP:Q', title='WIP'),
		tooltip=['Date', 'WIP']
	).interactive()
	average_wip = wip_run_chart.mark_line(color='black').transform_window(
		rolling_mean='mean(WIP)',
		frame=[-30, 30],
		groupby=['WIPLimit']
	).encode(
		x='Date:T',
		y='rolling_mean:Q'
	)
	wip_limit = wip_run_chart.mark_rule(strokeDash=[12, 6], size=2, color='blue').encode(
		y='WIPLimit:Q'
	)
	label_wip = wip_run_chart.mark_text(align='right', baseline='bottom', dx=-20, color='black').encode(
		alt.X('Date:T', aggregate='max'),
		alt.Y('WIPLimit:Q'),
		alt.Text('WIPLimit:Q')
	)
	st.altair_chart(wip_line + wip_limit + label_wip + average_wip)
	# TODO: Enhance WIP Run Stats
	st.write(chart_builder.get_run_df())

	# Horizontal Separator
	st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """,
				unsafe_allow_html=True)

	# =========================================
	# Throughput Charts
	# =========================================
	# ===== THROUGHPUT HISTOGRAM =====
	throughput_hist_graph = alt.Chart(chart_builder.get_throughput_hist_df(), title="Throughput Histogram")
	bar_graph = throughput_hist_graph.mark_bar(size=40).encode(
		x=alt.X('Throughput:Q', title='Throughput'),
		y=alt.Y('Count:Q', title='Count'),
		tooltip=['Throughput', 'Count']
	).interactive()
	throughput_85_confidence = throughput_hist_graph.mark_rule(strokeDash=[12, 6], size=2, color='red').encode(
		x='Throughput85:Q'
	)
	throughput_50_confidence = throughput_hist_graph.mark_rule(strokeDash=[12, 6], size=2, color='green').encode(
		x='Throughput50:Q'
	)
	throughput_avg = throughput_hist_graph.mark_rule(strokeDash=[12, 6], size=2, color='black').encode(
		x='ThroughputAvg:Q'
	)
	throughput_hist_label_85 = throughput_hist_graph.mark_text(align='right', baseline='top', dx=-20, color='red').encode(
		alt.X('Throughput85:Q'),
		alt.Y('Count:Q', aggregate='mean'),
		alt.Text('Throughput85:Q')
	)
	throughput_hist_label_50 = throughput_hist_graph.mark_text(align='right', baseline='top', dx=-20,
															   color='green').encode(
		alt.X('Throughput50:Q'),
		alt.Y('Count:Q', aggregate='mean'),
		alt.Text('Throughput50:Q')
	)
	throughput_hist_label_avg = throughput_hist_graph.mark_text(align='right', baseline='top', dx=-20,
															   color='black').encode(
		alt.X('ThroughputAvg:Q'),
		alt.Y('Count:Q', aggregate='mean'),
		alt.Text('ThroughputAvg:Q')
	)
	st.altair_chart(bar_graph + throughput_85_confidence + throughput_50_confidence + throughput_avg +
					throughput_hist_label_85 + throughput_hist_label_50 + throughput_hist_label_avg)
	# TODO: Enhance Throughput Run Stats
	st.write(chart_builder.get_throughput_hist_df())

	# Horizontal Separator
	st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """,
				unsafe_allow_html=True)

	# ===== THROUGHPUT RUN CHART =====
	throughput_run_chart = alt.Chart(chart_builder.get_run_df(), title="Throughput Run Chart")
	throughput_line = throughput_run_chart.mark_line(point=alt.OverlayMarkDef(color="red")).encode(
		x='Date:T',
		y='Throughput:Q',
		tooltip=['Date', 'Throughput']
	).interactive()
	# TODO: Build in 85% horizontal line for Throughput
	st.altair_chart(throughput_line)
	# TODO: Create Enhance Run Stats
	st.write(chart_builder.get_run_df())

	# Horizontal Separator
	st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """,
				unsafe_allow_html=True)

	# =========================================
	# Cycle Time Charts
	# =========================================
	# ===== CYCLE TIME HISTOGRAM =====
	cycle_time_hist_graph = alt.Chart(chart_builder.get_cycle_time_hist_df(), title="Cycle Time Histogram")
	bar_graph = cycle_time_hist_graph.mark_bar(size=4).encode(
		x=alt.X('Age:Q', title='Age'),
		y=alt.Y('Count:Q', title='Count'),
		tooltip=['Age', 'Count']
	).interactive()
	cycle_time_85_confidence = cycle_time_hist_graph.mark_rule(strokeDash=[12, 6], size=2, color='red').encode(
		x='CycleTime85:Q'
	)
	cycle_time_50_confidence = cycle_time_hist_graph.mark_rule(strokeDash=[12, 6], size=2, color='green').encode(
		x='CycleTime50:Q'
	)
	cycle_time_avg = cycle_time_hist_graph.mark_rule(strokeDash=[12, 6], size=2, color='black').encode(
		x='CycleTimeAvg:Q'
	)
	cycle_time_hist_label_85 = cycle_time_hist_graph.mark_text(align='right', baseline='top', dx=-20,
															   color='red').encode(
		alt.X('CycleTime85:Q'),
		alt.Y('Count:Q', aggregate='mean'),
		alt.Text('CycleTime85:Q')
	)
	cycle_time_hist_label_50 = cycle_time_hist_graph.mark_text(align='right', baseline='top', dx=-20,
															   color='green').encode(
		alt.X('CycleTime50:Q'),
		alt.Y('Count:Q', aggregate='mean'),
		alt.Text('CycleTime50:Q')
	)
	cycle_time_hist_label_avg = cycle_time_hist_graph.mark_text(align='right', baseline='top', dx=-20,
																color='black').encode(
		alt.X('CycleTimeAvg:Q'),
		alt.Y('Count:Q', aggregate='mean'),
		alt.Text('CycleTimeAvg:Q')
	)
	st.altair_chart(bar_graph + cycle_time_85_confidence + cycle_time_50_confidence + cycle_time_avg +
					cycle_time_hist_label_85 + cycle_time_hist_label_50 + cycle_time_hist_label_avg)
	# TODO: Enhance Cycle Time Histogram Stats
	st.write(chart_builder.get_cycle_time_hist_df())

	# Horizontal Separator
	st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """,
				unsafe_allow_html=True)

	# ===== CYCLE TIME SCATTERPLOT =====
	cycle_scatter_chart = alt.Chart(chart_builder.get_cycle_time_scatter_df(), title="Cycle Time Scatterplot")
	scatter_plot = cycle_scatter_chart.mark_circle(size=60).encode(
		x=alt.X('Done_Date:T', title='Completed Date'),
		y=alt.Y('Age:Q', title='Age'),
		tooltip=['Name', 'Age', 'Done_Date']
	).interactive()
	cycle_time_85_confidence_y = cycle_scatter_chart.mark_rule(strokeDash=[12, 6], size=2, color='red').encode(
		y='CycleTime85:Q'
	)
	cycle_time_50_confidence_Y = cycle_scatter_chart.mark_rule(strokeDash=[12, 6], size=2, color='green').encode(
		y='CycleTime50:Q'
	)
	cycle_time_average_y = cycle_scatter_chart.mark_rule(strokeDash=[12, 6], size=2, color='black').encode(
		y='CycleTimeAvg:Q'
	)
	label_85 = cycle_scatter_chart.mark_text(align='right', baseline='bottom', dx=-20, color='red').encode(
		alt.X('Done_Date:T', aggregate='max'),
		alt.Y('CycleTime85:Q'),
		alt.Text('CycleTime85:Q')
	)
	label_50 = cycle_scatter_chart.mark_text(align='right', baseline='bottom', dx=-20, color='green').encode(
		alt.X('Done_Date:T', aggregate='max'),
		alt.Y('CycleTime50:Q'),
		alt.Text('CycleTime50:Q')
	)
	label_avg = cycle_scatter_chart.mark_text(align='right', baseline='bottom', dx=-20, color='black').encode(
		alt.X('Done_Date:T', aggregate='max'),
		alt.Y('CycleTimeAvg:Q'),
		alt.Text('CycleTimeAvg:Q')
	)
	st.altair_chart(scatter_plot + cycle_time_85_confidence_y + cycle_time_50_confidence_Y + cycle_time_average_y
					+ label_85 + label_50 + label_avg,
					use_container_width=True)
	# TODO: Enhance Cycle Time Stats
	st.write(chart_builder.get_cycle_time_scatter_df())

def build_helpful_tips():
	tips_list = [['Red dashed lines = 85% confidence level'], ['Green dashed lines = 50% confidence level'],
				 ['Black dashed lines = Average of data'],
				 ['Click the "View Full screen" arrows at the right side of any chart to see it in full-screen'],
				 ['Dataframes have been included below charts to show you the raw data']]
	return pd.DataFrame(tips_list, columns=['Tips'])
