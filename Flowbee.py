import streamlit as st
import pandas as pd

from multiapp import MultiApp
from apps import Instructions, MCSimulation, FlowMetrics, Releases, Charts
import Globals

app = MultiApp()

st.set_page_config(layout='wide')
Globals.INPUT_CSV_DATAFRAME = None

st.markdown("""
# Flowbee Calculator
This is a calculator for agile metrics. It can run a Monte Carlo Simulation, Calculate standard Flow Metrics, and do
release metrics based on a json file and Jira Export csv file.
""")

app.add_app('Instructions', Instructions.app)
app.add_app('Monte Carlo', MCSimulation.app)
app.add_app('Flow Metrics', FlowMetrics.app)
app.add_app('Charts', Charts.app)
app.add_app('Release Metrics', Releases.app)

app.run()
