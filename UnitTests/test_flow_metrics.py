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
@pytest.fixture()
def flow_df():
	return pd.DataFrame([['A1', 'TestA1', 'Parent1', '2021-11-01', '2021-11-10', '2021-12-01', 'Yes', 'Strategic'],
						 ['A2', 'TestA2', 'Parent1', '2021-10-01', '2021-10-02', '2021-11-01', '', 'Strategic'],
						 ['B1', 'TestB1', 'Parent2', '2021-12-01', '2021-12-15', '2021-12-20', '', 'Maintenance'],
						 ['C3', 'TestC3', 'Parent3', '2021-01-01', '2021-05-01', '2022-01-05', '', 'Strategic'],
						 ['Z5', 'TestZ5', 'Parent4', '2021-08-08', '2021-10-06', '2022-01-10', '', 'Enabler'],
						 ['Z7', 'TestZ7', 'Parent4', '2022-01-01', '2022-01-05', '', '', 'Strategic']],
						 columns=['ID', 'Name', 'Parent', 'Ready', 'InProgress', 'Done', 'Cancelled', 'Type'])


@pytest.fixture()
def flow_no_cancelled_df():
	return pd.DataFrame([['A2', 'TestA2', 'Parent1', '2021-10-01', '2021-10-02', '2021-11-01', '', 'Strategic'],
						 ['B1', 'TestB1', 'Parent2', '2021-12-01', '2021-12-15', '2021-12-20', '', 'Maintenance'],
						 ['C3', 'TestC3', 'Parent3', '2021-01-01', '2021-05-01', '2022-01-05', '', 'Strategic'],
						 ['Z5', 'TestZ5', 'Parent4', '2021-08-08', '2021-10-06', '2022-01-10', '', 'Enabler'],
						 ['Z7', 'TestZ7', 'Parent4', '2022-01-01', '2022-01-05', '', '', 'Strategic']],
						 columns=['ID', 'Name', 'Parent', 'Ready', 'InProgress', 'Done', 'Cancelled', 'Type'])


@pytest.fixture()
def flow_completed_df():
	return pd.DataFrame([['A2', 'TestA2', 'Parent1', '2021-10-01', '2021-10-02', '2021-11-01', '', 'Strategic'],
						 ['B1', 'TestB1', 'Parent2', '2021-12-01', '2021-12-15', '2021-12-20', '', 'Maintenance'],
						 ['C3', 'TestC3', 'Parent3', '2021-01-01', '2021-05-01', '2022-01-05', '', 'Strategic'],
						 ['Z5', 'TestZ5', 'Parent4', '2021-08-08', '2021-10-06', '2022-01-10', '', 'Enabler']],
						 columns=['ID', 'Name', 'Parent', 'Ready', 'InProgress', 'Done', 'Cancelled', 'Type'])


@pytest.fixture()
def flow_completed_saved_items_df():
	return pd.DataFrame([['TestA2', '2021-10-02', '2021-11-01'],
						 ['TestB1', '2021-12-15', '2021-12-20'],
						 ['TestC3', '2021-05-01', '2022-01-05'],
						 ['TestZ5', '2021-10-06', '2022-01-10']],
						 columns=['Name', 'InProgress', 'Done'])


@pytest.fixture()
def sprint_df():
	return pd.DataFrame([['1.1', datetime(2022, 1, 3), datetime(2022, 1, 16)],
						 ['1.2', datetime(2022, 1, 17), datetime(2022, 1, 30)],
						 ['1.3', datetime(2022, 1, 31), datetime(2022, 2, 13)],
						 ['1.4', datetime(2022, 2, 14), datetime(2022, 2, 27)],
						 ['1.5', datetime(2022, 2, 28), datetime(2022, 3, 13)]],
						 columns=['SprintName', 'StartDate', 'EndDate'])


@pytest.fixture()
def input_flow_calculator(sprint_df):
	start_col = 'InProgress'
	end_col = 'Done'
	start_sprint = '1.1'
	end_sprint = '1.2'
	wip_limit = '10'
	item_names = 'Name'
	categories = 'Type'
	parent_toggle = False
	parent_column = 'Parent'
	return FlowCalcClass(start_col, end_col, start_sprint, end_sprint, wip_limit, item_names, categories,
						 parent_toggle, parent_column)


###################################
# UNIT TESTS
###################################
def test_remove_cancelled_rows(input_flow_calculator, flow_df, flow_no_cancelled_df):
	# setup
	# call function
	result = input_flow_calculator.removed_cancelled_rows(flow_df)
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
	test_calculator = input_flow_calculator
	# call function
	result = test_calculator.find_matching_sprint_date(sprint_df, '1.2', 'StartDate')
	# set expectation
	expected = datetime(2022, 1, 17)
	# assertion
	assert result == expected


def test_build_end_date(input_flow_calculator, sprint_df):
	# setup
	test_calculator = input_flow_calculator
	# call function
	result = test_calculator.find_matching_sprint_date(sprint_df, '1.2', 'EndDate')
	# set expectation
	expected = datetime(2022, 1, 30)
	# assertion
	assert result == expected


# def test_build_wip_df(input_flow_calculator):
# 	pass


# def test_build_dates_dataframe(input_flow_calculator):
# 	pass


# def test_build_throughput_run_dataframe(input_flow_calculator):
# 	pass

# def test_prep_categories(input_flow_calculator):
# 	pass


# def test_final_values_preparation(input_flow_calculator):
# 	pass


def test_prep_functions(input_flow_calculator, sprint_df, flow_df, mocker):
	# setup
	test_calculator = input_flow_calculator
	mocker.patch('FlowCalcClass.get_sprint_dataframe', return_value=sprint_df)
	mocker.patch('FlowCalcClass.get_flow_dataframe', return_value=flow_df)
	test_calculator.prep_for_metrics()
	# call function
	result = test_calculator.errors_were_found()
	# set expectation
	expected = False
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