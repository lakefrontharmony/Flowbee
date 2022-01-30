import pytest
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
# This is the dataframe that mimics an input file (with column names already stripped of spaces)
@pytest.fixture()
def flow_input_df():
	return pd.DataFrame([['A1', 'TestA1', 'Parent1', '2021-11-01', '2021-11-10', '2021-12-01', 'Yes', 'Strategic'],
						 ['A2', 'TestA2', 'Parent1', '2021-10-01', '2021-10-02', '2021-11-01', '', 'Strategic'],
						 ['B1', 'TestB1', 'Parent2', '2021-12-01', '2021-12-15', '2021-12-20', '', 'Maintenance'],
						 ['C3', 'TestC3', 'Parent3', '2021-01-01', '2021-05-01', '2022-01-05', '', 'Strategic'],
						 ['Z5', 'TestZ5', 'Parent4', '2021-08-08', '2021-10-06', '2022-01-10', '', 'Enabler'],
						 ['Z7', 'TestZ7', 'Parent4', '2022-01-01', '2022-01-03', '', '', 'Strategic']],
						 columns=['ID', 'Name', 'Parent', 'Ready', 'InProgress', 'Done', 'Cancelled', 'Type'])


# This is the dataframe after removing cancelled items
@pytest.fixture()
def flow_no_cancelled_df():
	return pd.DataFrame([['A2', 'TestA2', 'Parent1', '2021-10-01', '2021-10-02', '2021-11-01', '', 'Strategic'],
						 ['B1', 'TestB1', 'Parent2', '2021-12-01', '2021-12-15', '2021-12-20', '', 'Maintenance'],
						 ['C3', 'TestC3', 'Parent3', '2021-01-01', '2021-05-01', '2022-01-05', '', 'Strategic'],
						 ['Z5', 'TestZ5', 'Parent4', '2021-08-08', '2021-10-06', '2022-01-10', '', 'Enabler'],
						 ['Z7', 'TestZ7', 'Parent4', '2022-01-01', '2022-01-03', '', '', 'Strategic']],
						 columns=['ID', 'Name', 'Parent', 'Ready', 'InProgress', 'Done', 'Cancelled', 'Type'])


# This is the dataframe that is being sent in to the function to save off completed items.
@pytest.fixture()
def flow_completed_df():
	return pd.DataFrame([['A2', 'TestA2', 'Parent1', '2021-10-01', '2021-10-02', '2021-11-01', '', 'Strategic'],
						 ['B1', 'TestB1', 'Parent2', '2021-12-01', '2021-12-15', '2021-12-20', '', 'Maintenance'],
						 ['C3', 'TestC3', 'Parent3', '2021-01-01', '2021-05-01', '2022-01-05', '', 'Strategic'],
						 ['Z5', 'TestZ5', 'Parent4', '2021-08-08', '2021-10-06', '2022-01-10', '', 'Enabler']],
						 columns=['ID', 'Name', 'Parent', 'Ready', 'InProgress', 'Done', 'Cancelled', 'Type'])


# This is the dataframe that is saved off to display completed items.
@pytest.fixture()
def flow_completed_saved_items_df():
	return pd.DataFrame([['TestA2', '2021-10-02', '2021-11-01'],
						 ['TestB1', '2021-12-15', '2021-12-20'],
						 ['TestC3', '2021-05-01', '2022-01-05'],
						 ['TestZ5', '2021-10-06', '2022-01-10']],
						 columns=['Name', 'InProgress', 'Done'])


# This is the dataframe coming out of the "build_clean_df" function
@pytest.fixture()
def flow_clean_df():
	return pd.DataFrame([[datetime(2021, 5, 1), datetime(2022, 1, 5), 'Strategic'],
						 [datetime(2021, 10, 6), datetime(2022, 1, 10), 'Enabler']],
						 columns=['InProgress', 'Done', 'Type'])


# This is the dataframe that mimics the sprint input csv file
@pytest.fixture()
def sprint_df():
	return pd.DataFrame([['1.1', datetime(2022, 1, 3), datetime(2022, 1, 16)],
						 ['1.2', datetime(2022, 1, 17), datetime(2022, 1, 30)],
						 ['1.3', datetime(2022, 1, 31), datetime(2022, 2, 13)],
						 ['1.4', datetime(2022, 2, 14), datetime(2022, 2, 27)],
						 ['1.5', datetime(2022, 2, 28), datetime(2022, 3, 13)]],
						 columns=['SprintName', 'StartDate', 'EndDate'])


# This is the dataframe that represents the WIP dataframe as of 2022-01-03
@pytest.fixture()
def wip_df():
	return pd.DataFrame([[datetime(2021, 5, 1), datetime(2022, 1, 5), 'Strategic'],
						 [datetime(2021, 10, 6), datetime(2022, 1, 10), 'Enabler'],
						 [datetime(2022, 1, 3), pd.NaT, 'Strategic']],
						 columns=['InProgress', 'Done', 'Type'])


# This is the dataframe that represents a range of 2022-01-01 to 2022-01-05.
@pytest.fixture()
def dates_df():
	return pd.DataFrame([[datetime(2022, 1, 1), 0],
							 [datetime(2022, 1, 2), 0],
							 [datetime(2022, 1, 3), 0],
							 [datetime(2022, 1, 4), 0],
							 [datetime(2022, 1, 5), 0]],
						 columns=['Date', 'WIP'])


# This is the dataframe that represents a range of 2022-01-01 to 2022-01-05 with WIP for each date filled in.
@pytest.fixture()
def final_dates_df():
	return pd.DataFrame([[datetime(2022, 1, 1), 4],
						 [datetime(2022, 1, 2), 4],
						 [datetime(2022, 1, 3), 5],
						 [datetime(2022, 1, 4), 5],
						 [datetime(2022, 1, 5), 4]],
						columns=['Date', 'WIP'])


# This is the build of the FlowCalcClass
@pytest.fixture()
def input_flow_calculator(sprint_df):
	start_col = 'InProgress'
	end_col = 'Done'
	start_sprint = '1.1'
	end_sprint = '1.2'
	wip_limit = 4
	item_names = 'Name'
	categories = 'Type'
	parent_toggle = False
	parent_column = 'Parent'
	return FlowCalcClass(start_col, end_col, start_sprint, end_sprint, wip_limit, item_names, categories,
						 parent_toggle, parent_column)


###################################
# UNIT TESTS
###################################
def test_remove_cancelled_rows(input_flow_calculator, flow_input_df, flow_no_cancelled_df):
	# setup
	# call function
	result = input_flow_calculator.remove_cancelled_rows(flow_input_df)
	# set expectation
	expected = flow_no_cancelled_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


def test_save_completed_items_df(input_flow_calculator, flow_completed_df, flow_completed_saved_items_df):
	# setup
	# call function
	result = input_flow_calculator.save_clean_completed_items_df(flow_completed_df)
	# set expectation
	expected = flow_completed_saved_items_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


def test_build_start_date(input_flow_calculator, sprint_df):
	# setup
	sprint_name = '1.2'
	column_name = 'StartDate'
	# call function
	result = input_flow_calculator.find_matching_sprint_date(sprint_df, sprint_name, column_name)
	# set expectation
	expected = datetime(2022, 1, 17)
	# assertion
	assert result == expected


def test_build_end_date(input_flow_calculator, sprint_df):
	# setup
	sprint_name = '1.2'
	column_name = 'EndDate'
	# call function
	result = input_flow_calculator.find_matching_sprint_date(sprint_df, sprint_name, column_name)
	# set expectation
	expected = datetime(2022, 1, 30)
	# assertion
	assert result == expected


def test_cannot_find_end_date(input_flow_calculator, sprint_df):
	# setup
	sprint_name = '0.0'
	column_name = 'EndDate'
	# call function
	result = input_flow_calculator.find_matching_sprint_date(sprint_df, sprint_name, column_name)
	# set expectation
	expected = None
	# assertion
	assert result == expected


def test_build_wip_df(input_flow_calculator, flow_input_df, wip_df):
	# setup
	test_date = datetime(2022, 1, 3)
	# call function
	result = input_flow_calculator.build_wip_dataframe(flow_input_df, test_date)
	# set expectation
	expected = wip_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


def test_build_dates_dataframe(input_flow_calculator, dates_df):
	# setup
	start_date = datetime(2022, 1, 1)
	end_date = datetime(2022, 1, 5)
	# call function
	result = input_flow_calculator.build_dates_dataframe(start_date, end_date)
	# set expectation
	expected = dates_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


# def test_build_throughput_run_dataframe(input_flow_calculator):
# 	pass

# def test_prep_categories(input_flow_calculator):
# 	pass


# def test_final_values_preparation(input_flow_calculator):
# 	pass


def test_prep_functions(input_flow_calculator, sprint_df, flow_input_df, mocker):
	# setup
	test_calculator = input_flow_calculator
	mocker.patch('FlowCalcClass.get_sprint_dataframe', return_value=sprint_df)
	mocker.patch('FlowCalcClass.get_flow_dataframe', return_value=flow_input_df)
	test_calculator.prep_for_metrics()
	# call function
	result = test_calculator.prep_errors_were_found()
	# set expectation
	expected = False
	# assertion
	assert result == expected


def test_calculate_average_throughput(input_flow_calculator):
	# setup
	num_finished_items = 3
	num_days = 30
	# call function
	result = input_flow_calculator.calculate_average_throughput(num_finished_items, num_days)
	# set expectation
	expected = 0.70
	# assertion
	assert result == expected


def test_calculate_average_wip(input_flow_calculator, dates_df, flow_clean_df, wip_df):
	# setup
	# call function
	result = input_flow_calculator.calculate_average_wip(dates_df, flow_clean_df, wip_df)
	# set expectation
	expected = 4.4
	# assertion
	assert result == expected


def test_calculate_wip_violations(input_flow_calculator, final_dates_df):
	# setup
	# call function
	result = input_flow_calculator.calculate_wip_violations(final_dates_df)
	# set expectation
	expected = 2
	# assertion
	assert result == expected


def test_calculate_average_lead_time(input_flow_calculator, flow_clean_df):
	# setup
	num_of_finished_items = len(flow_clean_df)
	# call function
	result = input_flow_calculator.calculate_average_lead_time(flow_clean_df, num_of_finished_items)
	# set expectation
	expected = 172.5
	# assertion
	assert result == expected


"""
# Keeping this just so I remember how to snag from capsys if I need to see a print output
def test_capsys_output(capsys):
	print('testing an output')
	captured = capsys.readouterr()
	assert captured.out == 'testing an output'
	asser captured.err == ''
"""