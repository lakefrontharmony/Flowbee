import pytest
import pandas as pd
from datetime import datetime, date
from SimulationCalcClass import SimulationCalcClass


# To run unit tests:
# 1. Navigate to UnitTests folder in terminal
# 2. execute "coverage run -m pytest" to run all "test_*" files in folder
# 3. execute "coverage report -m" to get a coverage report from that run
# 4. execute "coverage html" to get a browser file of the changes that were tested.
###################################
# FIXTURES
###################################
# This is the dataframe that mimics an input file (with column names already stripped of spaces)
@pytest.fixture()
def chart_input_df():
	return pd.DataFrame([['A1', 'TestA1', 'Parent1', '2021-11-01', '2021-11-10', '2021-12-01', 'Yes', 'Strategic'],
						 ['A2', 'TestA2', 'Parent1', '2021-10-01', '2021-10-02', '2021-11-01', '', 'Strategic'],
						 ['B1', 'TestB1', 'Parent2', '2021-12-01', '2021-12-15', '2021-12-20', '', 'Maintenance'],
						 ['C3', 'TestC3', 'Parent3', '2021-01-01', '2021-05-01', '2022-01-05', '', 'Strategic'],
						 ['C4', 'TestC4', 'Parent3', '', '', '', '', 'Strategic'],
						 ['Z5', 'TestZ5', 'Parent4', '2021-08-08', '2021-10-06', '2022-01-10', '', 'Enabler'],
						 ['Z6', 'TestZ6', 'Parent4', '2021-11-02', '2021-12-02', '2022-02-10', '', 'Maintenance'],
						 ['Z7', 'TestZ7', 'Parent4', '2022-01-01', '2022-01-03', '', '', 'Strategic']],
						 columns=['ID', 'Name', 'Parent', 'Ready', 'InProgress', 'Done', 'Cancelled', 'Type'])


# This is the build of the SimulationCalcClass
@pytest.fixture()
def input_chart_builder():
	start_col = 'InProgress'
	end_col = 'Done'
	item_names = 'Name'
	start_date_toggle = True
	start_date = '2022-01-09'
	end_date = date(2022, 2, 20)
	wip_limit = 4
	return SimulationCalcClass(start_col, end_col, item_names, start_date_toggle, start_date, end_date)
###################################
# UNIT TESTS
###################################
