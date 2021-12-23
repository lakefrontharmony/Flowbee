import streamlit as st
import pandas as pd
import json

def app():
	st.title('Instructions')
	st.header('Input Format Guidelines')
	st.write("""
	- Save file in UTF-8 CSV format
	- Have one column for each phase in your Kanban flow
	- Make the first row a header to name your columns
	- Each phase column should contain only dates or blanks (for when an item has not yet reached that phase)
	- Dates should be in YYYY-MM-DD format since they will be sorted for some functions
	- To represent cancelled items:
	1. Stop recording dates at the last phase where it reached
	2. Include a column with header, "Cancelled" and enter "Yes" for each item which is cancelled
	3. These will be excluded from calculations in this Script
	- Columns after phase columns can be included if you would like to do grouping in Flow Metric calculations
	""")

	st.header('Sprint Data Guidelines')
	st.write("""
	- One row for each Sprint
	- Each row should have the Sprint name, Start Date, and End Date as columns
	- Dates should be in YYYY-MM-DD format since they will be sorted for display
	""")
