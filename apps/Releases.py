import streamlit as st
import pandas as pd
import json
from ReleaseMetricCalcClass import ReleaseMetricCalcClass


def app():
	st.title('Release Metrics')

	pipeline_info_file = st.sidebar.file_uploader("Select Pipeline Info JSON file", type='json')
	release_info_file = st.sidebar.file_uploader("Select Release Info UTF-8 CSV file", type='csv')

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
	json_calculator.read_json_file(pipeline_info_file)
	json_calculator.read_releases_csv_file(release_info_file)


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
