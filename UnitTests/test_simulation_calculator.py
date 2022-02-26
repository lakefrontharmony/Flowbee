import pytest
import pandas as pd
from datetime import datetime, date
from SimulationCalcClass import SimulationCalcClass
import Globals


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
def simulator_input_df():
	return pd.DataFrame([['A1', 'TestA1', 'Parent1', '2021-11-01', '2021-11-10', '2021-12-01', 'Yes', 'Strategic'],
						 ['A2', 'TestA2', 'Parent1', '2021-10-01', '2021-10-02', '2021-11-01', '', 'Strategic'],
						 ['A3', 'TestA3', 'Parent1', '2020-01-01', '2020-01-15', '2020-02-15', '', 'Maintenance'],
						 ['B1', 'TestB1', 'Parent2', '2021-12-01', '2021-12-15', '2021-12-20', '', 'Maintenance'],
						 ['C3', 'TestC3', 'Parent3', '2021-01-01', '2021-05-01', '2022-01-05', '', 'Strategic'],
						 ['C4', 'TestC4', 'Parent3', '', '', '', '', 'Strategic'],
						 ['Z5', 'TestZ5', 'Parent4', '2021-08-08', '2021-10-06', '2022-01-10', '', 'Enabler'],
						 ['Z6', 'TestZ6', 'Parent4', '2021-11-02', '2021-12-02', '2022-02-10', '', 'Maintenance'],
						 ['Z7', 'TestZ7', 'Parent4', '2022-01-01', '2022-01-03', '', '', 'Strategic']],
						 columns=['ID', 'Name', 'Parent', 'Ready', 'InProgress', 'Done', 'Cancelled', 'Type'])


# This is the dataframe after prep_dataframe_formatting
@pytest.fixture()
def simulator_prepped_df():
	return pd.DataFrame([['A2', 'TestA2', 'Parent1', '2021-10-01', datetime(2021, 10, 2), datetime(2021, 11, 1), '', 'Strategic'],
						 ['A3', 'TestA3', 'Parent1', '2020-01-01', datetime(2020, 1, 15), datetime(2020, 2, 15), '', 'Maintenance'],
						 ['B1', 'TestB1', 'Parent2', '2021-12-01', datetime(2021, 12, 15), datetime(2021, 12, 20), '', 'Maintenance'],
						 ['C3', 'TestC3', 'Parent3', '2021-01-01', datetime(2021, 5, 1), datetime(2022, 1, 5), '', 'Strategic'],
						 ['Z5', 'TestZ5', 'Parent4', '2021-08-08', datetime(2021, 10, 6), datetime(2022, 1, 10), '', 'Enabler'],
						 ['Z6', 'TestZ6', 'Parent4', '2021-11-02', datetime(2021, 12, 2), datetime(2022, 2, 10), '', 'Maintenance']],
						 columns=['ID', 'Name', 'Parent', 'Ready', 'InProgress', 'Done', 'Cancelled', 'Type'])


# This is the dataframe after build_clean_dataframe
@pytest.fixture()
def simulator_clean_df():
	return pd.DataFrame([[datetime(2021, 10, 2), datetime(2021, 11, 1)],
						 [datetime(2021, 12, 15), datetime(2021, 12, 20)]],
						 columns=['InProgress', 'Done'])


# This is the build of the SimulationCalcClass
@pytest.fixture()
def input_simulator_builder():
	duration = 'Last Calendar Year'
	start_col = 'InProgress'
	end_col = 'Done'
	sim_start = '2022-01-19'
	sim_end = '2022-04-12'
	num_to_complete = 20
	curr_date = datetime(2022, 2, 15)
	return SimulationCalcClass(duration, start_col, end_col, sim_start, sim_end, num_to_complete, curr_date)


###################################
# UNIT TESTS
###################################
# Removed cancelled rows and those with null values in start/end columns
def test_prep_dataframe_formatting(input_simulator_builder, simulator_input_df, simulator_prepped_df, mocker):
	# setup
	mocker.patch('SimulationCalcClass.get_input_dataframe', return_value=simulator_input_df)
	# call function
	result = input_simulator_builder.prep_dataframe_formatting()
	# set expectation
	expected = simulator_prepped_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


# Removed cancelled rows and those with null values in start/end columns
def test_prep_dataframe_formatting_with_cancelled_tags(input_simulator_builder, simulator_input_df,
													   simulator_prepped_df, mocker):
	# setup
	simulator_input_df.loc[simulator_input_df['Cancelled'] == 'Yes'] = 'Cancelled'
	mocker.patch('SimulationCalcClass.get_input_dataframe', return_value=simulator_input_df)
	# call function
	result = input_simulator_builder.prep_dataframe_formatting()
	# set expectation
	expected = simulator_prepped_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


# Removed cancelled rows and those with null values in start/end columns
def test_prep_dataframe_formatting_with_resolution_column(input_simulator_builder, simulator_input_df,
													   simulator_prepped_df, mocker):
	# setup
	simulator_input_df.rename(columns={'Cancelled': 'Resolution'}, inplace=True)
	simulator_prepped_df.rename(columns={'Cancelled': 'Resolution'}, inplace=True)
	mocker.patch('SimulationCalcClass.get_input_dataframe', return_value=simulator_input_df)
	# call function
	result = input_simulator_builder.prep_dataframe_formatting()
	# set expectation
	expected = simulator_prepped_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


# Removed cancelled rows and those with null values in start/end columns
def test_prep_dataframe_formatting_with_resolution_and_cancelled_tags(input_simulator_builder, simulator_input_df,
													   simulator_prepped_df, mocker):
	# setup
	simulator_input_df.loc[simulator_input_df['Cancelled'] == 'Yes'] = 'Cancelled'
	simulator_input_df.rename(columns={'Cancelled': 'Resolution'}, inplace=True)
	simulator_prepped_df.rename(columns={'Cancelled': 'Resolution'}, inplace=True)
	mocker.patch('SimulationCalcClass.get_input_dataframe', return_value=simulator_input_df)
	# call function
	result = input_simulator_builder.prep_dataframe_formatting()
	# set expectation
	expected = simulator_prepped_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


# Establish start and end dates of historical range (uses Last Calendar Year with input_simulator_builder)
def test_determine_hist_date_range_for_previous_year(input_simulator_builder, simulator_prepped_df):
	# setup
	# call function
	input_simulator_builder.determine_hist_date_range(simulator_prepped_df)
	result_start_date = input_simulator_builder.start_date
	result_end_date = input_simulator_builder.end_date
	# set expectation
	expected_start_date = datetime(2021, 1, 1)
	expected_end_date = datetime(2021, 12, 31)
	# assertion
	assert result_start_date == expected_start_date
	assert result_end_date == expected_end_date


# Establish start and end dates of historical range (uses Last Calendar Year with input_simulator_builder)
def test_determine_hist_date_range_for_previous_year_truncated(input_simulator_builder, simulator_prepped_df):
	# setup
	# remove the row where the date was more than one year ago so that the start date will be truncated
	simulator_prepped_df = simulator_prepped_df.loc[simulator_prepped_df['ID'] != 'A3']
	# call function
	input_simulator_builder.determine_hist_date_range(simulator_prepped_df)
	result_start_date = input_simulator_builder.start_date
	result_end_date = input_simulator_builder.end_date
	# set expectation
	expected_start_date = datetime(2021, 11, 1)
	expected_end_date = datetime(2021, 12, 31)
	# assertion
	assert result_start_date == expected_start_date
	assert result_end_date == expected_end_date


# Establish start and end dates of historical range
def test_determine_hist_date_range_for_ytd(input_simulator_builder, simulator_prepped_df):
	# setup
	input_simulator_builder.duration = 'YTD'
	# call function
	input_simulator_builder.determine_hist_date_range(simulator_prepped_df)
	result_start_date = input_simulator_builder.start_date
	result_end_date = input_simulator_builder.end_date
	# set expectation
	expected_start_date = datetime(2022, 1, 1)
	expected_end_date = datetime(2022, 2, 15)
	# assertion
	assert result_start_date == expected_start_date
	assert result_end_date == expected_end_date


# Establish start and end dates of historical range
def test_determine_hist_date_for_12_months(input_simulator_builder, simulator_prepped_df):
	# setup
	input_simulator_builder.duration = 'Last 12 Months'
	# call function
	input_simulator_builder.determine_hist_date_range(simulator_prepped_df)
	result_start_date = input_simulator_builder.start_date
	result_end_date = input_simulator_builder.end_date
	# set expectation
	expected_start_date = datetime(2021, 2, 10)
	expected_end_date = datetime(2022, 2, 10)
	# assertion
	assert result_start_date == expected_start_date
	assert result_end_date == expected_end_date


# Establish start and end dates of historical range
def test_determine_hist_date_for_all(input_simulator_builder, simulator_prepped_df):
	# setup
	input_simulator_builder.duration = 'All'
	# call function
	input_simulator_builder.determine_hist_date_range(simulator_prepped_df)
	result_start_date = input_simulator_builder.start_date
	result_end_date = input_simulator_builder.end_date
	# set expectation
	expected_start_date = datetime(2020, 2, 15)
	expected_end_date = datetime(2022, 2, 10)
	# assertion
	assert result_start_date == expected_start_date
	assert result_end_date == expected_end_date


# Establish start and end dates of historical range
def test_determine_hist_date_error(input_simulator_builder, simulator_prepped_df):
	# setup
	input_simulator_builder.duration = 'XXX'

	# call function
	input_simulator_builder.determine_hist_date_range(simulator_prepped_df)
	result_start_date = input_simulator_builder.start_date
	result_end_date = input_simulator_builder.end_date
	result_prep_going_good = input_simulator_builder.prep_going_good
	result_error_msg = input_simulator_builder.get_error_msgs()

	# set expectation
	expected_start_date = datetime(2022, 2, 15)
	expected_end_date = datetime(2022, 2, 15)
	expected_prep_going_good = False
	expected_error_msg = False
	if result_error_msg.count('Unexpected duration of simulation received') > 0:
		expected_error_msg = True

	# assertion
	assert result_start_date == expected_start_date
	assert result_end_date == expected_end_date
	assert result_prep_going_good == expected_prep_going_good
	assert expected_error_msg is True


# Removed cancelled rows and those with null values in start/end columns
def test_building_clean_dataframe(input_simulator_builder, simulator_prepped_df, simulator_clean_df):
	# setup
	input_simulator_builder.start_date = datetime(2021, 1, 1)
	input_simulator_builder.end_date = datetime(2021, 12, 31)
	# call function
	result = input_simulator_builder.build_clean_dataframe(simulator_prepped_df)
	# set expectation
	expected = simulator_clean_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None
