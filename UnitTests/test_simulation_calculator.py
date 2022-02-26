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
						 ['A4', 'TestA4', 'Parent1', '2022-01-05', '2022-01-10', '2022-01-30', 'Cancelled', 'Strategic'],
						 ['B1', 'TestB1', 'Parent2', '2021-12-01', '2021-12-15', '2021-12-20', '', 'Maintenance'],
						 ['C3', 'TestC3', 'Parent3', '2021-01-01', '2021-05-01', '2021-12-05', '', 'Strategic'],
						 ['C4', 'TestC4', 'Parent3', '', '', '', '', 'Strategic'],
						 ['D1', 'TestD1', 'Parent4', '2021-11-15', '2021-11-16', '2022-01-20', '', 'Strategic'],
						 ['D2', 'TestD2', 'Parent4', '2022-01-01', '2022-01-01', '2022-01-20', '', 'Strategic'],
						 ['D3', 'TestD4', 'Parent4', '2022-01-20', '2022-01-21', '2022-02-01', '', 'Strategic'],
						 ['D4', 'TestD4', 'Parent4', '2022-02-01', '2022-02-03', '2022-02-05', '', 'Strategic'],
						 ['D5', 'TestD5', 'Parent4', '2022-02-01', '2022-02-02', '2022-03-01', '', 'Strategic'],
						 ['Z5', 'TestZ5', 'Parent9', '2021-08-08', '2021-10-06', '2022-01-10', '', 'Enabler'],
						 ['Z6', 'TestZ6', 'Parent9', '2021-11-02', '2021-12-02', '2022-02-10', '', 'Maintenance'],
						 ['Z7', 'TestZ7', 'Parent9', '2022-01-01', '2022-01-03', '', '', 'Strategic']],
						 columns=['ID', 'Name', 'Parent', 'Ready', 'InProgress', 'Done', 'Cancelled', 'Type'])


# This is the dataframe after prep_dataframe_formatting
@pytest.fixture()
def simulator_prepped_df():
	return pd.DataFrame([['A2', 'TestA2', 'Parent1', '2021-10-01', datetime(2021, 10, 2), datetime(2021, 11, 1), '', 'Strategic'],
						 ['A3', 'TestA3', 'Parent1', '2020-01-01', datetime(2020, 1, 15), datetime(2020, 2, 15), '', 'Maintenance'],
						 ['B1', 'TestB1', 'Parent2', '2021-12-01', datetime(2021, 12, 15), datetime(2021, 12, 20), '', 'Maintenance'],
						 ['C3', 'TestC3', 'Parent3', '2021-01-01', datetime(2021, 5, 1), datetime(2021, 12, 5), '', 'Strategic'],
						 ['D1', 'TestD1', 'Parent4', '2021-11-15', datetime(2021, 11, 16), datetime(2022, 1, 20), '', 'Strategic'],
						 ['D2', 'TestD2', 'Parent4', '2022-01-01', datetime(2022, 1, 1), datetime(2022, 1, 20), '', 'Strategic'],
						 ['D3', 'TestD4', 'Parent4', '2022-01-20', datetime(2022, 1, 21), datetime(2022, 2, 1), '', 'Strategic'],
						 ['D4', 'TestD4', 'Parent4', '2022-02-01', datetime(2022, 2, 3), datetime(2022, 2, 5), '', 'Strategic'],
						 ['D5', 'TestD5', 'Parent4', '2022-02-01', datetime(2022, 2, 2), datetime(2022, 3, 1), '', 'Strategic'],
						 ['Z5', 'TestZ5', 'Parent9', '2021-08-08', datetime(2021, 10, 6), datetime(2022, 1, 10), '', 'Enabler'],
						 ['Z6', 'TestZ6', 'Parent9', '2021-11-02', datetime(2021, 12, 2), datetime(2022, 2, 10), '', 'Maintenance']],
						 columns=['ID', 'Name', 'Parent', 'Ready', 'InProgress', 'Done', 'Cancelled', 'Type'])


# This is the dataframe after build_clean_dataframe
@pytest.fixture()
def simulator_clean_df():
	return pd.DataFrame([[datetime(2021, 11, 16), datetime(2022, 1, 20)],
						 [datetime(2022, 1, 1), datetime(2022, 1, 20)],
						 [datetime(2022, 1, 21), datetime(2022, 2, 1)],
						 [datetime(2022, 2, 3), datetime(2022, 2, 5)],
						 [datetime(2021, 12, 2), datetime(2022, 2, 10)]],
						 columns=['InProgress', 'Done'])


# This is the dataframe after build_dates_dataframe using "last month" option (30 days) (using end date of 2/15/2022)
@pytest.fixture()
def dates_df_one_month():
	return pd.DataFrame([[datetime(2022, 1, 16), 0],
						 [datetime(2022, 1, 17), 0],
						 [datetime(2022, 1, 18), 0],
						 [datetime(2022, 1, 19), 0],
						 [datetime(2022, 1, 20), 0],
						 [datetime(2022, 1, 21), 0],
						 [datetime(2022, 1, 22), 0],
						 [datetime(2022, 1, 23), 0],
						 [datetime(2022, 1, 24), 0],
						 [datetime(2022, 1, 25), 0],
						 [datetime(2022, 1, 26), 0],
						 [datetime(2022, 1, 27), 0],
						 [datetime(2022, 1, 28), 0],
						 [datetime(2022, 1, 29), 0],
						 [datetime(2022, 1, 30), 0],
						 [datetime(2022, 1, 31), 0],
						 [datetime(2022, 2, 1), 0],
						 [datetime(2022, 2, 2), 0],
						 [datetime(2022, 2, 3), 0],
						 [datetime(2022, 2, 4), 0],
						 [datetime(2022, 2, 5), 0],
						 [datetime(2022, 2, 6), 0],
						 [datetime(2022, 2, 7), 0],
						 [datetime(2022, 2, 8), 0],
						 [datetime(2022, 2, 9), 0],
						 [datetime(2022, 2, 10), 0],
						 [datetime(2022, 2, 11), 0],
						 [datetime(2022, 2, 12), 0],
						 [datetime(2022, 2, 13), 0],
						 [datetime(2022, 2, 14), 0],
						 [datetime(2022, 2, 15), 0]],
						 columns=['Date', 'Frequency'])


# This is the dataframe after build_dist_dataframe using "last month" option (30 days) (using end date of 2/15/2022)
@pytest.fixture()
def dist_df_one_month():
	return pd.DataFrame([[0.0, 0.8709677419354839],
						 [1.0, 0.0967741935483871],
						 [2.0, 0.03225806451612903]],
						 columns=['Count', 'Frequency'])


# This is the build of the SimulationCalcClass
@pytest.fixture()
def input_simulator_builder():
	duration = 'Last Month'
	start_col = 'InProgress'
	end_col = 'Done'
	sim_start = '2022-01-19'
	sim_end = '2022-04-12'
	num_to_complete = 20
	curr_date = datetime(2022, 2, 15)
	return SimulationCalcClass(duration, start_col, end_col, sim_start, sim_end, num_to_complete, curr_date)


# This is the build of the SimulationCalcClass when set to calculate current WIP
@pytest.fixture()
def input_simulator_builder_use_current_wip():
	duration = 'Last Month'
	start_col = 'InProgress'
	end_col = 'Done'
	sim_start = '2022-01-19'
	sim_end = '2022-04-12'
	# Setting this to zero makes it calculate the current number of items in progress
	num_to_complete = 0
	curr_date = datetime(2022, 2, 15)
	return SimulationCalcClass(duration, start_col, end_col, sim_start, sim_end, num_to_complete, curr_date)


###################################
# UNIT TESTS
###################################
# Removed cancelled rows and those with null values in start/end columns
def test_prep_dataframe_formatting(input_simulator_builder, simulator_input_df, simulator_prepped_df):
	# setup
	# call function
	result = input_simulator_builder.prep_dataframe_formatting(simulator_input_df)
	# set expectation
	expected = simulator_prepped_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


# Removed cancelled rows and those with null values in start/end columns
def test_prep_dataframe_formatting_with_cancelled_tags(input_simulator_builder, simulator_input_df,
													   simulator_prepped_df):
	# setup
	simulator_input_df.loc[simulator_input_df['Cancelled'] == 'Yes'] = 'Cancelled'
	# call function
	result = input_simulator_builder.prep_dataframe_formatting(simulator_input_df)
	# set expectation
	expected = simulator_prepped_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


# Removed cancelled rows and those with null values in start/end columns
def test_prep_dataframe_formatting_with_resolution_column(input_simulator_builder, simulator_input_df,
													   simulator_prepped_df):
	# setup
	simulator_input_df.rename(columns={'Cancelled': 'Resolution'}, inplace=True)
	simulator_prepped_df.rename(columns={'Cancelled': 'Resolution'}, inplace=True)
	# call function
	result = input_simulator_builder.prep_dataframe_formatting(simulator_input_df)
	# set expectation
	expected = simulator_prepped_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


# Removed cancelled rows and those with null values in start/end columns
def test_prep_dataframe_formatting_with_resolution_and_cancelled_tags(input_simulator_builder, simulator_input_df,
													   simulator_prepped_df):
	# setup
	simulator_input_df.loc[simulator_input_df['Cancelled'] == 'Yes'] = 'Cancelled'
	simulator_input_df.rename(columns={'Cancelled': 'Resolution'}, inplace=True)
	simulator_prepped_df.rename(columns={'Cancelled': 'Resolution'}, inplace=True)
	# call function
	result = input_simulator_builder.prep_dataframe_formatting(simulator_input_df)
	# set expectation
	expected = simulator_prepped_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


# Establish start and end dates of historical range
def test_determine_hist_date_range_for_previous_year(input_simulator_builder, simulator_prepped_df):
	# setup
	input_simulator_builder.duration = 'Last Calendar Year'
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


# Establish start and end dates of historical range
def test_determine_hist_date_range_for_previous_year_truncated(input_simulator_builder, simulator_prepped_df):
	# setup
	input_simulator_builder.duration = 'Last Calendar Year'
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
	expected_start_date = datetime(2021, 3, 1)
	expected_end_date = datetime(2022, 3, 1)
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
	expected_end_date = datetime(2022, 3, 1)
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
	# set these values since we are not running through other prep functions
	input_simulator_builder.start_date = datetime(2022, 1, 16)
	# call function
	result = input_simulator_builder.build_clean_dataframe(simulator_prepped_df)
	# set expectation
	expected = simulator_clean_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


# Build dates dataframe. Only use last 30 days so that the return df is manageable for this test.
def test_building_dates_df_for_30_days(input_simulator_builder, dates_df_one_month):
	# setup
	# set these values since we are not running through other prep functions
	input_simulator_builder.start_date = datetime(2022, 1, 16)
	input_simulator_builder.end_date = datetime(2022, 2, 15)
	# call function
	result = input_simulator_builder.build_dates_dataframe()
	# set expectation
	expected = dates_df_one_month
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


# Build distribution dataframe based on last 30 days option
def test_building_dist_df(input_simulator_builder, simulator_clean_df, dates_df_one_month, dist_df_one_month):
	# setup
	# set these values since we are not running through other prep functions
	input_simulator_builder.start_date = datetime(2022, 1, 16)
	input_simulator_builder.end_date = datetime(2022, 2, 15)
	# call function
	result = input_simulator_builder.build_dist_dataframe(simulator_clean_df, dates_df_one_month)
	# set expectation
	expected = dist_df_one_month
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


# test building final fields for calculations
def test_final_field_preparation(input_simulator_builder, simulator_clean_df, dates_df_one_month, dist_df_one_month):
	# setup
	# call function
	# set expectation
	# assertion
	pass


# Build distribution dataframe based on last 30 days option
def test_calculate_current_wip_entries(input_simulator_builder, simulator_input_df):
	# setup
	# set these values since we are not running through other prep functions
	input_simulator_builder.start_date = datetime(2022, 1, 16)
	input_simulator_builder.end_date = datetime(2022, 2, 15)
	# call function
	result = input_simulator_builder.calc_current_num_items_in_progress(simulator_input_df)
	# set expectation
	# This includes one that hasn't been finished, and one that has been finished, but in the 'future'
	expected = 2
	# assertion
	assert result == expected
