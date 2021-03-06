import pandas as pd
import numpy as np
import Globals
from datetime import datetime, timedelta


class SimulationCalcClass:
	def __init__(self, duration, st_col, end_col, sim_st, sim_end, num_to_complete, curr_date):
		self.start_date = curr_date
		self.end_date = curr_date
		self.duration = duration
		self.start_col = str(st_col).replace(' ', '')
		self.end_col = str(end_col).replace(' ', '')
		self.sim_start = datetime.strptime(sim_st, '%Y-%m-%d')
		self.sim_end = datetime.strptime(sim_end, '%Y-%m-%d')
		self.num_items_to_simulate = num_to_complete
		self.finishing_all_ip_items = False
		self.curr_date = curr_date

		self.clean_df = None
		self.dates_df = None
		self.dist_df = None
		self.display_dist_df = None
		self.throughput_run_df = None
		self.simulation_stats = None
		self.how_many_sim_output = None
		self.when_sim_output = None
		self.how_many_percentiles = None
		self.when_percentiles = None
		self.max_entries_per_day = 0
		self.days_of_simulation = 0
		self.prep_going_good = True
		self.sims_going_good = True
		self.generator = np.random.default_rng()
		self.errors = []
		self.cancelled_items_removed = False

	# =========================================
	# EXTERNALLY CALLED FUNCTIONS
	# =========================================
	def prep_for_simulation(self):
		if self.num_items_to_simulate == 0:
			self.finishing_all_ip_items = True
			self.num_items_to_simulate = self.calc_current_num_items_in_progress(get_input_dataframe())
		if self.prep_going_good:
			self.clean_df = self.prep_dataframe_formatting(get_input_dataframe())
		if self.prep_going_good:
			self.determine_hist_date_range(self.clean_df)
		if self.prep_going_good:
			self.clean_df = self.build_clean_dataframe(self.clean_df)
		if self.prep_going_good:
			self.dates_df = self.build_dates_dataframe()
		if self.prep_going_good:
			self.dist_df = self.build_dist_dataframe(self.clean_df, self.dates_df)
		if self.prep_going_good:
			self.final_field_preparation(self.dist_df, self.clean_df)

	# TODO: Build in Error Handling through simulations
	def run_mc_simulations(self, iterations):
		self.run_monte_carlo_simulations(iterations, self.dist_df, self.max_entries_per_day, self.days_of_simulation)
		if self.sims_going_good:
			self.how_many_percentiles = self.build_how_many_percentile_dataframe(self.how_many_sim_output)
		if self.sims_going_good:
			self.when_percentiles = self.build_when_percentile_dataframe(self.when_sim_output)
		if self.sims_going_good:
			self.simulation_stats = self.log_run_stats(self.when_sim_output, self.how_many_sim_output,
													   self.simulation_stats)

	def prep_errors_were_found(self) -> bool:  # pragma: no cover
		if self.prep_going_good:  # pragma: no cover
			return False  # pragma: no cover
		else:  # pragma: no cover
			return True  # pragma: no cover

	def calc_errors_were_found(self) -> bool:  # pragma: no cover
		if self.sims_going_good:  # pragma: no cover
			return False  # pragma: no cover
		else:  # pragma: no cover
			return True  # pragma: no cover

	def get_error_msgs(self) -> list:  # pragma: no cover
		return self.errors  # pragma: no cover

	def get_num_items_to_simulate(self) -> int:  # pragma: no cover
		return self.num_items_to_simulate  # pragma: no cover

	def get_display_dist_df(self) -> pd.DataFrame:  # pragma: no cover
		return self.display_dist_df  # pragma: no cover

	def get_simulation_stats(self) -> pd.DataFrame:  # pragma: no cover
		return self.simulation_stats  # pragma: no cover

	def get_simulation_start_date(self) -> datetime:  # pragma: no cover
		return self.sim_start  # pragma: no cover

	def get_how_many_sim_output(self) -> pd.DataFrame:  # pragma: no cover
		return self.how_many_sim_output  # pragma: no cover

	def get_when_sim_output(self) -> pd.DataFrame:  # pragma: no cover
		return self.when_sim_output  # pragma: no cover

	def get_how_many_percentiles(self) -> pd.DataFrame:  # pragma: no cover
		return self.how_many_percentiles  # pragma: no cover

	def get_when_percentiles(self) -> pd.DataFrame:  # pragma: no cover
		return self.when_percentiles  # pragma: no cover

	def get_throughput_run(self) -> pd.DataFrame:  # pragma: no cover
		return self.throughput_run_df  # pragma: no cover

	# =========================================
	# ASSUMPTIONS
	# =========================================
	def get_monte_carlo_assumptions(self):  # pragma: no cover
		assumptions = [['Simulation is built using throughput of completed items only (not in progress items)'],  # pragma: no cover
					   ['Assumes that the historical throughput will be consistent with future throughput'],  # pragma: no cover
					   ['Date range is inclusive of start and end date']  # pragma: no cover
					   ]  # pragma: no cover

		duration_value = Globals.HIST_TIMEFRAME[self.duration]  # pragma: no cover
		if duration_value == Globals.HIST_TIMEFRAME['Last Calendar Year']:  # pragma: no cover
			assumptions.append(['Historical duration was one calc\'d as last year'])  # pragma: no cover
		elif duration_value == Globals.HIST_TIMEFRAME['YTD']:  # pragma: no cover
			assumptions.append(['Historical duration was calc\'d as 01/01 of this year to today'])  # pragma: no cover
		elif duration_value.isnumeric():  # pragma: no cover
			assumptions.append(['Historical duration was calc\'d back from the max end column date of the CSV file'])  # pragma: no cover

		if self.cancelled_items_removed:  # pragma: no cover
			assumptions.append(['Cancelled items were excluded from calculations'])  # pragma: no cover
		if self.finishing_all_ip_items:  # pragma: no cover
			assumptions.append(['Current IP items are ones that started before today\'s date and have not finished'])  # pragma: no cover

		return pd.DataFrame(assumptions, columns=['Assumption'])

	# =========================================
	# PREP FOR MONTE CARLO SIMULATION FUNCTIONS
	# =========================================
	# Build dataframe with non-null dates in end-column and start-column.
	# filter to only items which have not been cancelled
	def prep_dataframe_formatting(self, in_df: pd.DataFrame) -> pd.DataFrame:
		return_df = self.remove_cancelled_rows(in_df)

		# since the date columns have not been converted to dates yet, it was not seeing an empty string as null.
		end_bool_series = return_df[self.end_col].ne('')
		return_df = return_df.loc[end_bool_series]
		start_bool_series = return_df[self.start_col].ne('')
		return_df = return_df.loc[start_bool_series]

		if return_df.empty:
			self.report_error('No entries after removing cancelled and not-started entries')
			# return an empty dataframe
			return pd.DataFrame()

		# convert date columns to datetime elements.
		return_df.loc[:, self.start_col] = pd.to_datetime(return_df[self.start_col])
		return_df.loc[:, self.end_col] = pd.to_datetime(return_df[self.end_col])

		return_df.reset_index(drop=True, inplace=True)
		self.prep_going_good = True
		return return_df

	def remove_cancelled_rows(self, in_df: pd.DataFrame) -> pd.DataFrame:
		return_df = in_df.copy()
		if 'Cancelled' in return_df:
			cancelled_mask = (return_df['Cancelled'] != 'Yes') & (return_df['Cancelled'] != 'Cancelled')
			return_df = return_df.loc[cancelled_mask]
			return_df.reset_index(drop=True, inplace=True)
			self.cancelled_items_removed = True
		elif 'Resolution' in return_df:
			cancelled_mask = (return_df['Resolution'] != 'Yes') & (return_df['Resolution'] != 'Cancelled')
			return_df = return_df.loc[cancelled_mask]
			return_df.reset_index(drop=True, inplace=True)
			self.cancelled_items_removed = True
		return return_df

	# Use the duration to look back in time for appropriate time frame.
	# If duration is for weeks or months, calc based on months back from the last date in the file.
	# If duration is for a date range (i.e. YTD or last year), it will use the current date, or calc specific dates.
	def determine_hist_date_range(self, in_clean_df: pd.DataFrame):
		first_file_date = in_clean_df[self.end_col].min()
		duration_value = 'Null'
		if self.duration in Globals.HIST_TIMEFRAME.keys():
			duration_value = Globals.HIST_TIMEFRAME[self.duration]
		if duration_value == Globals.HIST_TIMEFRAME['Last Calendar Year']:
			last_year = self.curr_date.year - 1
			self.start_date = datetime(year=last_year,
								   month=1,
								   day=1)
			if self.start_date < first_file_date:
				self.start_date = first_file_date
			self.end_date = datetime(year=last_year,
								 month=12,
								 day=31)
			return
		elif duration_value == Globals.HIST_TIMEFRAME['YTD']:
			self.start_date = datetime(year=self.curr_date.year,
								   month=1,
								   day=1)
			self.start_date = max(self.start_date, first_file_date)
			self.end_date = self.curr_date
			return
		elif duration_value.isnumeric():
			self.end_date = in_clean_df[self.end_col].max()
			self.start_date = self.end_date - timedelta(days=int(duration_value))
			self.start_date = pd.to_datetime(self.start_date)
			self.start_date = max(self.start_date, first_file_date)
			return
		self.report_error('Unexpected duration of simulation received')

	# Build a clean dataframe with only appropriate entries for calculations
	def build_clean_dataframe(self, in_clean_df: pd.DataFrame) -> pd.DataFrame:
		# return entries within the appropriate date range
		return_df = in_clean_df.copy()
		date_mask = (return_df[self.end_col] >= self.start_date) & (return_df[self.end_col] <= self.end_date)
		return_df = return_df.loc[date_mask]

		if return_df.empty:
			self.report_error('No entries found in historical date range')
			# return an empty dataframe
			return pd.DataFrame()

		return_df = return_df[[self.start_col, self.end_col]]
		return_df.reset_index(drop=True, inplace=True)
		self.prep_going_good = True
		return return_df

	# Build a dataframe with one row for each date within range
	def build_dates_dataframe(self) -> pd.DataFrame:
		rng = pd.date_range(self.start_date, self.end_date)
		return pd.DataFrame({'Date': rng, 'Frequency': 0})

	# Build a dataframe with percentages for each possible outcome on any given day.
	# This serves as an input curve to a random number selector
	def build_dist_dataframe(self, in_clean_df: pd.DataFrame, in_dates_df: pd.DataFrame) -> pd.DataFrame:
		# Get a unique list of dates in the end column, and their frequency counts.
		date_counts = in_clean_df[self.end_col].value_counts()
		temp_df = pd.DataFrame(date_counts)
		temp_df = temp_df.reset_index()
		temp_df.columns = ('Date', 'Frequency')

		# merge the full list of dates in this period
		# and the unique list of dates we actually finished items to one dataframe
		# Save off the results for each day to 'self.throughput_run_dataframe' so that
		# we can reference that after simulations are complete.
		temp_df = pd.merge(left=in_dates_df, right=temp_df, how='left', left_on='Date', right_on='Date')
		temp_df['Frequency_y'] = temp_df['Frequency_y'].fillna(0)
		temp_df = pd.DataFrame({'Date': in_dates_df['Date'],
								'Frequency': temp_df['Frequency_x'] + temp_df['Frequency_y']})
		self.throughput_run_df = temp_df
		date_freq = temp_df['Frequency'].value_counts(normalize=True)
		temp_dist_df = pd.DataFrame(date_freq)
		temp_dist_df = temp_dist_df.reset_index()
		temp_dist_df.columns = ('Count', 'Frequency')

		# Build a dataframe of counts between 0 and the max number of completed items (+1 since it's a zero-based list)
		# use this to build the final dist_df which will have the actual frequencies of completion, and zeroes for any
		# numbers in between. This was added on because if you completed 1, 2, and 10 items, future calcs were looking
		# for a list of frequencies based on 0 - 10 (not a list of 3 frequencies representing 1, 2, and 10)
		blank_comp_df = pd.DataFrame({'Count': np.arange(0, temp_dist_df['Count'].max()+1, 1), 'Frequency': 0})
		return_df = pd.merge(left=blank_comp_df, right=temp_dist_df, how='left', left_on='Count', right_on='Count')
		return_df = pd.DataFrame({'Count': return_df['Count'],
									 'Frequency': return_df['Frequency_x'] + return_df['Frequency_y']})
		return_df['Frequency'] = return_df['Frequency'].fillna(0)
		return return_df

	# Any global fields that are helpful to have frequently during simulations.
	# Also building a general stats df for later reference
	def final_field_preparation(self, in_dist_df: pd.DataFrame, in_clean_df: pd.DataFrame):
		self.display_dist_df = self.build_display_percentiles_df(in_dist_df)

		self.max_entries_per_day = int(in_dist_df['Count'].max())
		self.days_of_simulation = (self.sim_end - self.sim_start).days
		self.days_of_simulation += 1  # include the start date (which date math was not doing)

		self.number_of_finished_items = len(in_clean_df)
		self.number_of_days = (self.end_date - self.start_date).days
		self.number_of_days += 1  # include the start date (which date math was not doing)

		stats_data = [[Globals.MC_HIST_DATE_RANGE_KEY, f"{datetime.strftime(self.start_date, '%Y-%m-%d')} - "
													   f"{datetime.strftime(self.end_date, '%Y-%m-%d')}"],
					  [Globals.SIM_DATE_RANGE_KEY, f"{datetime.strftime(self.sim_start, '%Y-%m-%d')} - "
												   f"{datetime.strftime(self.sim_end, '%Y-%m-%d')}"],
					  [Globals.NUMBER_OF_SIM_DAYS_KEY, f'{self.days_of_simulation}'],
					  [Globals.NUMBER_OF_ITEMS_KEY, f'{self.num_items_to_simulate}'],
					  [Globals.MAX_ENTRIES_PER_DAY_KEY, f'{self.max_entries_per_day}']
					  ]
		self.simulation_stats = pd.DataFrame(stats_data, columns=['Category', 'Value'])

	def build_display_percentiles_df(self, in_dist_df: pd.DataFrame) -> pd.DataFrame:
		return_df = in_dist_df.copy()
		pct_list = (return_df['Frequency'] * 100).round(2)
		pct_list = pct_list.astype(str) + '%'
		return_df['Frequency'] = pct_list
		return return_df

	# Number of items in progress is defined as anything that started before today in the start column,
	# and has not ended.
	def calc_current_num_items_in_progress(self, in_df: pd.DataFrame):
		base_df = self.remove_cancelled_rows(in_df)
		start_bool_series = base_df[self.start_col].ne('')
		base_df = base_df.loc[start_bool_series]

		base_df = base_df.loc[:, self.start_col: self.end_col]
		base_df = base_df.apply(pd.to_datetime, errors='coerce')
		date_mask = ((base_df[self.start_col] <= self.curr_date) & (base_df[self.end_col].isnull())) | \
					((base_df[self.start_col] <= self.curr_date) & (base_df[self.end_col] > self.curr_date))
		return len(base_df[date_mask])

	# =========================================
	# MONTE CARLO SIMULATION FUNCTIONS
	# =========================================
	def run_monte_carlo_simulations(self, iterations: int, in_dist_df: pd.DataFrame, in_max_per_day: int, in_days_of_sim: int):
		how_many_output_array = np.zeros([0, 1])
		when_output_array = np.zeros([0, 1])
		prob_dist = in_dist_df['Frequency'].tolist()
		simulation_days = int(self.num_items_to_simulate * 20)
		for i in range(iterations):
			# How Many
			daily_entries_completed_list = self.generate_random_daily_completed_list(in_max_per_day, simulation_days, prob_dist)
			# daily_entries_completed_list = self.generator.choice(in_max_per_day+1, simulation_days, p=prob_dist)
			how_many_completed_list = daily_entries_completed_list[:in_days_of_sim]
			how_many_output_array = np.append(how_many_output_array, int(sum(how_many_completed_list)))

			# When
			# A bug popped up for when the number of items completed in the first day of the simulation was larger than
			# the number to simulate, num_of_days was getting set to 0 and triggering the same condition as if the
			# cumsum was never able to complete before hitting the end of the array. Added a default of 1 day and check
			# to verify that the first day is smaller than the num of items to simulate before doing cumsum.
			num_of_days = 1
			if daily_entries_completed_list[0] < self.num_items_to_simulate:
				# add one to this number because the index is zero based and we want to know the count of the location
				num_of_days = (np.cumsum(daily_entries_completed_list) < self.num_items_to_simulate).argmin() + 1
			if num_of_days == 0:
				self.report_error(f'Could not calculate the number of days to complete {self.num_items_to_simulate}')
				break
			when_output_array = np.append(when_output_array, num_of_days)

		self.how_many_sim_output = pd.DataFrame(how_many_output_array, columns=['Output'])
		self.when_sim_output = pd.DataFrame(when_output_array, columns=['Output'])

	def generate_random_daily_completed_list(self, in_max_per_day: int, simulation_days: int, prob_dist: list):  # pragma: no cover
		return self.generator.choice(in_max_per_day+1, simulation_days, p=prob_dist)  # pragma: no cover

	def build_how_many_percentile_dataframe(self, in_how_many_sim_output: pd.DataFrame) -> pd.DataFrame:
		calc_percentiles = 1 - Globals.PERCENTILES_LIST
		return_df = in_how_many_sim_output.quantile(calc_percentiles)
		return_df.rename(columns={'Output': 'Count_Percentiles'}, inplace=True)
		return_df.index = Globals.PERCENTILES_LIST
		return return_df

	def build_when_percentile_dataframe(self, in_when_sim_output: pd.DataFrame) -> pd.DataFrame:
		return_df = in_when_sim_output.quantile(Globals.PERCENTILES_LIST)
		return_df.rename(columns={'Output': 'Days_Percentiles'}, inplace=True)
		return_df['End_Date'] = return_df['Days_Percentiles']
		return_df['End_Date'] = \
			return_df['End_Date'].apply(lambda duration: self.sim_start + timedelta(days=duration))
		return_df['End_Date'] = return_df['End_Date'].dt.strftime('%Y-%m-%d')
		return return_df

	# Append to the General Stats df with run stats.
	def log_run_stats(self, in_when_sim_output: pd.DataFrame, in_how_many_sim_output: pd.DataFrame,
					  in_sim_stats: pd.DataFrame) -> pd.DataFrame:
		avg_days_to_completion = round(sum(in_when_sim_output['Output']) / len(in_when_sim_output['Output']), 0)
		avg_completion_date = self.sim_start + timedelta(days=avg_days_to_completion)
		avg_completion_date = avg_completion_date.strftime('%Y-%m-%d')

		mode_days_to_completion = in_when_sim_output.mode()['Output'][0]
		mode_completion_date = self.sim_start + timedelta(days=mode_days_to_completion)
		mode_completion_date = mode_completion_date.strftime('%Y-%m-%d')
		stats_data = [[Globals.MC_AVG_NUM_COMPLETED_KEY,
					   f'{int(sum(in_how_many_sim_output["Output"]) / len(in_how_many_sim_output["Output"]))} items'],
					  [Globals.MC_MODE_NUM_COMPLETED_KEY, f'{int(in_how_many_sim_output.mode()["Output"][0])} items'],
					  [Globals.MC_AVG_DAYS_TO_COMPLETE_KEY, avg_completion_date],
					  [Globals.MC_MODE_DAYS_TO_COMPLETE_KEY, mode_completion_date]
					  ]
		new_data = pd.DataFrame(stats_data, columns=['Category', 'Value'])
		return in_sim_stats.append(new_data, ignore_index=True)


	# =========================================
	# ERROR HANDLING
	# =========================================
	def report_error(self, error_msg):  # pragma: no cover
		self.prep_going_good = False  # pragma: no cover
		self.sims_going_good = False  # pragma: no cover
		self.errors.append(error_msg)  # pragma: no cover


def get_input_dataframe() -> pd.DataFrame:  # pragma: no cover
	return Globals.INPUT_CSV_DATAFRAME  # pragma: no cover
