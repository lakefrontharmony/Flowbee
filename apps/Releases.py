import streamlit as st
import pandas as pd
import numpy as np
import json

import Globals


def app():
	st.title('Release Metrics')
	if Globals.INPUT_CSV_DATAFRAME is not None:
		pipeline_info_file = st.sidebar.file_uploader("Select Pipeline Info JSON file", type='json')
	else:
		st.write('Please select an input csv file to continue.')
		return

	st.write('Complete the form on the sidebar to view results of release metrics.')

	if pipeline_info_file is not None:
		json_file = json.load(pipeline_info_file)
		df_1 = pd.json_normalize(json_file)
		df_2 = pd.json_normalize(df_1.iat[0, 0])
		found_entry = df_2[(df_2['slug'] == 'odm-withdrawals') & (df_2['statusMessage'] == 'Available')]
		st.write(found_entry.name)
		#st.json(json_file)