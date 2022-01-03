import streamlit as st
import pandas as pd
import json
from PIL import Image


def app():
	flowbee_pic = Image.open('Files/Flowbee-box.jpeg')
	st.image(flowbee_pic, caption='The original Flowbee')
	st.title('Instructions')
	st.header('Will these metrics be applicable to me?')
	st.write("""
	Short answer: Yes. \n
	All of these metrics are based on the flow through a system and adhering to Little's Law.
	As long as you are in a system where you can improve your processes towards a few basic principles,
	these numbers and visuals will help you be more predictable.
	Even if you are struggling with your processes, the charts and flow metrics can help you visualize your process
	and see where you have room for improvements.
	
	Little's Law:
	Average Cycle Time = Average Work In Progress / Average Throughput
	* NOTE: This is one variation of Little's Law that helps us with predictability.
	
	Assumptions which make Little's Law applicable to your process \n
	1. The average input or Arrival Rate should be equal the average Throughput (Departure Rate). \n
	2. All work that is started will eventually be completed and exit the system. \n
	3. The amount of WIP should be roughly the same at the beginning 
	and at the end of the time interval chosen for the calculation. \n
	4. The average age of the WIP is neither increasing nor decreasing. \n
	5. Cycle Time, WIP, and Throughput must all be measured using consistent units. \n
	
	Even if these assumptions do not hold for the entire time period under consideration, this can still be used as
	an estimation. The "goodness" of the estimate depends on how badly the assumptions have been violated.
	
	* NOTE: Little's Law is not forecasting. For forecasting, please use the "Monte Carlo" option in this app.
	""")

	st.header('Date File Format Guidelines')
	st.write("""
	- Save file in UTF-8 CSV format
	- Have one column for each phase in your Kanban flow
	- Make the first row a header to name your columns
	- Each phase column should contain only dates or blanks (for when an item has not yet reached that phase)
	- Dates should be in YYYY-MM-DD format since they will be sorted for some functions
	- To represent cancelled items:
	1. Stop recording dates at the last phase where it reached
	2. Include a column with header, "Cancelled" and enter "Yes" for each item which is cancelled
	3. These will be excluded from many calculations in this script
	- Additional columns (other than the  phase columns) can be included if you would like to do grouping in Flow Metric calculations
	""")

	st.header('Sprint Data File Format Guidelines')
	st.write("""
	- One row for each Sprint
	- Each row should have the Sprint name, Start Date, and End Date as columns
	- Dates should be in YYYY-MM-DD format since they will be sorted for display
	""")
