import streamlit as st
import pandas as pd
import json
import Globals


def app():
	st.title('Release Metrics')

	pipeline_info_file = st.sidebar.file_uploader("Select Pipeline Info JSON file", type='json')
	release_info_file = st.sidebar.file_uploader("Select Release Info UTF-8 CSV file", type='csv')

	if pipeline_info_file is None | release_info_file is None:
		st.write('Complete the form on the sidebar to view results of release metrics.')
		return

	json_file = json.load(pipeline_info_file)
	df_1 = pd.json_normalize(json_file)
	df_2 = pd.json_normalize(df_1.iat[0, 0])
	found_entry = df_2[(df_2['slug'] == 'odm-withdrawals') & (df_2['statusMessage'] == 'Available')]
	st.write(found_entry.name)
	#st.json(json_file)