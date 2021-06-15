import pandas as pd
import numpy as np
import Globals
from datetime import datetime, date, timedelta


class SimulationCalcClass:
	def __init__(self, duration, st_col, end_col, sim_st, sim_end, num_to_complete):
		self.start_date = date.today()
		self.end_date = date.today()
		self.duration = duration
		self.start_col = str(st_col).replace(' ', '')
		self.end_col = str(end_col).replace(' ', '')
		self.sim_start = datetime.strptime(sim_st, '%Y-%m-%d')
		self.sim_end = datetime.strptime(sim_end, '%Y-%m-%d')
		if num_to_complete == 0:
			self.finishing_all_ip_items = True
			Globals.NUM_ITEMS_TO_SIMULATE = self.calc_current_num_items_in_progress()
		else:
			self.finishing_all_ip_items = False
			Globals.NUM_ITEMS_TO_SIMULATE = num_to_complete
		self.clean_df = None
		self.dates_df = None
		self.dist_df = None
		self.max_entries_per_day = 0
		self.days_of_simulation = 0
		self.prep_going_good = True
		self.sims_going_good = True
		self.generator = np.random.default_rng()

	# =========================================
	# EXTERNALLY CALLED FUNCTIONS
	# =========================================
	def prep_for_simulation(self):
		self.prep_dataframe_formatting()
		self.determine_hist_date_range()
		if self.prep_going_good:
			self.build_clean_dataframe()
		if self.prep_going_good:
			self.build_dates_dataframe()
		if self.prep_going_good:
			self.build_dist_dataframe()
		if self.prep_going_good:
			self.final_field_preparation()
		if self.prep_going_good:
			Globals.GOOD_FOR_GO = True

	# TODO: Build in Error Handling through simulations
	def run_mc_simulations(self, iterations):
		Globals.SIMULATIONS_SUCCESSFUL = False
		self.run_monte_carlo_simulations(iterations)
		if self.sims_going_good:
			self.build_how_many_percentile_dataframe()
		if self.sims_going_good:
			self.build_when_percentile_dataframe()
		if self.sims_going_good:
			self.log_run_stats()
		if self.sims_going_good:
			Globals.SIMULATIONS_SUCCESSFUL = True

	# =========================================
	# ASSUMPTIONS
	# =========================================
	def get_monte_carlo_assumptions(self):
		assumptions = [['Simulation is built using throughput of completed items only (not in progress items)'],
					   ['Assumes that the historical throughput will be consistent with future throughput'],
					   ['Date range is inclusive of start and end date']
					   ]

		duration_value = Globals.HIST_TIMEFRAME[self.duration]
		if duration_value == Globals.HIST_TIMEFRAME['Last Calendar Year']:
			assumptions.append(['Historical duration was one calc\'d as last year'])
		elif duration_value == Globals.HIST_TIMEFRAME['YTD']:
			assumptions.append(['Historical duration was calc\'d as 01/01 of this year to today'])
		elif duration_value.isnumeric():
			assumptions.append(['Historical duration was calc\'d back from the max end column date of the CSV file'])

		if 'Cancelled' in Globals.INPUT_CSV_DATAFRAME:
			assumptions.append(['Cancelled items were excluded from calculations'])
		if self.finishing_all_ip_items:
			assumptions.append(['Current IP items are ones that started before today\'s date and have not finished'])

		return pd.DataFrame(assumptions, columns=['Assumption'])

	# =========================================
	# PREP FOR MONTE CARLO SIMULATION FUNCTIONS
	# =========================================
	# Build dataframe with non-null dates in end-column and start-column.
	# filter to only items which have not been cancelled
	def prep_dataframe_formatting(self):
		base_df = Globals.INPUT_CSV_DATAFRAME
		if 'Cancelled' in base_df:
			cancelled_mask = base_df['Cancelled'] != 'Yes'
			base_df = base_df.loc[cancelled_mask]
		end_bool_series = pd.notnull(base_df[self.end_col])
		self.clean_df = base_df[end_bool_series]
		start_bool_series = pd.notnull(self.clean_df[self.start_col])
		self.clean_df = self.clean_df[start_bool_series]

		# convert date columns to datetime elements.
		self.clean_df[self.start_col] = pd.to_datetime(self.clean_df[self.start_col])
		self.clean_df[self.end_col] = pd.to_datetime(self.clean_df[self.end_col])

	# Use the duration to look back in time for appropriate time frame.
	# If duration is for weeks or months, calc based on months back from the last date in the file.
	# If duration is for a date range (i.e. YTD or last year), it will use the current date, or calc specific dates.
	def determine_hist_date_range(self):
		first_file_date = self.clean_df[self.end_col].min()
		duration_value = Globals.HIST_TIMEFRAME[self.duration]
		if duration_value == Globals.HIST_TIMEFRAME['Last Calendar Year']:
			last_year = date.today().year - 1
			self.start_date =  date(year=last_year,
								   month=1,
								   day=1)
			self.start_date = pd.to_datetime(self.start_date)
			if self.start_date < first_file_date:
				self.start_date = first_file_date
			self.end_date = date(year=last_year,
								 month=12,
								 day=31)
			self.end_date = pd.to_datetime(self.end_date)
			return
		elif duration_value == Globals.HIST_TIMEFRAME['YTD']:
			self.start_date = date(year=date.today().year,
								   month=1,
								   day=1)
			self.start_date = pd.to_datetime(self.start_date)
			self.start_date = max(self.start_date, first_file_date)
			self.end_date = datetime.today()
			return
		elif duration_value.isnumeric():
			self.end_date = self.clean_df[self.end_col].max()
			self.start_date = self.end_date - timedelta(days=int(duration_value))
			self.start_date = pd.to_datetime(self.start_date)
			self.start_date = max(self.start_date, first_file_date)
			return
		self.prep_going_good = False
		self.report_error('Unexpected duration of simulation received')

	# Build a clean dataframe with only appropriate entries for calculations
	# TODO: Error Handling
	def build_clean_dataframe(self):
		# return entries within the appropriate date range
		date_mask = (self.clean_df[self.end_col] >= self.start_date) & (self.clean_df[self.end_col] <= self.end_date)
		self.clean_df = self.clean_df.loc[date_mask]
		self.clean_df = self.clean_df[[self.start_col, self.end_col]].copy()

	# Build a dataframe with one row for each date within range
	# TODO: Error Handling
	def build_dates_dataframe(self):
		rng = pd.date_range(self.start_date, self.end_date)
		self.dates_df = pd.DataFrame({'Date': rng, 'Frequency': 0})

	# Build a dataframe with percentages for each possible outcome on any given day.
	# This serves as an input curve to a random number selector
	# TODO: Error Handling
	def build_dist_dataframe(self):
		# Get a unique list of dates in the end column, and their frequency counts.
		date_counts = self.clean_df[self.end_col].value_counts()
		temp_df = pd.DataFrame(date_counts)
		temp_df = temp_df.reset_index()
		temp_df.columns = ('Date', 'Frequency')

		# merge the full list of dates in this period
		# and the unique list of dates we actually finished items to one dataframe
		temp_df = pd.merge(left=self.dates_df, right=temp_df, how='left', left_on='Date', right_on='Date')
		temp_df['Frequency_y'] = temp_df['Frequency_y'].fillna(0)
		temp_df = pd.DataFrame({'Date': self.dates_df['Date'],
								'Frequency': temp_df['Frequency_x'] + temp_df['Frequency_y']})
		date_freq = temp_df['Frequency'].value_counts(normalize=True)
		temp_dist_df = pd.DataFrame(date_freq)
		temp_dist_df = temp_dist_df.reset_index()
		temp_dist_df.columns = ('Count', 'Frequency')

		# Build a dataframe of counts between 0 and the max number of completed items (+1 since it's a zero-based list)
		# use this to build the final dist_df which will have the actual frequencies of completion, and zeroes for any
		# numbers in between. This was added on because if you completed 1, 2, and 10 items, future calcs were looking
		# for a list of frequencies based on 0 - 10 (not a list of 3 frequencies representing 1, 2, and 10)
		blank_comp_df = pd.DataFrame({'Count': np.arange(0, temp_dist_df['Count'].max()+1, 1), 'Frequency': 0})
		self.dist_df = pd.merge(left=blank_comp_df, right=temp_dist_df, how='left', left_on='Count', right_on='Count')
		self.dist_df = pd.DataFrame({'Count': self.dist_df['Count'],
									 'Frequency': self.dist_df['Frequency_x'] + self.dist_df['Frequency_y']})
		self.dist_df['Frequency'] = self.dist_df['Frequency'].fillna(0)

	# Any global fields that are helpful to have frequently during simulations.
	# Also building a general stats df for later reference
	def final_field_preparation(self):
		self.max_entries_per_day = int(self.dist_df['Count'].max())
		self.days_of_simulation = (self.sim_end - self.sim_start).days
		self.days_of_simulation += 1  # include the start date (which date math was not doing)

		self.number_of_finished_items = len(self.clean_df)
		self.number_of_days = \
			(self.end_date - self.start_date) / np.timedelta64(1, 'D')
		self.number_of_days += 1  # include the start date (which date math was not doing)
		stats_data = [[Globals.MC_HIST_DATE_RANGE_KEY, f"{datetime.strftime(self.start_date, '%Y-%m-%d')} - {datetime.strftime(self.end_date, '%Y-%m-%d')}"],
					  [Globals.SIM_DATE_RANGE_KEY, f"{datetime.strftime(self.sim_start, '%Y-%m-%d')} - {datetime.strftime(self.sim_end, '%Y-%m-%d')}"],
					  [Globals.NUMBER_OF_SIM_DAYS_KEY, self.days_of_simulation],
					  [Globals.NUMBER_OF_ITEMS_KEY, Globals.NUM_ITEMS_TO_SIMULATE],
					  [Globals.MAX_ENTRIES_PER_DAY_KEY, self.max_entries_per_day]
					  ]
		Globals.MC_SIMULATION_STATS = pd.DataFrame(stats_data, columns=['Category', 'Value'])

	# Number of items in progress is defined as anything that started before today in the start column,
	# and has not ended.
	def calc_current_num_items_in_progress(self):
		base_df = Globals.INPUT_CSV_DATAFRAME
		# filter to only items which have not been cancelled
		if 'Cancelled' in base_df:
			cancelled_mask = base_df['Cancelled'] != 'Yes'
			base_df = base_df.loc[cancelled_mask]
		temp_df = base_df.loc[:, self.start_col: self.end_col]
		temp_df = temp_df.apply(pd.to_datetime, errors='coerce')
		date_mask = (temp_df[self.start_col] <= np.datetime64('Today')) & (temp_df[self.end_col].isnull())
		return len(temp_df[date_mask])

	# =========================================
	# MONTE CARLO SIMULATION FUNCTIONS
	# =========================================
	def run_monte_carlo_simulations(self, iterations):
		how_many_output_array = np.zeros([0, 1])
		when_output_array = np.zeros([0, 1])
		prob_dist = self.dist_df['Frequency'].tolist()
		simulation_days = int(Globals.NUM_ITEMS_TO_SIMULATE * 20)
		for i in range(iterations):
			# How Many
			daily_entries_completed_list = self.generator.choice(self.max_entries_per_day+1, simulation_days, p=prob_dist)
			how_many_completed_list = daily_entries_completed_list[:self.days_of_simulation]
			how_many_output_array = np.append(how_many_output_array, int(sum(how_many_completed_list)))

			# When
			num_of_days = (np.cumsum(daily_entries_completed_list) < Globals.NUM_ITEMS_TO_SIMULATE).argmin()
			if num_of_days == 0:
				print('reached the end of the random array before finding date of completion')
				self.sims_going_good = False
				break
			when_output_array = np.append(when_output_array, num_of_days)

		Globals.HOW_MANY_SIM_OUTPUT = pd.DataFrame(how_many_output_array, columns=['Output'])
		Globals.WHEN_SIM_OUTPUT = pd.DataFrame(when_output_array, columns=['Output'])

	def build_how_many_percentile_dataframe(self):
		calc_percentiles = 1 - Globals.PERCENTILES_LIST
		Globals.HOW_MANY_PERCENTILES = Globals.HOW_MANY_SIM_OUTPUT.quantile(calc_percentiles)
		Globals.HOW_MANY_PERCENTILES.rename(columns={'Output': 'Count_Percentiles'}, inplace=True)
		Globals.HOW_MANY_PERCENTILES.index = Globals.PERCENTILES_LIST

	def build_when_percentile_dataframe(self):
		Globals.WHEN_PERCENTILES = Globals.WHEN_SIM_OUTPUT.quantile(Globals.PERCENTILES_LIST)
		Globals.WHEN_PERCENTILES.rename(columns={'Output': 'Days_Percentiles'}, inplace=True)
		Globals.WHEN_PERCENTILES['End_date'] = Globals.WHEN_PERCENTILES['Days_Percentiles']
		Globals.WHEN_PERCENTILES['End_date'] = \
			Globals.WHEN_PERCENTILES['End_date'].apply(lambda duration: self.sim_start + timedelta(days=duration))
		Globals.WHEN_PERCENTILES['End_date'] = Globals.WHEN_PERCENTILES['End_date'].dt.strftime('%Y-%m-%d')

	# Append to the General Stats df with run stats.
	def log_run_stats(self):
		avg_days_to_completion = round(sum(Globals.WHEN_SIM_OUTPUT['Output']) / len(Globals.WHEN_SIM_OUTPUT['Output']), 0)
		avg_completion_date = self.sim_start + timedelta(days=avg_days_to_completion)
		avg_completion_date = avg_completion_date.strftime('%Y-%m-%d')

		mode_days_to_completion = Globals.WHEN_SIM_OUTPUT.mode()['Output'][0]
		mode_completion_date = self.sim_start + timedelta(days=mode_days_to_completion)
		mode_completion_date = mode_completion_date.strftime('%Y-%m-%d')
		stats_data = [[Globals.MC_AVG_NUM_COMPLETED_KEY,
					   f'{int(sum(Globals.HOW_MANY_SIM_OUTPUT["Output"]) / len(Globals.HOW_MANY_SIM_OUTPUT["Output"]))} items'],
					  [Globals.MC_MODE_NUM_COMPLETED_KEY, f'{int(Globals.HOW_MANY_SIM_OUTPUT.mode()["Output"][0])} items'],
					  [Globals.MC_AVG_DAYS_TO_COMPLETE_KEY, avg_completion_date],
					  [Globals.MC_MODE_DAYS_TO_COMPLETE_KEY, mode_completion_date]
					  ]
		new_data = pd.DataFrame(stats_data, columns=['Category', 'Value'])
		Globals.MC_SIMULATION_STATS = Globals.MC_SIMULATION_STATS.append(new_data, ignore_index=True)
		# Globals.MC_SIMULATION_STATS

	# =========================================
	# ERROR HANDLING
	# =========================================
	def report_error(self, error_msg):
		Globals.GOOD_FOR_GO = False
		Globals.GLOBAL_ERROR_MSG = error_msg
