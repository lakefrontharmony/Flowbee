import pytest
import pandas as pd
from datetime import datetime


# To run unit tests:
# 1. Navigate to UnitTests folder in terminal
# 2. execute "coverage run -m pytest" to run all "test_*" files in folder
# 3. execute "coverage report -m" to get a coverage report from that run
# 4. execute "coverage html" to get a browser file of the changes that were tested.
###################################
# Flow Metric Testing
###################################
# This is the dataframe that mimics an input file (with column names already stripped of spaces)
@pytest.fixture()
def flow_input_df():
	return pd.DataFrame([['A1', 'TestA1', 'Parent1', '2021-11-01', '2021-11-10', '2021-12-01', 'Yes', 'Strategic'],
						 ['A2', 'TestA2', 'Parent1', '2021-10-01', '2021-10-02', '2021-11-01', '', 'Strategic'],
						 ['B1', 'TestB1', 'Parent2', '2021-12-01', '2021-12-15', '2021-12-20', '', 'Maintenance'],
						 ['C3', 'TestC3', 'Parent3', '2021-01-01', '2021-05-01', '2022-01-05', '', 'Strategic'],
						 ['C4', 'TestC4', 'Parent3', '', '', '', '', 'Strategic'],
						 ['Z5', 'TestZ5', 'Parent4', '2021-08-08', '2021-10-06', '2022-01-10', '', 'Enabler'],
						 ['Z7', 'TestZ7', 'Parent4', '2022-01-01', '2022-01-03', '', '', 'Strategic']],
						 columns=['ID', 'Name', 'Parent', 'Ready', 'InProgress', 'Done', 'Cancelled', 'Type'])


# This is the dataframe after removing cancelled items
@pytest.fixture()
def flow_no_cancelled_df():
	return pd.DataFrame([['A2', 'TestA2', 'Parent1', '2021-10-01', '2021-10-02', '2021-11-01', '', 'Strategic'],
						 ['B1', 'TestB1', 'Parent2', '2021-12-01', '2021-12-15', '2021-12-20', '', 'Maintenance'],
						 ['C3', 'TestC3', 'Parent3', '2021-01-01', '2021-05-01', '2022-01-05', '', 'Strategic'],
						 ['C4', 'TestC4', 'Parent3', '', '', '', '', 'Strategic'],
						 ['Z5', 'TestZ5', 'Parent4', '2021-08-08', '2021-10-06', '2022-01-10', '', 'Enabler'],
						 ['Z7', 'TestZ7', 'Parent4', '2022-01-01', '2022-01-03', '', '', 'Strategic']],
						 columns=['ID', 'Name', 'Parent', 'Ready', 'InProgress', 'Done', 'Cancelled', 'Type'])


# This is the dataframe coming out of the "build_clean_df" function
@pytest.fixture()
def flow_clean_df():
	return pd.DataFrame([[datetime(2021, 5, 1), datetime(2022, 1, 5), 'Strategic', 249.0],
						 [datetime(2021, 10, 6), datetime(2022, 1, 10), 'Enabler', 96.0]],
						 columns=['InProgress', 'Done', 'Type', 'lead_time'])


###################################
# Release Metric Testing
###################################
@pytest.fixture()
def input_json_pipeline_file():
	return open('../Files/UnitTestFiles/pipeline_example.json')   # pragma: no cover


@pytest.fixture()
def input_release_csv_file():
	return open('../Files/UnitTestFiles/fix_versions_unit_test.csv')   # pragma: no cover
