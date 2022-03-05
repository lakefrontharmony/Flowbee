import pytest
import pandas as pd
from datetime import date
from ReleaseMetricCalcClass import ReleaseMetricCalcClass


# To run unit tests:
# 1. Navigate to UnitTests folder in terminal
# 2. execute "coverage run -m pytest" to run all "test_*" files in folder
# 3. execute "coverage report -m" to get a coverage report from that run
# 4. execute "coverage html" to get a browser file of the changes that were tested.
###################################
# FIXTURES
###################################
@pytest.fixture()
def input_release_calculator(input_json_pipeline_file):
	return_calculator = ReleaseMetricCalcClass()
	return_calculator.read_json_file(input_json_pipeline_file)
	return return_calculator


@pytest.fixture()
def test_release_in_file():
	return pd.DataFrame([['pipeline_num_1 1.0.56', date(2022, 1, 15), 'CRQ1', 'Released'],
						 ['pipeline_num_2 5.2.0', date(2022, 1, 1), 'CRQ2', 'Released'],
						 ['pipeline_num_3 24.9.4', date(2021, 12, 20), 'CRQ3', 'Released'],
						 ['pipeline_35.1', date(2022, 1, 5), '', 'Unreleased'],
						 ['pipeline_num_18  3.19 6', date(2021, 11, 20), 'CRQ4', 'Released'],
						 ['', date(2021, 11, 20), 'CRQ5', 'Unreleased'],
						 ['pipeline_num_6  1.23 6', date(2022, 1, 2), 'CRQ6', 'Released'],
						 ['pipeline_num_7 1.2.3', date(2021, 12, 31), '', 'Released']],
						columns=['Fix Version/s', 'Release Date', 'CRQ', 'Status'])


@pytest.fixture()
def test_release_cleaned_file():
	# Tests for expected formatting, and when there is accidentally no space (test_3: returns full name),
	# and when there is two spaces (test_4: still returns only up to first space)
	return pd.DataFrame([['pipeline_num_1 1.0.56', 'pipeline_num_1', date(2022, 1, 15), 'CRQ1'],
						 ['pipeline_num_2 5.2.0', 'pipeline_num_2', date(2022, 1, 1), 'CRQ2'],
						 ['pipeline_num_3 24.9.4', 'pipeline_num_3', date(2021, 12, 20), 'CRQ3'],
						 ['pipeline_35.1', 'pipeline_35.1', date(2022, 1, 5), ''],
						 ['pipeline_num_18  3.19 6', 'pipeline_num_18', date(2021, 11, 20), 'CRQ4'],
						 ['', '', date(2021, 11, 20), 'CRQ5'],
						 ['pipeline_num_6  1.23 6', 'pipeline_num_6', date(2022, 1, 2), 'CRQ6'],
						 ['pipeline_num_7 1.2.3', 'pipeline_num_7', date(2021, 12, 31), '']],
						columns=['Fix Version/s', 'System', 'Release Date', 'CRQ'])


@pytest.fixture()
def tested_release_against_pipeline_file():
	# Same as the cleaned file, but with a True/False column.
	# Tests first/last entries, middle active entries, entries on a pipeline which incorrectly missed a space,
	# entries on pipeline which aren't active, and entries not on pipelines
	return pd.DataFrame([['pipeline_num_1 1.0.56', 'pipeline_num_1', date(2022, 1, 15), 'CRQ1', 'True'],
						 ['pipeline_num_2 5.2.0', 'pipeline_num_2', date(2022, 1, 1), 'CRQ2', 'True'],
						 ['pipeline_num_3 24.9.4', 'pipeline_num_3', date(2021, 12, 20), 'CRQ3', 'False'],
						 ['pipeline_35.1', 'pipeline_35.1', date(2022, 1, 5), '', 'False'],
						 ['pipeline_num_18  3.19 6', 'pipeline_num_18', date(2021, 11, 20), 'CRQ4', 'False'],
						 ['', '', date(2021, 11, 20), 'CRQ5', 'False'],
						 ['pipeline_num_6  1.23 6', 'pipeline_num_6', date(2022, 1, 2), 'CRQ6', 'True'],
						 ['pipeline_num_7 1.2.3', 'pipeline_num_7', date(2021, 12, 31), '', 'False']],
						columns=['Fix Version/s', 'System', 'Release Date', 'CRQ', 'On Pipeline'])


@pytest.fixture()
def releases_between_dec_15_2021_and_jan_15_2022_df():
	return pd.DataFrame([['pipeline_num_1 1.0.56', 'pipeline_num_1', date(2022, 1, 15), 'CRQ1', 'True'],
						 ['pipeline_num_2 5.2.0', 'pipeline_num_2', date(2022, 1, 1), 'CRQ2', 'True'],
						 ['pipeline_num_3 24.9.4', 'pipeline_num_3', date(2021, 12, 20), 'CRQ3', 'False'],
						 ['pipeline_35.1', 'pipeline_35.1', date(2022, 1, 5), '', 'False'],
						 ['pipeline_num_6  1.23 6', 'pipeline_num_6', date(2022, 1, 2), 'CRQ6', 'True'],
						 ['pipeline_num_7 1.2.3', 'pipeline_num_7', date(2021, 12, 31), '', 'False']],
						columns=['Fix Version/s', 'System', 'Release Date','CRQ', 'On Pipeline'])


@pytest.fixture()
def pipeline_count_df():
	return pd.DataFrame([['False', 5],
						 ['True', 3]], columns=['On Pipeline', 'Count'])


@pytest.fixture()
def deployment_summary_df():
	return pd.DataFrame([[date(2021, 11, 20), 1, 2],
						 [date(2021, 12, 20), 1, 1],
						 [date(2021, 12, 31), 1, 0],
						 [date(2022, 1, 1), 1, 1],
						 [date(2022, 1, 2), 1, 1],
						 [date(2022, 1, 5), 1, 0],
						 [date(2022, 1, 15), 1, 1]
						 ], columns=['Release Date', 'Systems', 'CRQs'])


###################################
# UNIT TESTS
###################################
def test_open_and_create_release_dataframe(input_release_calculator, test_release_in_file):
	# setup
	in_file = '../Files/UnitTestFiles/test_release_in_file.csv'
	# call function
	input_release_calculator.read_releases_csv_file(in_file)
	result = input_release_calculator.get_release_df()
	# set expectation
	expected = test_release_in_file
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


def test_matching_pipeline_entry_exists(input_release_calculator):
	# setup
	known_entry = 'pipeline_num_2'
	# call function
	result = input_release_calculator.pipeline_entry_exists_for(known_entry)
	# set expectation
	expected = 'True'
	# assertion
	assert result == expected


def test_matching_pipeline_entry_exists_but_not_available(input_release_calculator):
	# setup
	known_entry = 'pipeline_num_3'
	# call function
	result = input_release_calculator.pipeline_entry_exists_for(known_entry)
	# set expectation
	expected = 'False'
	# assertion
	assert result == expected


def test_matching_pipeline_entry_doesnt_exist(input_release_calculator):
	# setup
	unknown_entry = 'withdrawals'
	# call function
	result = input_release_calculator.pipeline_entry_exists_for(unknown_entry)
	# set expectation
	expected = 'False'
	# assertion
	assert result == expected


def test_stripping_fix_version_of_release_numbers(input_release_calculator, test_release_in_file, test_release_cleaned_file):
	# setup
	# call function
	result = input_release_calculator.strip_release_name_of_version(test_release_in_file)
	# set expectation
	expected = test_release_cleaned_file
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


def test_comparing_release_df_to_pipelines(input_release_calculator, test_release_cleaned_file,
										   tested_release_against_pipeline_file):
	# setup
	# call function
	result = input_release_calculator.check_df_for_pipelines(test_release_cleaned_file)
	# set expectation
	expected = tested_release_against_pipeline_file
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


def test_comparing_release_df_to_pipeline_between_dates(input_release_calculator, test_release_cleaned_file,
														releases_between_dec_15_2021_and_jan_15_2022_df):
	# setup
	start_date = date(2021, 12, 15)
	end_date = date(2022, 1, 15)
	# call function
	result = input_release_calculator.check_df_for_pipelines_between_dates(test_release_cleaned_file, start_date, end_date)
	# set expectation
	expected = releases_between_dec_15_2021_and_jan_15_2022_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


def test_build_pipeline_summary_pd(input_release_calculator, tested_release_against_pipeline_file, pipeline_count_df):
	# setup
	# call function
	result = input_release_calculator.build_pipeline_summary_df(tested_release_against_pipeline_file)
	# set expectation
	expected = pipeline_count_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


def test_build_deployment_summary_pd(input_release_calculator, tested_release_against_pipeline_file, deployment_summary_df):
	# setup
	# call function
	result = input_release_calculator.build_release_summary(tested_release_against_pipeline_file)
	# set expectation
	expected = deployment_summary_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


# This should return 1 because the test file has 1 out of 2 entries for this date as a blank fix version.
def test_count_fix_versions_on_date(input_release_calculator, tested_release_against_pipeline_file):
	# setup
	in_date = date(2021, 11, 20)
	col_name = 'Fix Version/s'
	# call function
	result = input_release_calculator.count_entries_on_date(tested_release_against_pipeline_file, in_date, col_name)
	# set expectation
	expected = 1
	# assertion
	assert result == expected


def test_count_crq_on_date(input_release_calculator, tested_release_against_pipeline_file):
	# setup
	in_date = date(2021, 11, 20)
	col_name = 'CRQ'
	# call function
	result = input_release_calculator.count_entries_on_date(tested_release_against_pipeline_file, in_date, col_name)
	# set expectation
	expected = 2
	# assertion
	assert result == expected


# The input file has a release on 1/5/2022 but no CRQ assigned. This should return a zero for that date.
def test_blank_crq_on_date(input_release_calculator, tested_release_against_pipeline_file):
	# setup
	in_date = date(2022, 1, 5)
	col_name = 'CRQ'
	# call function
	result = input_release_calculator.count_entries_on_date(tested_release_against_pipeline_file, in_date, col_name)
	# set expectation
	expected = 0
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