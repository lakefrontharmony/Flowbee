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
						 ['D6', 'TestD6', 'Parent4', '2022-01-02', '2022-01-02', '2022-01-20', '', 'Strategic'],
						 ['D7', 'TestD7', 'Parent4', '2022-01-01', '2022-01-02', '2022-01-20', '', 'Strategic'],
						 ['Z3', 'TestZ3', 'Parent9', '2021-11-02', '2021-12-02', '2022-02-10', '', 'Maintenance'],
						 ['Z4', 'TestZ4', 'Parent9', '2021-11-02', '2021-12-02', '2022-02-10', '', 'Maintenance'],
						 ['Z5', 'TestZ5', 'Parent9', '2021-08-08', '2021-10-06', '2022-01-10', '', 'Enabler'],
						 ['Z6', 'TestZ6', 'Parent9', '2021-11-02', '2021-12-02', '2022-02-10', '', 'Maintenance'],
						 ['Z7', 'TestZ7', 'Parent9', '2022-01-01', '2022-01-03', '', '', 'Strategic']],
						 columns=['ID', 'Name', 'Parent', 'Ready', 'InProgress', 'Done', 'Cancelled', 'Type'])


# This is the dataframe that mimics an input file and has no entries after clearing out not-started and cancelled
# entries as of 02/15/2022
@pytest.fixture()
def simulator_input_not_started_df():
	return pd.DataFrame([['A1', 'TestA1', 'Parent1', '2021-11-01', '2021-11-10', '2021-12-01', 'Yes', 'Strategic'],
						 ['A4', 'TestA4', 'Parent1', '2022-01-05', '2022-01-10', '2022-01-30', 'Cancelled', 'Strategic'],
						 ['C4', 'TestC4', 'Parent3', '2022-01-05', '', '', '', 'Strategic']],
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
						 ['D6', 'TestD6', 'Parent4', '2022-01-02', datetime(2022, 1, 2), datetime(2022, 1, 20), '', 'Strategic'],
						 ['D7', 'TestD7', 'Parent4', '2022-01-01', datetime(2022, 1, 2), datetime(2022, 1, 20), '', 'Strategic'],
						 ['Z3', 'TestZ3', 'Parent9', '2021-11-02', datetime(2021, 12, 2), datetime(2022, 2, 10), '', 'Maintenance'],
						 ['Z4', 'TestZ4', 'Parent9', '2021-11-02', datetime(2021, 12, 2), datetime(2022, 2, 10), '', 'Maintenance'],
						 ['Z5', 'TestZ5', 'Parent9', '2021-08-08', datetime(2021, 10, 6), datetime(2022, 1, 10), '', 'Enabler'],
						 ['Z6', 'TestZ6', 'Parent9', '2021-11-02', datetime(2021, 12, 2), datetime(2022, 2, 10), '', 'Maintenance']],
						 columns=['ID', 'Name', 'Parent', 'Ready', 'InProgress', 'Done', 'Cancelled', 'Type'])


# This is the dataframe after build_clean_dataframe using 01/16/2022 - 2/15/2022 date range (exludes 03/01/2022 item)
@pytest.fixture()
def simulator_clean_df_excluding_future_date_test():
	return pd.DataFrame([[datetime(2021, 11, 16), datetime(2022, 1, 20)],
						 [datetime(2022, 1, 1), datetime(2022, 1, 20)],
						 [datetime(2022, 1, 21), datetime(2022, 2, 1)],
						 [datetime(2022, 2, 3), datetime(2022, 2, 5)],
						 [datetime(2022, 1, 2), datetime(2022, 1, 20)],
						 [datetime(2022, 1, 2), datetime(2022, 1, 20)],
						 [datetime(2021, 12, 2), datetime(2022, 2, 10)],
						 [datetime(2021, 12, 2), datetime(2022, 2, 10)],
						 [datetime(2021, 12, 2), datetime(2022, 2, 10)]],
						 columns=['InProgress', 'Done'])


# This is the dataframe after build_clean_dataframe (2022-01-30 - 2022-3-1 date range)
@pytest.fixture()
def simulator_clean_df():
	return pd.DataFrame([[datetime(2022, 1, 21), datetime(2022, 2, 1)],
						 [datetime(2022, 2, 3), datetime(2022, 2, 5)],
						 [datetime(2022, 2, 2), datetime(2022, 3, 1)],
						 [datetime(2021, 12, 2), datetime(2022, 2, 10)],
						 [datetime(2021, 12, 2), datetime(2022, 2, 10)],
						 [datetime(2021, 12, 2), datetime(2022, 2, 10)]],
						 columns=['InProgress', 'Done'])


# This is the dataframe after build_dates_dataframe using "last month" option (30 days) (using end date of 2/15/2022)
@pytest.fixture()
def dates_df_one_month():
	return pd.DataFrame([[datetime(2022, 1, 30), 0],
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
						 [datetime(2022, 2, 15), 0],
						 [datetime(2022, 2, 16), 0],
						 [datetime(2022, 2, 17), 0],
						 [datetime(2022, 2, 18), 0],
						 [datetime(2022, 2, 19), 0],
						 [datetime(2022, 2, 20), 0],
						 [datetime(2022, 2, 21), 0],
						 [datetime(2022, 2, 22), 0],
						 [datetime(2022, 2, 23), 0],
						 [datetime(2022, 2, 24), 0],
						 [datetime(2022, 2, 25), 0],
						 [datetime(2022, 2, 26), 0],
						 [datetime(2022, 2, 27), 0],
						 [datetime(2022, 2, 28), 0],
						 [datetime(2022, 3, 1), 0]],
						 columns=['Date', 'Frequency'])


# This is the dataframe after build_dist_dataframe using "last month" option (30 days) (using end date of 2/15/2022)
@pytest.fixture()
def dist_df_one_month():
	return pd.DataFrame([[0.0, 0.8709677419354839],
						 [1.0, 0.0967741935483871],
						 [2.0, 0],
						 [3.0, 0.03225806451612903]],
						 columns=['Count', 'Frequency'])


# This is the dataframe after build_display_percentiles_df using "last month" option (30 days) (using end date of 2/15/2022)
@pytest.fixture()
def display_dist_df_one_month():
	return pd.DataFrame([[0.0, '87.1%'],
						 [1.0, '9.68%'],
						 [2.0, '0.0%'],
						 [3.0, '3.23%']],
						 columns=['Count', 'Frequency'])


# This is the dataframe after final_field_preparation using "last month" option (30 days) (using end date of 2/15/2022)
@pytest.fixture()
def simulation_stats_one_month():
	return pd.DataFrame([['Historical Date Range', '2022-01-30 - 2022-03-01'],
						 ['Simulation Date Range', '2022-01-19 - 2022-04-12'],
						 ['Number of Days For "How Many" Sim', '84'],
						 ['Number of Items For "When" Sim', '4'],
						 ['Max Throughput Per Day:', '3']],
						 columns=['Category', 'Value'])


@pytest.fixture()
def final_sim_stats():
	return pd.DataFrame([['Historical Date Range', '2022-01-30 - 2022-03-01'],
						 ['Simulation Date Range', '2022-01-19 - 2022-04-12'],
						 ['Number of Days For "How Many" Sim', '84'],
						 ['Number of Items For "When" Sim', '4'],
						 ['Max Throughput Per Day:', '3'],
						 ['Avg # Completed In "How Many" Sim (Rounded)', '6 items'],
						 ['Most Freq. # Completed In "How Many" Sim', '6 items'],
						 ['Avg Date To Complete Items In "When" Sim (Rounded)', '2022-02-01'],
						 ['Most Freq. Date To Complete Items in "When" Sim', '2022-02-01']],
						columns=['Category', 'Value'])


# This is the mock return from np.random.default_rng().choice
@pytest.fixture()
def daily_entries_completed_mocked_list():
	return [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0,
			0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
			0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
			0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]


# This is the mock return from np.random.default_rng().choice for the full run_mc_simulation test
@pytest.fixture()
def full_daily_entries_completed_mocked_list():
	return [[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0,  # 1
			0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
			0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
			0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
			[0, 0, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0,  # 2
			 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
			 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
			 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
			[0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0,  # 3
			 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
			 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
			 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1, 0, 1, 0, 0, 0,  # 4
			 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
			 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
			 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
			[0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0,  # 5
			 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
			 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
			 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
			[0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 3, 0, 3, 0, 0, 0, 1, 0, 0, 0,  # 6
			 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
			 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
			 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
			[0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0,  # 7
			 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
			 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
			 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
			[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0,  # 8
			 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
			 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
			 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0,  # 9
			 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
			 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1, 0, 0, 0, 0, 0,
			 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0,  # 10
			 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
			 0, 0, 0, 1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
			 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],]


# This is the dataframe after run_monte_carlo_simulations for "how_many" simulation (10 iterations)
@pytest.fixture()
def how_many_sim_output():
	return pd.DataFrame([[6.0],
						 [6.0],
						 [6.0],
						 [6.0],
						 [6.0],
						 [6.0],
						 [6.0],
						 [6.0],
						 [6.0],
						 [6.0]],
						 columns=['Output'])


# This is the dataframe after run_monte_carlo_simulations for "when" simulation (10 iterations)
@pytest.fixture()
def when_sim_output():
	return pd.DataFrame([[13.0],
						 [13.0],
						 [13.0],
						 [13.0],
						 [13.0],
						 [13.0],
						 [13.0],
						 [13.0],
						 [13.0],
						 [13.0]],
						 columns=['Output'])


@pytest.fixture()
def how_many_pct_df():
	return pd.DataFrame([[6.0],
						 [6.0],
						 [6.0],
						 [6.0]],
						columns=['Count_Percentiles'], index=[0.95, 0.85, 0.7, 0.5])


@pytest.fixture()
def when_pct_df():
	return pd.DataFrame([[13.0, '2022-02-01'],
						 [13.0, '2022-02-01'],
						 [13.0, '2022-02-01'],
						 [13.0, '2022-02-01']],
						columns=['Days_Percentiles', 'End_Date'], index=[0.95, 0.85, 0.7, 0.5])


# This is the "how_many_sim_output" dataframe for the full run_mc_simulations test (10 iterations)
@pytest.fixture()
def full_how_many_sim_output():
	return pd.DataFrame([[12.0],
						 [15.0],
						 [13.0],
						 [12.0],
						 [14.0],
						 [17.0],
						 [13.0],
						 [12.0],
						 [12.0],
						 [12.0]],
						 columns=['Output'])


# This is the "when_sim_output" dataframe for the full run_mc_simulations test (10 iterations)
@pytest.fixture()
def full_when_sim_output():
	return pd.DataFrame([[13.0],
						 [4.0],
						 [13.0],
						 [15.0],
						 [13.0],
						 [11.0],
						 [13.0],
						 [13.0],
						 [33.0],
						 [33.0]],
						 columns=['Output'])


# This is the "how_many_pct" dataframe for the full run_mc_simulations test (10 iterations)
@pytest.fixture()
def full_how_many_pct_df():
	return pd.DataFrame([[12.0],
						 [12.0],
						 [12.0],
						 [12.5]],
						columns=['Count_Percentiles'], index=[0.95, 0.85, 0.7, 0.5])


# This is the "when_pct" dataframe for the full run_mc_simulations test (10 iterations)
@pytest.fixture()
def full_when_pct_df():
	return pd.DataFrame([[33.0, '2022-02-21'],
						 [26.69999999999999, '2022-02-14'],
						 [13.6, '2022-02-01'],
						 [13.0, '2022-02-01']],
						columns=['Days_Percentiles', 'End_Date'], index=[0.95, 0.85, 0.7, 0.5])


# This is the "sim_stats" dataframe for the full run_mc_simulations test (10 iterations)
@pytest.fixture()
def full_final_sim_stats():
	return pd.DataFrame([['Historical Date Range', '2022-01-30 - 2022-03-01'],
						 ['Simulation Date Range', '2022-01-19 - 2022-04-12'],
						 ['Number of Days For "How Many" Sim', '84'],
						 ['Number of Items For "When" Sim', '4'],
						 ['Max Throughput Per Day:', '3'],
						 ['Avg # Completed In "How Many" Sim (Rounded)', '13 items'],
						 ['Most Freq. # Completed In "How Many" Sim', '12 items'],
						 ['Avg Date To Complete Items In "When" Sim (Rounded)', '2022-02-04'],
						 ['Most Freq. Date To Complete Items in "When" Sim', '2022-02-01']],
						columns=['Category', 'Value'])

# This is the build of the SimulationCalcClass
@pytest.fixture()
def input_simulator_builder():
	duration = 'Last Month In File'
	start_col = 'InProgress'
	end_col = 'Done'
	sim_start = '2022-01-19'
	sim_end = '2022-04-12'
	num_to_complete = 4
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
	input_simulator_builder.duration = 'Last 12 Months In File'
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
def test_building_clean_dataframe(input_simulator_builder, simulator_prepped_df,
								  simulator_clean_df_excluding_future_date_test):
	# setup
	# set these values since we are not running through other prep functions
	input_simulator_builder.start_date = datetime(2022, 1, 16)
	# call function
	result = input_simulator_builder.build_clean_dataframe(simulator_prepped_df)
	# set expectation
	expected = simulator_clean_df_excluding_future_date_test
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


# Build dates dataframe. Only use last 30 days so that the return df is manageable for this test.
def test_building_dates_df_for_30_days(input_simulator_builder, dates_df_one_month):
	# setup
	# set these values since we are not running through other prep functions
	input_simulator_builder.start_date = datetime(2022, 1, 30)
	input_simulator_builder.end_date = datetime(2022, 3, 1)
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
	input_simulator_builder.start_date = datetime(2022, 1, 30)
	input_simulator_builder.end_date = datetime(2022, 3, 1)
	# call function
	result = input_simulator_builder.build_dist_dataframe(simulator_clean_df, dates_df_one_month)
	# set expectation
	expected = dist_df_one_month
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


def test_build_display_percentiles_df(input_simulator_builder, dist_df_one_month, display_dist_df_one_month):
	# setup
	# set these values since we are not running through other prep functions
	input_simulator_builder.start_date = datetime(2022, 1, 16)
	# call function
	result = input_simulator_builder.build_display_percentiles_df(dist_df_one_month)
	# set expectation
	expected = display_dist_df_one_month
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


# test building final fields for calculations
def test_final_field_preparation(input_simulator_builder, dist_df_one_month, simulator_clean_df, simulation_stats_one_month):
	# setup
	# set these values since we are not running through other prep functions
	input_simulator_builder.start_date = datetime(2022, 1, 30)
	input_simulator_builder.end_date = datetime(2022, 3, 1)
	# call function
	input_simulator_builder.final_field_preparation(dist_df_one_month, simulator_clean_df)
	result = input_simulator_builder.get_simulation_stats()
	# set expectation
	expected = simulation_stats_one_month
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


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


# Full test of prep_for_simulations
def test_prep_for_simulations(input_simulator_builder, simulator_input_df, simulator_clean_df, dates_df_one_month,
							  dist_df_one_month, display_dist_df_one_month, simulation_stats_one_month, mocker):
	# setup
	mocker.patch('SimulationCalcClass.get_input_dataframe', return_value=simulator_input_df)

	# call function
	input_simulator_builder.prep_for_simulation()
	result_clean_df = input_simulator_builder.clean_df
	result_start_date = input_simulator_builder.start_date
	result_end_date = input_simulator_builder.end_date
	result_dates_df = input_simulator_builder.dates_df
	result_dist_df = input_simulator_builder.dist_df
	result_display_dist_df = input_simulator_builder.display_dist_df
	result_simulation_stats = input_simulator_builder.simulation_stats

	# set expectation
	expected_clean_df = simulator_clean_df
	expected_start_date = datetime(2022, 1, 30)
	expected_end_date = datetime(2022, 3, 1)
	expected_dates_df = dates_df_one_month
	expected_dist_df = dist_df_one_month
	expected_display_dist_df = display_dist_df_one_month
	expected_simulation_stats = simulation_stats_one_month

	# assertion
	assert pd.testing.assert_frame_equal(result_clean_df, expected_clean_df) is None
	assert result_start_date == expected_start_date
	assert result_end_date == expected_end_date
	assert pd.testing.assert_frame_equal(result_dates_df, expected_dates_df) is None
	assert pd.testing.assert_frame_equal(result_dist_df, expected_dist_df) is None
	assert pd.testing.assert_frame_equal(result_display_dist_df, expected_display_dist_df) is None
	assert pd.testing.assert_frame_equal(result_simulation_stats, expected_simulation_stats) is None


# Full test of prep_for_simulations
def test_prep_with_current_wip(input_simulator_builder_use_current_wip, simulator_input_df, mocker):
	# setup
	mocker.patch('SimulationCalcClass.get_input_dataframe', return_value=simulator_input_df)

	# call function
	input_simulator_builder_use_current_wip.prep_for_simulation()
	result_num_items_to_simulate = input_simulator_builder_use_current_wip.num_items_to_simulate

	# set expectation
	expected_num_items_to_simulate = 2

	# assertion
	assert result_num_items_to_simulate == expected_num_items_to_simulate


# Full test of prep_for_simulations where we don't have entries for the curr_date.year and it fails during prep
def test_prep_future_ytd_failure_test(input_simulator_builder, simulator_input_df, mocker):
	# setup
	mocker.patch('SimulationCalcClass.get_input_dataframe', return_value=simulator_input_df)
	input_simulator_builder.curr_date = datetime(2023, 2, 15)
	input_simulator_builder.duration = 'YTD'
	# call function
	input_simulator_builder.prep_for_simulation()
	result_errors_found = input_simulator_builder.prep_errors_were_found()

	# set expectation
	expected_errors_found = True
	expected_error_msg_exists = False
	expected_error_list = input_simulator_builder.get_error_msgs()
	if expected_error_list.count('No entries found in historical date range') > 0:
		expected_error_msg_exists = True

	# assertion
	assert result_errors_found == expected_errors_found
	assert expected_error_msg_exists is True


# Full test of prep_for_simulations where we don't have entries after removing cancelled and not started entries
def test_prep_no_in_progress_after_cancelled_and_null_check(input_simulator_builder, simulator_input_not_started_df,
															mocker):
	# setup
	mocker.patch('SimulationCalcClass.get_input_dataframe', return_value=simulator_input_not_started_df)
	# call function
	input_simulator_builder.prep_for_simulation()
	result_errors_found = input_simulator_builder.prep_errors_were_found()

	# set expectation
	expected_errors_found = True
	expected_error_msg_exists = False
	expected_error_list = input_simulator_builder.get_error_msgs()
	if expected_error_list.count('No entries after removing cancelled and not-started entries') > 0:
		expected_error_msg_exists = True

	# assertion
	assert result_errors_found == expected_errors_found
	assert expected_error_msg_exists is True


# running the when and how many simulations
def test_run_monte_carlo_simulations(input_simulator_builder, dist_df_one_month, daily_entries_completed_mocked_list,
									 how_many_sim_output, when_sim_output, mocker):
	# setup
	mocker.patch('SimulationCalcClass.SimulationCalcClass.generate_random_daily_completed_list',
				 return_value=daily_entries_completed_mocked_list)
	# call function
	input_simulator_builder.run_monte_carlo_simulations(10, dist_df_one_month, 3, 30)
	result_how_many = input_simulator_builder.how_many_sim_output
	result_when = input_simulator_builder.when_sim_output
	# set expectation
	expected_how_many = how_many_sim_output
	expected_when = when_sim_output
	# assertion
	assert pd.testing.assert_frame_equal(result_how_many, expected_how_many) is None
	assert pd.testing.assert_frame_equal(result_when, expected_when) is None


# building the "how_many" percentiles dataframe
def test_build_how_many_percentile_dataframe(input_simulator_builder, how_many_sim_output, how_many_pct_df):
	# setup
	# call function
	result = input_simulator_builder.build_how_many_percentile_dataframe(how_many_sim_output)
	# set expectation
	expected = how_many_pct_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


# building the "when" percentiles dataframe
def test_build_when_percentile_dataframe(input_simulator_builder, when_sim_output, when_pct_df):
	# setup
	# call function
	result = input_simulator_builder.build_when_percentile_dataframe(when_sim_output)
	# set expectation
	expected = when_pct_df
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


# building the "how_many" percentiles dataframe
def test_log_run_stats(input_simulator_builder, when_sim_output, how_many_sim_output,
					   simulation_stats_one_month, final_sim_stats):
	# setup
	# call function
	result = input_simulator_builder.log_run_stats(when_sim_output, how_many_sim_output, simulation_stats_one_month)
	# set expectation
	expected = final_sim_stats
	# assertion
	assert pd.testing.assert_frame_equal(result, expected) is None


# full run of monte carlo simulations.
def test_run_mc_simulations(input_simulator_builder, simulator_input_df, full_daily_entries_completed_mocked_list,
							full_how_many_sim_output, full_when_sim_output, full_how_many_pct_df, full_when_pct_df,
							full_final_sim_stats, mocker):
	# setup
	num_iterations = 10
	mocker.patch('SimulationCalcClass.get_input_dataframe', return_value=simulator_input_df)
	mocked_list = mocker.patch('SimulationCalcClass.SimulationCalcClass.generate_random_daily_completed_list')
	mocked_list.side_effect = full_daily_entries_completed_mocked_list
	input_simulator_builder.prep_for_simulation()

	# call function
	input_simulator_builder.run_mc_simulations(num_iterations)
	result_errors_found = input_simulator_builder.calc_errors_were_found()
	result_how_many_output = input_simulator_builder.how_many_sim_output
	result_when_output = input_simulator_builder.when_sim_output
	result_how_many_pct = input_simulator_builder.how_many_percentiles
	result_when_pct = input_simulator_builder.when_percentiles
	result_sim_stats = input_simulator_builder.simulation_stats
	# set expectation
	expected_errors_found = False
	expected_how_many = full_how_many_sim_output
	expected_when = full_when_sim_output
	expected_how_many_pct = full_how_many_pct_df
	expected_when_pct = full_when_pct_df
	expected_sim_stats = full_final_sim_stats
	# assertion
	assert result_errors_found == expected_errors_found
	assert pd.testing.assert_frame_equal(result_how_many_output, expected_how_many) is None
	assert pd.testing.assert_frame_equal(result_when_output, expected_when) is None
	assert pd.testing.assert_frame_equal(result_how_many_pct, expected_how_many_pct) is None
	assert pd.testing.assert_frame_equal(result_when_pct, expected_when_pct) is None
	assert pd.testing.assert_frame_equal(result_sim_stats, expected_sim_stats) is None


"""
# Keeping this just so I remember how to snag from capsys if I need to see a print output
def test_capsys_output(capsys):
	print('testing an output')
	captured = capsys.readouterr()
	assert captured.out == 'testing an output'
	asser captured.err == ''
"""