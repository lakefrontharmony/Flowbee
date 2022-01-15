import pytest
import json
from ReleaseMetricCalcClass import ReleaseMetricCalcClass


# import fixtures to conftest.py file in the future
###################################
# FIXTURES
###################################
@pytest.fixture()
def input_calculator():
	return ReleaseMetricCalcClass()


@pytest.fixture()
def input_json_pipeline_file():
	return open('Files/pipeline_test.json')


@pytest.fixture()
def input_release_csv_file():
	return open('Files/fix_versions_unit_test.csv')


###################################
# UNIT TESTS
###################################
def test_matching_pipeline_entry_exists(input_json_pipeline_file, input_calculator):
	# setup
	input_calculator.read_json_file(input_json_pipeline_file)
	known_entry = 'odm-withdrawals'
	# call function
	result = input_calculator.pipeline_entry_exists_for(known_entry)

	# set expectation
	expected = True

	# assertion
	assert result == expected


def test_matching_pipeline_entry_doesnt_exist(input_file, input_calculator):
	# setup
	input_calculator.read_json_file(input_file)
	unknown_entry = 'withdrawals'
	# call function
	result = input_calculator.pipeline_entry_exists_for(unknown_entry)

	# set expectation
	expected = False

	# assertion
	assert result == expected
