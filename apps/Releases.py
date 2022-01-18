import streamlit as st
import pandas as pd
import json
from datetime import date, timedelta
from ReleaseMetricCalcClass import ReleaseMetricCalcClass


def app():
	st.title('Release Metrics')

	pipeline_info_file = st.sidebar.file_uploader("Select Pipeline Info JSON file", type='json')
	release_info_file = st.sidebar.file_uploader("Select Release Info UTF-8 CSV file", type='csv')
	release_form = st.sidebar.form('Would you like to limit your metrics to a date range?')
	release_form.subheader('Fill out dates and submit to limit the results:')
	start_date = release_form.date_input('Start Date', value=date.today() - timedelta(days=90))
	end_date = release_form.date_input('End Date', value=date.today())
	submit_button = release_form.form_submit_button(label='Submit')

	if pipeline_info_file is None:
		st.header('Please select a pipeline json file to continue.')
		st.subheader('Expected Format of Pipeline Info json file')
		display_example_json_df()
		return

	if release_info_file is None:
		st.header('Please select a UTF-8 CSV file of release information')
		st.subheader('Expected Format of Release Information File')
		display_example_csv_df()
		return

	json_calculator = ReleaseMetricCalcClass()
	json_calculator.prepare_for_metrics(pipeline_info_file, release_info_file)
	if submit_button:
		json_calculator.run_release_metrics(start_date, end_date)
	else:
		json_calculator.run_release_metrics()

	st.subheader('Results')
	st.write(json_calculator.get_release_df())
	st.subheader('Summary')
	st.write(json_calculator.get_release_summary_df())


# =========================================
# Internal Functions
# =========================================
def display_example_json_df():
	st.write('Each item in the pipeline must have a "slug" and "statusMessage" (Available = considered active).')
	json_file = open('Files/pipeline_example.json')
	display_json = json.load(json_file)
	st.json(display_json)


def display_example_csv_df():
	example_df = pd.DataFrame([['name_of_system version', 'date_of_release (YYYY-MM-DD)'],
							   ['mainframe_release 1.0.0', '2021-12-15'],
							   ['apigee_release 5.6.1', '2022-01-05']], columns=['Fix Version/s', 'Date'])
	st.write(example_df)
