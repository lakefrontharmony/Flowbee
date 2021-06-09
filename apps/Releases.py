import streamlit as st
import pandas as pd
import numpy as np

import Globals


def app():
	if Globals.INPUT_CSV_DATAFRAME is not None:
		release_form = st.sidebar.form('Release Metrics')
		start_sprint = release_form.selectbox('Choose Start Sprint', Globals.HIST_TIMEFRAME)
		end_sprint = release_form.selectbox('Choose End Sprint', Globals.HIST_TIMEFRAME)
		submit_button = release_form.form_submit_button('Run Release Metrics')

	st.title('Release Metrics')
	st.write('Complete the form on the sidebar to view results of release metrics.')

	if submit_button:
		st.write(f'start sprint:{start_sprint}, end sprint:{end_sprint}')
