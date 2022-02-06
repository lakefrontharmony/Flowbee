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
# This is the clean dataframe filtered to a start date for the ChartBuilderClass
@pytest.fixture()
def chart_clean_filtered_to_start_date_df():
	return pd.DataFrame([['TestZ5', date(2021, 10, 6), date(2022, 1, 10), 4],
						 ['TestZ7', date(2022, 1, 3), pd.NaT, 4]],
						columns=['Name', '1_InProgress', '2_Done', 'WIPLimit'])


# This is the clean dataframe for the ChartBuilderClass
@pytest.fixture()
def chart_clean_df():
	return pd.DataFrame([['TestA2', date(2021, 10, 2), date(2021, 11, 1), 4],
						 ['TestB1', date(2021, 12, 15), date(2021, 12, 20), 4],
						 ['TestC3', date(2021, 5, 1), date(2022, 1, 5), 4],
						 ['TestZ5',date(2021, 10, 6), date(2022, 1, 10), 4],
						 ['TestZ7',date(2022, 1, 3), pd.NaT, 4]],
						 columns=['Name', '1_InProgress', '2_Done', 'WIPLimit'])


@pytest.fixture()
def flow_completed_saved_items_df():
	return pd.DataFrame([['TestA2', date(2021, 10, 2), date(2021, 11, 1), 4],
						 ['TestB1', date(2021, 12, 15), date(2021, 12, 20), 4],
						 ['TestC3', date(2021, 5, 1), date(2022, 1, 5), 4],
						 ['TestZ5', date(2021, 10, 6), date(2022, 1, 10), 4]],
						columns=['Name', '1_InProgress', '2_Done', 'WIPLimit'])


@pytest.fixture()
def flow_clean_alt_date_range_testing_df():
	return pd.DataFrame([[datetime(2022, 1, 8), datetime(2022, 1, 30), 'Enabler', 15.0],
						 [datetime(2022, 1, 18), datetime(2022, 1, 31), 'Strategic', 13.0],
						 [datetime(2022, 1, 26), datetime(2022, 2, 1), 'Strategic', 6.0]],
						columns=['InProgress', 'Done', 'Type', 'lead_time'])


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
						 [datetime(2022, 2, 3), 0, 0, 0]],
						columns=['Date', 'WIP', 'Throughput', 'Avg Cycle Time'])


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
						 [datetime(2022, 2, 3), 0, 0, 0]],
						columns=['Date', 'WIP', 'Throughput', 'Avg Cycle Time'])


# This is the build of the FlowCalcClass
@pytest.fixture()
def input_chart_builder():
	start_col = 'InProgress'
	end_col = 'Done'
	item_names = 'Name'
	start_date_toggle = True
	start_date = '2022-01-09'
	wip_limit = 4
	return ChartBuilderClass(start_col, end_col, item_names, start_date_toggle, start_date, wip_limit)


###################################
# UNIT TESTS
###################################
# TODO: Get this to run successfully
def test_build_clean_df(input_chart_builder, flow_input_df, chart_clean_df):
	# setup
	# call function
	result = input_chart_builder.build_clean_df(flow_input_df)
	# set expectation
	expected = chart_clean_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


def test_remove_cancelled_rows(input_chart_builder, flow_input_df, flow_no_cancelled_df):
	# setup
	# call function
	result = input_chart_builder.remove_cancelled_rows(flow_input_df)
	# set expectation
	expected = flow_no_cancelled_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


def test_filtering_clean_df_to_start_date(input_chart_builder, flow_input_df, chart_clean_df,
										  chart_clean_filtered_to_start_date_df):
	# setup
	input_chart_builder.build_clean_df(flow_input_df)
	# call function
	result = input_chart_builder.filter_clean_df_to_start_date(chart_clean_df)
	# set expectation
	expected = chart_clean_filtered_to_start_date_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


def test_filtering_dates_df_to_start_date(input_chart_builder, flow_clean_alt_date_range_testing_df,
										  dates_filtered_df):
	# setup
	end_date = date(2022, 2, 3)
	# call function
	result = input_chart_builder.build_dates_df(flow_clean_alt_date_range_testing_df, end_date)
	# set expectation
	expected = dates_filtered_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


def test_not_filtering_dates_df_to_start_date(input_chart_builder, flow_clean_alt_date_range_testing_df,
											  dates_not_filtered_df):
	# setup
	end_date = date(2022, 2, 3)
	input_chart_builder.use_start_date = False
	# call function
	result = input_chart_builder.build_dates_df(flow_clean_alt_date_range_testing_df, end_date)
	# set expectation
	expected = dates_not_filtered_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


def test_build_completed_items_df(input_chart_builder, chart_clean_df, flow_completed_saved_items_df):
	# setup
	input_chart_builder.start_col = '1_InProgress'
	input_chart_builder.end_col = '2_Done'
	# call function
	result = input_chart_builder.build_completed_df(chart_clean_df)
	# set expectation
	expected = flow_completed_saved_items_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None
