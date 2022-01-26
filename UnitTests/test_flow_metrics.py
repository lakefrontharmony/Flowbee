import pytest
from pytest_mock import mocker
import pandas as pd
from datetime import datetime
from FlowCalcClass import FlowCalcClass


# To run unit tests:
# 1. Navigate to UnitTests folder in terminal
# 2. execute "coverage run -m pytest" to run all "test_*" files in folder
# 3. execute "coverage report -m" to get a coverage report from that run
# 4. execute "coverage html" to get a browser file of the changes that were tested.
###################################
# FIXTURES
###################################
@pytest.fixture()
def flow_dataframe():
	return pd.DataFrame([['A1', 'TestA1', 'Parent1', '2021-11-01', '2021-11-10', '2021-12-01', 'Strategic'],
						 ['A2', 'TestA2', 'Parent1', '2021-10-01', '2021-10-02', '2021-11-01', 'Strategic'],
						 ['B1', 'TestB1', 'Parent2', '2021-12-01', '2021-12-15', '2021-12-20', 'Maintenance'],
						 ['C3', 'TestC3', 'Parent3', '2021-01-01', '2021-05-01', '2021-06-01', 'Strategic'],
						 ['Z5', 'TestZ5', 'Parent4', '2021-08-08', '2021-10-06', '2021-12-01', 'Enabler']],
						 columns=['ID', 'Name', 'Parent', 'Ready', 'In Progress', 'Done', 'Type'])


@pytest.fixture()
def sprint_dataframe():
	return pd.DataFrame([['1.1', datetime(2022, 1, 3), datetime(2022, 1, 16)],
						 ['1.2', datetime(2022, 1, 17), datetime(2022, 1, 30)],
						 ['1.3', datetime(2022, 1, 31), datetime(2022, 2, 13)],
						 ['1.4', datetime(2022, 2, 14), datetime(2022, 2, 27)],
						 ['1.5', datetime(2022, 2, 28), datetime(2022, 3, 13)]],
						 columns=['SprintName', 'StartDate', 'EndDate'])


@pytest.fixture()
def input_flow_calculator():
	start_col = 'InProgress'
	end_col = 'Done'
	start_sprint = '1.1'
	end_sprint = '1.2'
	wip_limit = '10'
	item_names = ''
	categories = 'Type'
	parent_toggle = False
	parent_column = 'Parent'
	return FlowCalcClass(start_col, end_col, start_sprint, end_sprint, wip_limit, item_names, categories,
						 parent_toggle, parent_column)


###################################
# UNIT TESTS
###################################
def test_open_and_create_dataframe(input_flow_calculator, sprint_dataframe):
	# setup
	# will this fail by trying to create the calculator before patching the global variable?
	mocker.patch.object(input_flow_calculator.Globals.SPRINT_INFO_DATAFRAME, sprint_dataframe)
	# call function
	# set expectation
	# assertion
	return


"""
# Keeping this just so I remember how to snag from capsys if I need to see a print output
def test_capsys_output(capsys):
	print('testing an output')
	captured = capsys.readouterr()
	assert captured.out == 'testing an output'
	asser captured.err == ''
"""