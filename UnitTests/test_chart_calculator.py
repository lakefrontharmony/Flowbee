import pytest
import pandas as pd
from datetime import datetime, date
from ChartBuilderClass import ChartBuilderClass
from unittest import mock


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


# This is the dataframe after removing cancelled items
@pytest.fixture()
def chart_no_cancelled_df():
	return pd.DataFrame([['A2', 'TestA2', 'Parent1', '2021-10-01', '2021-10-02', '2021-11-01', '', 'Strategic'],
						 ['B1', 'TestB1', 'Parent2', '2021-12-01', '2021-12-15', '2021-12-20', '', 'Maintenance'],
						 ['C3', 'TestC3', 'Parent3', '2021-01-01', '2021-05-01', '2022-01-05', '', 'Strategic'],
						 ['C4', 'TestC4', 'Parent3', '', '', '', '', 'Strategic'],
						 ['Z5', 'TestZ5', 'Parent4', '2021-08-08', '2021-10-06', '2022-01-10', '', 'Enabler'],
						 ['Z6', 'TestZ6', 'Parent4', '2021-11-02', '2021-12-02', '2022-02-10', '', 'Maintenance'],
						 ['Z7', 'TestZ7', 'Parent4', '2022-01-01', '2022-01-03', '', '', 'Strategic']],
						 columns=['ID', 'Name', 'Parent', 'Ready', 'InProgress', 'Done', 'Cancelled', 'Type'])


# This is the clean_df out of "build_clean_df" for the ChartBuilderClass
@pytest.fixture()
def chart_clean_df():
	return pd.DataFrame([['TestA2', date(2021, 10, 2), date(2021, 11, 1), 4],
						 ['TestB1', date(2021, 12, 15), date(2021, 12, 20), 4],
						 ['TestC3', date(2021, 5, 1), date(2022, 1, 5), 4],
						 ['TestZ5',date(2021, 10, 6), date(2022, 1, 10), 4],
						 ['TestZ6', date(2021, 12, 2), date(2022, 2, 10), 4],
						 ['TestZ7',date(2022, 1, 3), pd.NaT, 4]],
						 columns=['Name', '1_InProgress', '2_Done', 'WIPLimit'])


# This is the chart_clean_df filtered to a start date of 1/9/22 (out of filter_clean_df_to_start_date())
@pytest.fixture()
def chart_clean_filtered_to_start_date_df():
	return pd.DataFrame([['TestZ5', date(2021, 10, 6), date(2022, 1, 10), 4],
						 ['TestZ6', date(2021, 12, 2), date(2022, 2, 10), 4],
						 ['TestZ7', date(2022, 1, 3), pd.NaT, 4]],
						columns=['Name', '1_InProgress', '2_Done', 'WIPLimit'])


# saving all completed items from chart_clean_df
@pytest.fixture()
def flow_completed_saved_items_df():
	return pd.DataFrame([['TestZ5', date(2021, 10, 6), date(2022, 1, 10), 4],
						 ['TestZ6', date(2021, 12, 2), date(2022, 2, 10), 4]],
						columns=['Name', '1_InProgress', '2_Done', 'WIPLimit'])

# clean_df but start dates are changed to help build a smaller data set.
@pytest.fixture()
def flow_clean_alt_date_range_testing_df():
	return pd.DataFrame([[datetime(2022, 1, 8), datetime(2022, 1, 30), 'Enabler', 15.0],
						 [datetime(2022, 1, 18), datetime(2022, 1, 31), 'Strategic', 13.0],
						 [datetime(2022, 1, 26), datetime(2022, 2, 1), 'Strategic', 6.0]],
						columns=['InProgress', 'Done', 'Type', 'lead_time'])


# Uses range of 01/08/2022 to 02/20/2022 from flow_clean_alt_date_range_testing_df
@pytest.fixture()
def dates_not_filtered_df():
	return pd.DataFrame([[datetime(2022, 1, 8), 0, 0, 0],
						 [datetime(2022, 1, 9), 0, 0, 0],
						 [datetime(2022, 1, 10), 0, 0, 0],
						 [datetime(2022, 1, 11), 0, 0, 0],
						 [datetime(2022, 1, 12), 0, 0, 0],
						 [datetime(2022, 1, 13), 0, 0, 0],
						 [datetime(2022, 1, 14), 0, 0, 0],
						 [datetime(2022, 1, 15), 0, 0, 0],
						 [datetime(2022, 1, 16), 0, 0, 0],
						 [datetime(2022, 1, 17), 0, 0, 0],
						 [datetime(2022, 1, 18), 0, 0, 0],
						 [datetime(2022, 1, 19), 0, 0, 0],
						 [datetime(2022, 1, 20), 0, 0, 0],
						 [datetime(2022, 1, 21), 0, 0, 0],
						 [datetime(2022, 1, 22), 0, 0, 0],
						 [datetime(2022, 1, 23), 0, 0, 0],
						 [datetime(2022, 1, 24), 0, 0, 0],
						 [datetime(2022, 1, 25), 0, 0, 0],
						 [datetime(2022, 1, 26), 0, 0, 0],
						 [datetime(2022, 1, 27), 0, 0, 0],
						 [datetime(2022, 1, 28), 0, 0, 0],
						 [datetime(2022, 1, 29), 0, 0, 0],
						 [datetime(2022, 1, 30), 0, 0, 0],
						 [datetime(2022, 1, 31), 0, 0, 0],
						 [datetime(2022, 2, 1), 0, 0, 0],
						 [datetime(2022, 2, 2), 0, 0, 0],
						 [datetime(2022, 2, 3), 0, 0, 0],
						 [datetime(2022, 2, 4), 0, 0, 0],
						 [datetime(2022, 2, 5), 0, 0, 0],
						 [datetime(2022, 2, 6), 0, 0, 0],
						 [datetime(2022, 2, 7), 0, 0, 0],
						 [datetime(2022, 2, 8), 0, 0, 0],
						 [datetime(2022, 2, 9), 0, 0, 0],
						 [datetime(2022, 2, 10), 0, 0, 0],
						 [datetime(2022, 2, 11), 0, 0, 0],
						 [datetime(2022, 2, 12), 0, 0, 0],
						 [datetime(2022, 2, 13), 0, 0, 0],
						 [datetime(2022, 2, 14), 0, 0, 0],
						 [datetime(2022, 2, 15), 0, 0, 0],
						 [datetime(2022, 2, 16), 0, 0, 0],
						 [datetime(2022, 2, 17), 0, 0, 0],
						 [datetime(2022, 2, 18), 0, 0, 0],
						 [datetime(2022, 2, 19), 0, 0, 0],
						 [datetime(2022, 2, 20), 0, 0, 0]],
						columns=['Date', 'WIP', 'Throughput', 'Avg Cycle Time'])


# Uses range of 01/09/2022 to 02/20/2022
@pytest.fixture()
def dates_filtered_df():
	return pd.DataFrame([[datetime(2022, 1, 9), 0, 0, 0],
						 [datetime(2022, 1, 10), 0, 0, 0],
						 [datetime(2022, 1, 11), 0, 0, 0],
						 [datetime(2022, 1, 12), 0, 0, 0],
						 [datetime(2022, 1, 13), 0, 0, 0],
						 [datetime(2022, 1, 14), 0, 0, 0],
						 [datetime(2022, 1, 15), 0, 0, 0],
						 [datetime(2022, 1, 16), 0, 0, 0],
						 [datetime(2022, 1, 17), 0, 0, 0],
						 [datetime(2022, 1, 18), 0, 0, 0],
						 [datetime(2022, 1, 19), 0, 0, 0],
						 [datetime(2022, 1, 20), 0, 0, 0],
						 [datetime(2022, 1, 21), 0, 0, 0],
						 [datetime(2022, 1, 22), 0, 0, 0],
						 [datetime(2022, 1, 23), 0, 0, 0],
						 [datetime(2022, 1, 24), 0, 0, 0],
						 [datetime(2022, 1, 25), 0, 0, 0],
						 [datetime(2022, 1, 26), 0, 0, 0],
						 [datetime(2022, 1, 27), 0, 0, 0],
						 [datetime(2022, 1, 28), 0, 0, 0],
						 [datetime(2022, 1, 29), 0, 0, 0],
						 [datetime(2022, 1, 30), 0, 0, 0],
						 [datetime(2022, 1, 31), 0, 0, 0],
						 [datetime(2022, 2, 1), 0, 0, 0],
						 [datetime(2022, 2, 2), 0, 0, 0],
						 [datetime(2022, 2, 3), 0, 0, 0],
						 [datetime(2022, 2, 4), 0, 0, 0],
						 [datetime(2022, 2, 5), 0, 0, 0],
						 [datetime(2022, 2, 6), 0, 0, 0],
						 [datetime(2022, 2, 7), 0, 0, 0],
						 [datetime(2022, 2, 8), 0, 0, 0],
						 [datetime(2022, 2, 9), 0, 0, 0],
						 [datetime(2022, 2, 10), 0, 0, 0],
						 [datetime(2022, 2, 11), 0, 0, 0],
						 [datetime(2022, 2, 12), 0, 0, 0],
						 [datetime(2022, 2, 13), 0, 0, 0],
						 [datetime(2022, 2, 14), 0, 0, 0],
						 [datetime(2022, 2, 15), 0, 0, 0],
						 [datetime(2022, 2, 16), 0, 0, 0],
						 [datetime(2022, 2, 17), 0, 0, 0],
						 [datetime(2022, 2, 18), 0, 0, 0],
						 [datetime(2022, 2, 19), 0, 0, 0],
						 [datetime(2022, 2, 20), 0, 0, 0],],
						columns=['Date', 'WIP', 'Throughput', 'Avg Cycle Time'])


@pytest.fixture()
def date_col_names():
	return ['1_InProgress', '2_Done']


@pytest.fixture()
def cfd_df():
	return pd.DataFrame([[datetime(2022, 1, 9), 3, 0],
						 [datetime(2022, 1, 10), 3, 1],
						 [datetime(2022, 1, 11), 3, 1],
						 [datetime(2022, 1, 12), 3, 1],
						 [datetime(2022, 1, 13), 3, 1],
						 [datetime(2022, 1, 14), 3, 1],
						 [datetime(2022, 1, 15), 3, 1],
						 [datetime(2022, 1, 16), 3, 1],
						 [datetime(2022, 1, 17), 3, 1],
						 [datetime(2022, 1, 18), 3, 1],
						 [datetime(2022, 1, 19), 3, 1],
						 [datetime(2022, 1, 20), 3, 1],
						 [datetime(2022, 1, 21), 3, 1],
						 [datetime(2022, 1, 22), 3, 1],
						 [datetime(2022, 1, 23), 3, 1],
						 [datetime(2022, 1, 24), 3, 1],
						 [datetime(2022, 1, 25), 3, 1],
						 [datetime(2022, 1, 26), 3, 1],
						 [datetime(2022, 1, 27), 3, 1],
						 [datetime(2022, 1, 28), 3, 1],
						 [datetime(2022, 1, 29), 3, 1],
						 [datetime(2022, 1, 30), 3, 1],
						 [datetime(2022, 1, 31), 3, 1],
						 [datetime(2022, 2, 1), 3, 1],
						 [datetime(2022, 2, 2), 3, 1],
						 [datetime(2022, 2, 3), 3, 1],
						 [datetime(2022, 2, 4), 3, 1],
						 [datetime(2022, 2, 5), 3, 1],
						 [datetime(2022, 2, 6), 3, 1],
						 [datetime(2022, 2, 7), 3, 1],
						 [datetime(2022, 2, 8), 3, 1],
						 [datetime(2022, 2, 9), 3, 1],
						 [datetime(2022, 2, 10), 3, 2],
						 [datetime(2022, 2, 11), 3, 2],
						 [datetime(2022, 2, 12), 3, 2],
						 [datetime(2022, 2, 13), 3, 2],
						 [datetime(2022, 2, 14), 3, 2],
						 [datetime(2022, 2, 15), 3, 2],
						 [datetime(2022, 2, 16), 3, 2],
						 [datetime(2022, 2, 17), 3, 2],
						 [datetime(2022, 2, 18), 3, 2],
						 [datetime(2022, 2, 19), 3, 2],
						 [datetime(2022, 2, 20), 3, 2]],
						columns=['Date', '1_InProgress', '2_Done'])


@pytest.fixture()
def cfd_vectors_df():
	return pd.DataFrame([['1_InProgress', datetime(2022, 1, 9), 3],
						 ['1_InProgress', datetime(2022, 2, 20), 3],
						 ['2_Done', datetime(2022, 1, 10), 1],
						 ['2_Done', datetime(2022, 2, 20), 2]],
						columns=['Status', 'Date', 'Count'])


# assumes overriding the current date to 02/20/2022
@pytest.fixture()
def aging_wip_df():
	return pd.DataFrame([['TestZ5', 96, '2_Done', datetime(2021, 10, 6), datetime(2022, 1, 10), 96, 0,
						  92.1, 83.0, 83.0],
						 ['TestZ6', 70, '2_Done', date(2021, 12, 2), date(2022, 2, 10), 70, 0, 92.1, 83, 83],
						 ['TestZ7', 48, '1_InProgress', datetime(2022, 1, 3), pd.NaT, 48, 0,
						  92.1, 83.0, 83.0]],
						columns=['Name', 'Age', 'Status', 'Start_Date', 'Done_Date', '1_InProgress', '2_Done',
								 'CycleTime85', 'CycleTime50', 'CycleTimeAvg'])


# uses dates_filtered_df range of 01/09/2022 to 02/20/2022
@pytest.fixture()
def run_df():
	return pd.DataFrame([[datetime(2022, 1, 9), 3, 0, 4],
						 [datetime(2022, 1, 10), 2, 1, 4],
						 [datetime(2022, 1, 11), 2, 0, 4],
						 [datetime(2022, 1, 12), 2, 0, 4],
						 [datetime(2022, 1, 13), 2, 0, 4],
						 [datetime(2022, 1, 14), 2, 0, 4],
						 [datetime(2022, 1, 15), 2, 0, 4],
						 [datetime(2022, 1, 16), 2, 0, 4],
						 [datetime(2022, 1, 17), 2, 0, 4],
						 [datetime(2022, 1, 18), 2, 0, 4],
						 [datetime(2022, 1, 19), 2, 0, 4],
						 [datetime(2022, 1, 20), 2, 0, 4],
						 [datetime(2022, 1, 21), 2, 0, 4],
						 [datetime(2022, 1, 22), 2, 0, 4],
						 [datetime(2022, 1, 23), 2, 0, 4],
						 [datetime(2022, 1, 24), 2, 0, 4],
						 [datetime(2022, 1, 25), 2, 0, 4],
						 [datetime(2022, 1, 26), 2, 0, 4],
						 [datetime(2022, 1, 27), 2, 0, 4],
						 [datetime(2022, 1, 28), 2, 0, 4],
						 [datetime(2022, 1, 29), 2, 0, 4],
						 [datetime(2022, 1, 30), 2, 0, 4],
						 [datetime(2022, 1, 31), 2, 0, 4],
						 [datetime(2022, 2, 1), 2, 0, 4],
						 [datetime(2022, 2, 2), 2, 0, 4],
						 [datetime(2022, 2, 3), 2, 0, 4],
						 [datetime(2022, 2, 4), 2, 0, 4],
						 [datetime(2022, 2, 5), 2, 0, 4],
						 [datetime(2022, 2, 6), 2, 0, 4],
						 [datetime(2022, 2, 7), 2, 0, 4],
						 [datetime(2022, 2, 8), 2, 0, 4],
						 [datetime(2022, 2, 9), 2, 0, 4],
						 [datetime(2022, 2, 10), 1, 1, 4],
						 [datetime(2022, 2, 11), 1, 0, 4],
						 [datetime(2022, 2, 12), 1, 0, 4],
						 [datetime(2022, 2, 13), 1, 0, 4],
						 [datetime(2022, 2, 14), 1, 0, 4],
						 [datetime(2022, 2, 15), 1, 0, 4],
						 [datetime(2022, 2, 16), 1, 0, 4],
						 [datetime(2022, 2, 17), 1, 0, 4],
						 [datetime(2022, 2, 18), 1, 0, 4],
						 [datetime(2022, 2, 19), 1, 0, 4],
						 [datetime(2022, 2, 20), 1, 0, 4]],
						columns=['Date', 'WIP', 'Throughput', 'WIPLimit'])


# assumes overriding the current date to 02/20/2022
@pytest.fixture()
def throughput_hist_df():
	return pd.DataFrame([[0, 41, 1.0, 1.0, 0.05],
						 [1, 2, 1.0, 1.0, 0.05]],
						columns=['Throughput', 'Count', 'Throughput85', 'Throughput50', 'ThroughputAvg'])


@pytest.fixture()
def cycle_time_hist_df():
	return pd.DataFrame([[96, 1, 92.1, 83.0, 83.0],
						 [70, 1, 92.1, 83.0, 83.0]],
						columns=['Age', 'Count', 'CycleTime85', 'CycleTime50', 'CycleTimeAvg'])


@pytest.fixture()
def cycle_time_scatter_df():
	return pd.DataFrame([['TestZ5', 96, '2_Done', datetime(2021, 10, 6), datetime(2022, 1, 10), 96, 0,
						  92.1, 83.0, 83.0],
						 ['TestZ6', 70, '2_Done', datetime(2021, 12, 2), datetime(2022, 2, 10), 70, 0,
						  92.1, 83.0, 83.0]],
						columns=['Name', 'Age', 'Status', 'Start_Date', 'Done_Date', '1_InProgress', '2_Done',
								 'CycleTime85', 'CycleTime50', 'CycleTimeAvg'])


# This is the build of the ChartBuilderClass
@pytest.fixture()
def input_chart_builder():
	start_col = 'InProgress'
	end_col = 'Done'
	item_names = 'Name'
	start_date_toggle = True
	start_date = '2022-01-09'
	end_date = date(2022, 2, 20)
	wip_limit = 4
	return ChartBuilderClass(start_col, end_col, item_names, start_date_toggle, start_date, end_date, wip_limit)


###################################
# UNIT TESTS
###################################
# PREP FUNCTION TESTING
###################################
def test_build_clean_chart_df(input_chart_builder, chart_input_df, chart_clean_df):
	# setup
	# call function
	result = input_chart_builder.build_clean_df(chart_input_df)
	# set expectation
	expected = chart_clean_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


# Test for column name of 'Cancelled' and values of 'Yes' in cancelled rows
def test_remove_cancelled_yes_rows(input_chart_builder, chart_input_df, chart_no_cancelled_df):
	# setup
	# call function
	result = input_chart_builder.remove_cancelled_rows(chart_input_df)
	# set expectation
	expected = chart_no_cancelled_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


# Test for column name of 'Cancelled' and values of 'Cancelled' in cancelled rows
def test_remove_cancelled_cancelled_rows(input_chart_builder, chart_input_df, chart_no_cancelled_df):
	# setup
	chart_input_df.loc[chart_input_df['Cancelled'] == 'Yes'] = 'Cancelled'
	# call function
	result = input_chart_builder.remove_cancelled_rows(chart_input_df)
	# set expectation
	expected = chart_no_cancelled_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


# Test for column name of 'Resolution' and values of 'Yes' in cancelled rows (column export of Jira, but with 'yes' values)
def test_remove_resolution_yes_rows(input_chart_builder, chart_input_df, chart_no_cancelled_df):
	# setup
	chart_input_df.rename(columns={'Cancelled': 'Resolution'}, inplace=True)
	chart_no_cancelled_df.rename(columns={'Cancelled': 'Resolution'}, inplace=True)
	# call function
	result = input_chart_builder.remove_cancelled_rows(chart_input_df)
	# set expectation
	expected = chart_no_cancelled_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


# Test for column name of 'Resolution' and values of 'Cancelled' in cancelled rows (export of Jira)
def test_remove_resolution_cancelled_rows(input_chart_builder, chart_input_df, chart_no_cancelled_df):
	# setup
	chart_input_df.rename(columns={'Cancelled': 'Resolution'}, inplace=True)
	chart_no_cancelled_df.rename(columns={'Cancelled': 'Resolution'}, inplace=True)
	chart_input_df.loc[chart_input_df['Resolution'] == 'Yes'] = 'Cancelled'
	# call function
	result = input_chart_builder.remove_cancelled_rows(chart_input_df)
	# set expectation
	expected = chart_no_cancelled_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


def test_filtering_clean_df_to_start_date(input_chart_builder, chart_input_df, chart_clean_df,
										  chart_clean_filtered_to_start_date_df):
	# setup
	input_chart_builder.build_clean_df(chart_input_df)
	# call function
	result = input_chart_builder.filter_clean_df_to_start_date(chart_clean_df)
	# set expectation
	expected = chart_clean_filtered_to_start_date_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


def test_filtering_dates_df_to_start_date(input_chart_builder, flow_clean_alt_date_range_testing_df,
										  dates_filtered_df):
	# setup
	end_date = date(2022, 2, 20)
	# call function
	result = input_chart_builder.build_dates_df(flow_clean_alt_date_range_testing_df, end_date)
	# set expectation
	expected = dates_filtered_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


def test_not_filtering_dates_df_to_start_date(input_chart_builder, flow_clean_alt_date_range_testing_df,
											  dates_not_filtered_df):
	# setup
	end_date = date(2022, 2, 20)
	input_chart_builder.use_start_date = False
	# call function
	result = input_chart_builder.build_dates_df(flow_clean_alt_date_range_testing_df, end_date)
	# set expectation
	expected = dates_not_filtered_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


def test_build_completed_items_df(input_chart_builder, chart_clean_filtered_to_start_date_df, flow_completed_saved_items_df):
	# setup
	input_chart_builder.start_col = '1_InProgress'
	input_chart_builder.end_col = '2_Done'
	# call function
	result = input_chart_builder.build_completed_df(chart_clean_filtered_to_start_date_df)
	# set expectation
	expected = flow_completed_saved_items_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


def test_calc_completed_stats(input_chart_builder, flow_completed_saved_items_df):
	# setup
	input_chart_builder.start_col = '1_InProgress'
	input_chart_builder.end_col = '2_Done'
	end_date = date(2022, 2, 20)
	# call function
	input_chart_builder.calc_completed_stats(flow_completed_saved_items_df, end_date)
	# set expectation
	expected_cycle_time_85_confidence = 92.1
	expected_cycle_time_50_confidence = 83
	expected_cycle_time_average = 83
	expected_throughput_85_confidence = 1
	expected_throughput_50_confidence = 1
	expected_throughput_average = 0.05
	expected_prep_going_good = True
	# assertion
	assert expected_cycle_time_85_confidence == input_chart_builder.cycle_time_85_confidence
	assert expected_cycle_time_50_confidence == input_chart_builder.cycle_time_50_confidence
	assert expected_cycle_time_average == input_chart_builder.cycle_time_average
	assert expected_throughput_85_confidence == input_chart_builder.throughput_85_confidence
	assert expected_throughput_50_confidence == input_chart_builder.throughput_50_confidence
	assert expected_throughput_average == input_chart_builder.throughput_average
	assert expected_prep_going_good == input_chart_builder.prep_going_good


def test_prep_for_charting(input_chart_builder, chart_input_df, mocker):
		# setup
		test_calculator = input_chart_builder
		mocker.patch('ChartBuilderClass.get_flow_dataframe', return_value=chart_input_df)
		test_calculator.prep_for_charting()
		# call function
		result = test_calculator.prep_errors_were_found()
		# set expectation
		expected = False
		# assertion
		assert result == expected


# BUILD FUNCTION TESTING
###################################
def test_build_cfd_chart(input_chart_builder, dates_filtered_df, date_col_names,
					chart_clean_filtered_to_start_date_df, cfd_df):
	# setup
	# call function
	result = input_chart_builder.build_cfd_df(dates_filtered_df, date_col_names, chart_clean_filtered_to_start_date_df)
	# set expectation
	expected = cfd_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


def test_build_cfd_vectors(input_chart_builder, date_col_names, cfd_df, cfd_vectors_df):
	# setup
	# call function
	result = input_chart_builder.build_cfd_vectors(date_col_names, cfd_df)
	# set expectation
	expected = cfd_vectors_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


def test_build_aging_wip(input_chart_builder, chart_clean_filtered_to_start_date_df, date_col_names,
						 aging_wip_df):
	# setup
	input_chart_builder.start_col = '1_InProgress'
	input_chart_builder.end_col = '2_Done'
	# manually set these since we're not testing the calculation of cycle time stats
	input_chart_builder.cycle_time_85_confidence = 92.1
	input_chart_builder.cycle_time_50_confidence = 83.0
	input_chart_builder.cycle_time_average = 83.0
	# this represents date.today() in the program.
	end_date = date(2022, 2, 20)

	# call function
	result = input_chart_builder.build_aging_wip_df(chart_clean_filtered_to_start_date_df, date_col_names, end_date)

	# set expectation
	expected = aging_wip_df

	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


def test_build_run_df(input_chart_builder, dates_filtered_df, chart_clean_filtered_to_start_date_df, run_df):
	# setup
	input_chart_builder.start_col = '1_InProgress'
	input_chart_builder.end_col = '2_Done'
	# call function
	result = input_chart_builder.build_run_df(dates_filtered_df, chart_clean_filtered_to_start_date_df)
	# set expectation
	expected = run_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


def test_build_throughput_hist_df(input_chart_builder, run_df, throughput_hist_df):
	# setup
	# manually set these since we're not testing the calculation of throughput stats
	input_chart_builder.throughput_85_confidence = 1.0
	input_chart_builder.throughput_50_confidence = 1.0
	input_chart_builder.throughput_average = 0.05

	# call function
	result = input_chart_builder.build_throughput_histogram_df(run_df)

	# set expectation
	expected = throughput_hist_df

	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


def test_build_cycle_time_hist_df(input_chart_builder, aging_wip_df, cycle_time_hist_df):
	# setup
	input_chart_builder.end_col = '2_Done'
	# manually set these since we're not testing the calculation of cycle time stats
	input_chart_builder.cycle_time_85_confidence = 92.1
	input_chart_builder.cycle_time_50_confidence = 83.0
	input_chart_builder.cycle_time_average = 83.0

	# call function
	result = input_chart_builder.build_cycle_time_histogram_df(aging_wip_df)

	# set expectation
	expected = cycle_time_hist_df

	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


def test_build_cycle_time_scatter_df(input_chart_builder, aging_wip_df, cycle_time_scatter_df):
	# setup
	input_chart_builder.end_col = '2_Done'
	# manually set these since we're not testing the calculation of cycle time stats
	input_chart_builder.cycle_time_85_confidence = 96.0
	input_chart_builder.cycle_time_50_confidence = 96.0
	input_chart_builder.cycle_time_average = 96.0

	# call function
	result = input_chart_builder.build_cycle_time_scatter_df(aging_wip_df)

	# set expectation
	expected = cycle_time_scatter_df

	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


def test_building_all_charts(input_chart_builder, chart_input_df, cfd_df, cfd_vectors_df, aging_wip_df, run_df,
							 throughput_hist_df, cycle_time_hist_df, cycle_time_scatter_df, mocker):
	# setup
	mocker.patch('ChartBuilderClass.get_flow_dataframe', return_value=chart_input_df)
	input_chart_builder.prep_for_charting()

	# call function
	input_chart_builder.build_charts()
	resulting_errors = input_chart_builder.build_errors_were_found()

	# set expectation
	expected_errors = False
	expected_cfd = cfd_df
	expected_cfd_vectors = cfd_vectors_df
	expected_aging_wip = aging_wip_df
	expected_run_df = run_df
	expected_throughput_hist_df = throughput_hist_df
	expected_cycle_time_hist_df = cycle_time_hist_df
	expected_cycle_time_scatter_df = cycle_time_scatter_df

	# assertion
	assert resulting_errors == expected_errors
	assert pd.testing.assert_frame_equal(input_chart_builder.cfd_df, expected_cfd) is None
	assert pd.testing.assert_frame_equal(input_chart_builder.cfd_vectors, expected_cfd_vectors) is None
	assert pd.testing.assert_frame_equal(input_chart_builder.aging_wip_df, expected_aging_wip) is None
	assert pd.testing.assert_frame_equal(input_chart_builder.run_df, expected_run_df) is None
	assert pd.testing.assert_frame_equal(input_chart_builder.throughput_hist_df, expected_throughput_hist_df) is None
	assert pd.testing.assert_frame_equal(input_chart_builder.cycle_time_hist_df, expected_cycle_time_hist_df) is None
	assert pd.testing.assert_frame_equal(input_chart_builder.cycle_time_scatter_df, expected_cycle_time_scatter_df) is None
