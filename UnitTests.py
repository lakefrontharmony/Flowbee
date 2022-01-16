import pytest
import pandas as pd
from ReleaseMetricCalcClass import ReleaseMetricCalcClass


# import fixtures to conftest.py file in the future
###################################
# FIXTURES
###################################
@pytest.fixture()
def input_calculator(input_json_pipeline_file):
	return_calculator = ReleaseMetricCalcClass()
	return_calculator.read_json_file(input_json_pipeline_file)
	return return_calculator


@pytest.fixture()
def input_json_pipeline_file():
	return open('Files/pipeline_example.json')


@pytest.fixture()
def input_release_csv_file():
	return open('Files/fix_versions_unit_test.csv')


@pytest.fixture()
def test_release_in_file():
	return pd.DataFrame([['pipeline_num_1 1.0.56', '2022-01-15'],
						 ['pipeline_num_2 5.2.0', '2022-01-01'],
						 ['pipeline_num_3 24.9.4', '2021-12-20'],
						 ['pipeline_35.1', '2022-01-05'],
						 ['pipeline_num_6  1.23 6', '2022-01-02'],
						 ['pipeline_num_7 1.2.3', '2021-12-31']],
						columns=['Fix Version/s', 'Release Date'])


@pytest.fixture()
def test_release_cleaned_file():
	# Tests for expected formatting, and when there is accidentally no space (test_3: returns full name),
	# and when there is two spaces (test_4: still returns only up to first space)
	return pd.DataFrame([['pipeline_num_1', '2022-01-15'],
						 ['pipeline_num_2', '2022-01-01'],
						 ['pipeline_num_3','2021-12-20'],
						 ['pipeline_35.1','2022-01-05'],
						 ['pipeline_num_6', '2022-01-02'],
						 ['pipeline_num_7', '2021-12-31']],
						columns=['Fix Version/s', 'Release Date'])


@pytest.fixture()
def tested_release_against_pipeline_file():
	# Same as the cleaned file, but with a True/False column.
	# Tests first/last entries, middle active entries, entries on a pipeline which incorrectly missed a space,
	# entries on pipeline which aren't active, and entries not on pipelines
	return pd.DataFrame([['pipeline_num_1', '2022-01-15', 'True'],
						 ['pipeline_num_2', '2022-01-01', 'True'],
						 ['pipeline_num_3','2021-12-20', 'False'],
						 ['pipeline_35.1','2022-01-05', 'False'],
						 ['pipeline_num_6', '2022-01-02', 'True'],
						 ['pipeline_num_7', '2021-12-31', 'False']],
						columns=['Fix Version/s', 'Release Date', 'On Pipeline'])


# TODO: Build results dataframe to display in streamlit
@pytest.fixture()
def results_dataframe():
	pass


###################################
# UNIT TESTS
###################################
def test_matching_pipeline_entry_exists(input_calculator):
	# setup
	known_entry = 'pipeline_num_2'
	# call function
	result = input_calculator.pipeline_entry_exists_for(known_entry)

	# set expectation
	expected = 'True'

	# assertion
	assert result == expected


def test_matching_pipeline_entry_exists_but_not_available(input_calculator):
	# setup
	known_entry = 'pipeline_num_3'
	# call function
	result = input_calculator.pipeline_entry_exists_for(known_entry)

	# set expectation
	expected = 'False'

	# assertion
	assert result == expected


def test_matching_pipeline_entry_doesnt_exist(input_calculator):
	# setup
	unknown_entry = 'withdrawals'
	# call function
	result = input_calculator.pipeline_entry_exists_for(unknown_entry)

	# set expectation
	expected = 'False'

	# assertion
	assert result == expected


def test_stripping_fix_version_of_release_numbers(input_calculator, test_release_in_file, test_release_cleaned_file):
	# setup
	# call function
	result = input_calculator.strip_release_name_of_version(test_release_in_file)
	# set expectation
	expected = test_release_cleaned_file
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


def test_comparing_release_df_to_pipelines(input_calculator, test_release_cleaned_file,
										   tested_release_against_pipeline_file):
	# setup
	# call function
	result = input_calculator.check_df_for_pipelines(test_release_cleaned_file)
	# set expectation
	expected = tested_release_against_pipeline_file
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


"""
def test_capsys_output(capsys):
	print('testing an output')
	captured = capsys.readouterr()
	assert captured.out == 'testing an output'
	asser captured.err == ''
"""