import streamlit as st
import pandas as pd
from ReleaseMetricCalcClass import ReleaseMetricCalcClass


def app():
	st.title('Release Metrics')

	pipeline_info_file = st.sidebar.file_uploader("Select Pipeline Info JSON file", type='json')
	release_info_file = st.sidebar.file_uploader("Select Release Info UTF-8 CSV file", type='csv')

	if pipeline_info_file is None:
		st.write('Please select a pipeline json file to continue.')
		return

	if release_info_file is None:
		st.write('Please select a UTF-8 CSV file of release information')
		return

	json_calculator = ReleaseMetricCalcClass()
	json_calculator.read_json_file(pipeline_info_file)
	json_calculator.read_releases_csv_file(release_info_file)
