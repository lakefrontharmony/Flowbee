import streamlit as st
import pandas as pd
import numpy as np
from glom import glom

import Globals


def app():
	if Globals.INPUT_CSV_DATAFRAME is not None:
		pipeline_info_file = st.sidebar.file_uploader("Select Pipeline Info JSON file", type='json')
		if pipeline_info_file is not None:
			# TODO: Convert this to json_normalize()
			Globals.PIPELINE_JSON_DATAFRAME = pd.read_json(pipeline_info_file)
			release_form = st.sidebar.form('Release Metrics')
			submit_button = release_form.form_submit_button('Run Release Metrics')

	st.title('Release Metrics')
	st.write('Complete the form on the sidebar to view results of release metrics.')

	if Globals.INPUT_CSV_DATAFRAME is not None:
		if Globals.PIPELINE_JSON_DATAFRAME is not None:
			if submit_button:
				st.write('Opened both files')
				print('=====')
				# print(v2_mask)
