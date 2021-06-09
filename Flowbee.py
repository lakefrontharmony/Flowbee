import streamlit as st
import pandas as pd

from multiapp import MultiApp
from apps import MCSimulation, FlowMetrics, Releases
import Globals

app = MultiApp()

uploaded_file = st.sidebar.file_uploader("Select Date File", type='csv')
if uploaded_file is not None:
	Globals.INPUT_CSV_DATAFRAME = pd.read_csv(uploaded_file)
	Globals.INPUT_CSV_DATAFRAME.columns = Globals.INPUT_CSV_DATAFRAME.columns.str.replace(' ', '')

st.markdown("""
# Flowbee Calculator
This is a calculator for agile metrics. It can run a Monte Carlo Simulation, Calculate standard Flow Metrics, and do
release metrics based on a json file and Jira Export csv file.
""")

app.add_app('Monte Carlo', MCSimulation.app)
app.add_app('Flow Metrics', FlowMetrics.app)
app.add_app('Release Metrics', Releases.app)

app.run()