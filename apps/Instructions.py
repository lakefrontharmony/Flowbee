import streamlit as st
from PIL import Image


def app():
	st.sidebar.header('Select an option from the Navigation dropdown to get started')
	st.sidebar.subheader('Templates for Download:')
	with open('Files/Flow_template.csv') as file:
		st.sidebar.download_button('Download Flow CSV', file, file_name='Flow.csv', mime='text/csv')
	with open('Files/SprintData_template.csv') as file:
		st.sidebar.download_button('Download Sprint Data CSV', file, file_name='SprintData.csv', mime='text/csv')

	flowbee_pic = Image.open('Files/Flowbee-box.jpeg')
	st.image(flowbee_pic, caption='The original Flowbee')

	st.title('Instructions')
	st.write("""
	1. Select an option from the Navigation dropdown above. \n
	2. Upload the applicable files through the left-sidebar 
	(each page will tell you what files it needs). \n
	3. Fill out any necessary form and the results will display in the main screen. \n
	This was designed to be very simple and let you get the context you need from the data.
	""")
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
