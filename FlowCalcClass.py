import pandas as pd
import numpy as np
from datetime import datetime
import Globals


class FlowCalcClass:
	def __init__(self, start_col, end_col, start_date, end_date,
				 wip_limit, item_names, categories, parent_toggle, parent_column):
		self.prep_going_good = True
		self.calcs_going_good = True
		self.errors = []
		self.number_of_finished_items = 0
		self.number_of_days = 0
		self.daily_wip_limit = wip_limit
		self.item_names_column = item_names
		self.categories_column = categories
		self.category_calc_toggle = False if self.categories_column == '' else True
		self.parent_toggle = parent_toggle
		self.parent_column = parent_column

		self.start_col = start_col
		self.end_col = end_col
		# self.start_date = start_date
		# self.end_date = end_date
		self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
		self.end_date = datetime.strptime(end_date, '%Y-%m-%d')

		self.clean_df = None
		self.wip_df = None
		self.dates_df = None
		self.completed_items = None
		self.flow_metric_categories = []
		self.flow_metric_stats = pd.DataFrame()
		self.flow_metric_results = pd.DataFrame()
		self.flow_metric_category_results = pd.DataFrame()

	# =========================================
	# EXTERNALLY CALLED FUNCTIONS
	# =========================================
	def prep_for_metrics(self):
		# self.start_date = self.find_matching_sprint_date(get_sprint_dataframe(), self.start_date, 'StartDate')
		# self.end_date = self.find_matching_sprint_date(get_sprint_dataframe(), self.end_date, 'EndDate')
		if self.prep_going_good:
			self.clean_df = self.build_clean_dataframe(get_flow_dataframe())
		if self.prep_going_good:
			self.wip_df = self.build_wip_dataframe(get_flow_dataframe(), self.end_date)
		if self.prep_going_good:
			self.dates_df = self.build_dates_dataframe(self.start_date, self.end_date)
		if self.prep_going_good & self.category_calc_toggle:
			self.flow_metric_categories = self.prep_categories(self.clean_df)
		if self.prep_going_good:
			self.flow_metric_stats = self.final_values_preparation(self.start_date, self.end_date,
																   self.clean_df, self.wip_df)
		if self.prep_going_good:
			Globals.GOOD_FOR_GO = True
		else:
			Globals.GLOBAL_ERROR_MSG = str(self.errors)

	def run_flow_metrics(self):
		avg_lead_time = self.calculate_average_lead_time(self.clean_df, self.number_of_finished_items)
		avg_throughput = self.calculate_average_throughput(self.number_of_finished_items, self.number_of_days)
		avg_wip = self.calculate_average_wip(self.dates_df, self.clean_df, self.wip_df)
		wip_violations = self.calculate_wip_violations(self.dates_df)
		flow_data = [[Globals.FLOW_METRIC_LEAD_TIME_KEY, avg_lead_time],
					 [Globals.FLOW_METRIC_WEEKLY_THROUGHPUT_KEY, avg_throughput],
					 [Globals.FLOW_METRIC_AVG_WIP_KEY, avg_wip],
					 [Globals.FLOW_METRIC_WIP_VIOLATIONS_KEY, wip_violations],
					 [Globals.FLOW_METRIC_WIP_VIOLATIONS_PCT_KEY,f'{round((wip_violations/self.number_of_days)*100, 2)}%']]
		self.flow_metric_results = pd.DataFrame(flow_data, columns=['Category', 'Value'])

		if self.calcs_going_good & self.category_calc_toggle:
			self.flow_metric_category_results = self.calculate_category_metrics(self.flow_metric_categories,
																				self.clean_df, self.number_of_days)
		if self.parent_toggle:
			self.calculate_average_parent_wip()

	# This is a check for errors.
	# Return True if errors were found, False if there were no errors
	def prep_errors_were_found(self) -> bool:
		if self.prep_going_good:  # pragma: no cover
			return False  # pragma: no cover
		return True  # pragma: no cover

	def calc_errors_were_found(self) -> bool:
		if self.calcs_going_good:  # pragma: no cover
			return False  # pragma: no cover
		return True  # pragma: no cover

	def get_error_msgs(self) -> list:
		return self.errors  # pragma: no cover

	def get_completed_item_names(self) -> pd.DataFrame:
		return self.completed_items  # pragma: no cover

	def get_flow_metric_stats(self) -> pd.DataFrame:
		return self.flow_metric_stats  # pragma: no cover

	def get_flow_metric_results(self) -> pd.DataFrame:
		return self.flow_metric_results  # pragma: no cover

	def get_flow_metric_category_results(self) -> pd.DataFrame:
		return self.flow_metric_category_results  # pragma: no cover

	# =========================================
	# ASSUMPTIONS
	# =========================================
	def get_flow_metric_assumptions(self):
		assumptions = [['Flow metrics are calculated on completed items only.'],  # pragma: no cover
					   ['Date range is inclusive of start and end sprint.'],  # pragma: no cover
					   ['"In Progress" is defined as an item which has started and has not completed by the end date.'],  # pragma: no cover
					   ['Rounding could cause a trivial amount of difference in some of these calculations.']  # pragma: no cover
					   ]  # pragma: no cover
		if 'Cancelled' in get_flow_dataframe():  # pragma: no cover
			assumptions.append(['Cancelled items were excluded from calculations'])  # pragma: no cover
		assumptions_df = pd.DataFrame(assumptions, columns=['Assumption'])  # pragma: no cover
		return assumptions_df  # pragma: no cover

	# =========================================
	# PREP FUNCTIONS
	# =========================================
	# find matching rows, get correct column as a series,
	# convert series to a ndarray of values, and select the first value (if it exists)
	def find_matching_sprint_date(self, in_df, sprint_name, target_column):
		return_date = None
		found_row = in_df['SprintName'].values == sprint_name
		found_series = in_df[found_row][target_column].values
		if found_series.size == 0:
			self.errors.append(f'No matching dates found for {sprint_name} in the {target_column} column')
			self.prep_going_good = False
		else:
			return_date = pd.to_datetime(found_series[0])
		return return_date

	# Build dataframe with non-null dates in end-column and start-column (include all columns between those two)
	# Convert date columns to datetime elements.
	# Filter to only entries within the appropriate date range.
	# TODO: Add Parent Column to dataframe
	def build_clean_dataframe(self, in_df) -> pd.DataFrame:
		return_df = in_df.copy()
		# filter to only items which have not been cancelled
		return_df = self.remove_cancelled_rows(return_df)

		end_bool_series = pd.notnull(return_df[self.end_col])
		return_df = return_df[end_bool_series]

		end_bool_series = return_df[self.end_col].ne('')
		return_df = return_df.loc[end_bool_series]

		start_bool_series = pd.notnull(return_df[self.start_col])
		return_df = return_df[start_bool_series]

		start_bool_series = return_df[self.start_col].ne('')
		return_df = return_df.loc[start_bool_series]

		if return_df is None:
			self.prep_going_good = False
			self.errors.append('Had no entries finish in this time frame')
			# return an empty dataframe
			return pd.DataFrame()

		# convert date columns to datetime elements.
		return_df[self.start_col] = return_df[self.start_col].apply(pd.to_datetime, errors='coerce')
		return_df[self.end_col] = return_df[self.end_col].apply(pd.to_datetime, errors='coerce')

		# return entries within the appropriate date range
		date_mask = (return_df[self.end_col] >= self.start_date) & (
					return_df[self.end_col] <= self.end_date)
		return_df = return_df.loc[date_mask]
		# Before we trim out to just the date fields, save off a df that can be displayed later
		self.completed_items = self.save_clean_completed_items_df(return_df)
		# changed code to not gather all columns between start and end column.
		return_df = return_df.loc[:, [self.start_col, self.end_col, self.categories_column]]

		if len(return_df.index) == 0:
			self.errors.append('No data to run flow metrics against. Select valid Sprint range')
			self.prep_going_good = False
			# return an empty dataframe
			return pd.DataFrame()

		self.prep_going_good = True
		return_df.reset_index(drop=True, inplace=True)
		return return_df

	def remove_cancelled_rows(self, in_df: pd.DataFrame) -> pd.DataFrame:
		return_df = in_df.copy()
		if 'Cancelled' in return_df:
			cancelled_mask = (return_df['Cancelled'] != 'Yes') & (return_df['Cancelled'] != 'Cancelled')
			return_df = return_df.loc[cancelled_mask]
			return_df.reset_index(drop=True, inplace=True)
		elif 'Status' in return_df:
			cancelled_mask = (return_df['Status'] != 'Yes') & (return_df['Status'] != 'Cancelled')
			return_df = return_df.loc[cancelled_mask]
			return_df.reset_index(drop=True, inplace=True)
		return return_df

	def save_clean_completed_items_df(self, clean_df: pd.DataFrame) -> pd.DataFrame:
		temp_df = clean_df.loc[:, [self.item_names_column, self.start_col, self.end_col]]
		temp_df[self.start_col] = temp_df[self.start_col].astype(str)
		temp_df[self.end_col] = temp_df[self.end_col].astype(str)
		return temp_df

	# Build to only columns between start and end column
	# Use only items that started before the end date and are still in progress (null on end column or ended after period)
	# TODO: Add Parent Column to dataframe
	def build_wip_dataframe(self, in_df: pd.DataFrame, in_end_date: datetime) -> pd.DataFrame:
		# filter to only items which have not been cancelled
		return_df = self.remove_cancelled_rows(in_df)

		temp_df = return_df.loc[:, [self.start_col, self.end_col, self.categories_column]]
		temp_df[self.start_col] = temp_df[self.start_col].apply(pd.to_datetime, errors='coerce')
		temp_df[self.end_col] = temp_df[self.end_col].apply(pd.to_datetime, errors='coerce')
		date_mask = (temp_df[self.start_col] <= in_end_date) & (temp_df[self.end_col].isnull()) | \
					((temp_df[self.start_col] <= in_end_date) & (temp_df[self.end_col] > in_end_date))
		return_df = temp_df.loc[date_mask]
		return_df.reset_index(drop=True, inplace=True)

		return return_df

	# Build a dataframe for the dates within our range
	def build_dates_dataframe(self, in_start_date: datetime, in_end_date: datetime) -> pd.DataFrame:
		rng = pd.date_range(in_start_date, in_end_date)
		self.prep_going_good = True
		return pd.DataFrame({'Date': rng, 'WIP': 0})

	# Build a Numpy Array of the categories in the main file.
	# Note that this may have categories outside of the selected date range, so when processing, make sure you check
	# for no values matching the category.
	def prep_categories(self, flow_array: pd.DataFrame) -> np.array:
		flow_metric_categories = flow_array[self.categories_column].unique()
		if len(flow_metric_categories) == 0:
			self.category_calc_toggle = False
		self.prep_going_good = True
		return flow_metric_categories

	# Any final value preparations that are helpful for future calculations
	def final_values_preparation(self, start_date: datetime.date, end_date: datetime.date,
								 clean_df: pd.DataFrame, wip_df: pd.DataFrame) -> pd.DataFrame:
		self.number_of_finished_items = len(clean_df)
		self.number_of_days = \
			((np.datetime64(end_date) - np.datetime64(start_date)) / np.timedelta64(1, 'D')) + 1
			# ((end_date - start_date) / np.timedelta64(1, 'D')) + 1
		stats_data = [[Globals.FLOW_METRIC_START_DATE_KEY, datetime.strftime(start_date, '%Y-%m-%d')],
					  [Globals.FLOW_METRIC_END_DATE_KEY, datetime.strftime(end_date, '%Y-%m-%d')],
					  [Globals.FLOW_METRIC_DAYS_KEY, int(self.number_of_days)],
					  [Globals.FLOW_METRIC_COMPLETED_ITEMS_KEY, self.number_of_finished_items],
					  [Globals.FLOW_METRIC_IP_ITEMS_KEY, len(wip_df)]
		]
		return pd.DataFrame(stats_data, columns=['Category', 'Value'])

	# =========================================
	# FLOW METRICS FUNCTIONS
	# =========================================
	# Find columns between the start and end date columns.
	# Calculate Cycle time from the start date to leaving each column (note the date in the columns is enter, not leave).
	def calculate_average_cycle_time(self):
		pass  # pragma: no cover

	# Calculate the average time from start to end column.
	def calculate_average_lead_time(self, clean_df: pd.DataFrame, number_of_finished_items) -> np.float64:
		clean_df['lead_time'] = clean_df[self.end_col] - clean_df[self.start_col]
		clean_df['lead_time'] = clean_df['lead_time'] / np.timedelta64(1, 'D')
		self.calcs_going_good = True
		return round(clean_df['lead_time'].sum() / number_of_finished_items, 2)

	# Calculate the average number of items completed per week
	# Count how many items finished, divide by number of days in period, then multiply by 7 (days)
	def calculate_average_throughput(self, num_finished_items, num_days) -> np.float64:
		self.calcs_going_good = True
		return round((num_finished_items / num_days) * 7, 2)

	# Calculate the daily average wip for each column and as a whole system.
	# Check the clean_df for completed items, then the wip_df for in progress items.
	def calculate_average_wip(self, dates_df: pd.DataFrame, clean_df: pd.DataFrame, wip_df: pd.DataFrame):
		dates_df['WIP'] = dates_df.apply(lambda row: self.calc_wip_on_date(row, clean_df, wip_df), axis=1)
		self.calcs_going_good = True
		return round(dates_df['WIP'].sum()/len(dates_df), 2)

	# With the WIP limit known, calculate how many days were over that WIP limit
	def calculate_wip_violations(self, dates_df):
		self.calcs_going_good = True
		matching_entries = dates_df['WIP'] > self.daily_wip_limit
		return len(dates_df.loc[matching_entries])

	# call function with np array of the categories
	# once completed, add the work mix type to the Dataframe
	def calculate_category_metrics(self, in_categories: np.array,
								   clean_df: pd.DataFrame, number_of_days: int) -> pd.DataFrame:
		flow_metric_category_results = pd.DataFrame(columns=[Globals.FLOW_METRIC_CATEGORY_KEY,
																	 Globals.FLOW_METRIC_CATEGORY_COUNT_KEY,
																	 Globals.FLOW_METRIC_LEAD_TIME_KEY,
																	 Globals.FLOW_METRIC_WEEKLY_THROUGHPUT_KEY])
		category_series = np.empty((0, 4))
		for category in in_categories:
			category_results = self.calc_category_details(category, clean_df, number_of_days)
			if category_results.size > 0:
				category_series = np.append(category_series, [category_results], axis=0)
		flow_metric_category_results = pd.DataFrame(category_series, columns=[Globals.FLOW_METRIC_CATEGORY_KEY,
																	 Globals.FLOW_METRIC_CATEGORY_COUNT_KEY,
																	 Globals.FLOW_METRIC_LEAD_TIME_KEY,
																	 Globals.FLOW_METRIC_WEEKLY_THROUGHPUT_KEY])
		# cast the columns to explicit types as they start off as "object" types
		flow_metric_category_results[Globals.FLOW_METRIC_CATEGORY_KEY] = \
			flow_metric_category_results[Globals.FLOW_METRIC_CATEGORY_KEY].astype(str)
		flow_metric_category_results[Globals.FLOW_METRIC_CATEGORY_COUNT_KEY] = \
			flow_metric_category_results[Globals.FLOW_METRIC_CATEGORY_COUNT_KEY].astype(int)
		flow_metric_category_results[Globals.FLOW_METRIC_LEAD_TIME_KEY] = \
			flow_metric_category_results[Globals.FLOW_METRIC_LEAD_TIME_KEY].astype(float)
		flow_metric_category_results[Globals.FLOW_METRIC_WEEKLY_THROUGHPUT_KEY] = \
			flow_metric_category_results[Globals.FLOW_METRIC_WEEKLY_THROUGHPUT_KEY].astype(float)

		number_completed = flow_metric_category_results[Globals.FLOW_METRIC_CATEGORY_COUNT_KEY].sum()
		flow_metric_category_results[Globals.FLOW_METRIC_WORK_MIX_KEY] = \
			(flow_metric_category_results[Globals.FLOW_METRIC_CATEGORY_COUNT_KEY] / number_completed).astype(float)
		flow_metric_category_results[Globals.FLOW_METRIC_WORK_MIX_KEY] *= 100
		flow_metric_category_results[Globals.FLOW_METRIC_WORK_MIX_KEY] = \
			flow_metric_category_results[Globals.FLOW_METRIC_WORK_MIX_KEY].round(decimals=2)
		return flow_metric_category_results

	# Get unique list of parent items
	# Find the min start date for each parent item and the max end date (or end of period)
	# cycle through dates_df to see how many parents were IP each day
	def calculate_average_parent_wip(self):
		pass  # pragma: no cover

	# Calculate the duration of all items within the historical range (that have completed)
	# Calculate the standard quantiles for historical duration
	# Calculate the age of each In Progress item.
	# Use WIP data set, not clean dataset.
	# Output:
	# 	Build a Dataframe for each column between start and finish
	# 	Items currently in progress have their age and ID put in the column in which they currently reside.
	def calculate_aging_wip(self):
		pass  # pragma: no cover

	# =========================================
	# INTERNAL FUNCTIONS
	# =========================================
	def calc_wip_on_date(self, row, clean_df, wip_df, calculate_categories=False):
		found_completed_rows = (clean_df[self.start_col] <= row['Date']) & (clean_df[self.end_col] > row['Date'])
		temp_df = clean_df.loc[found_completed_rows]
		found_ip_rows = (wip_df[self.start_col] <= row['Date'])
		temp_df_2 = wip_df.loc[found_ip_rows]
		total_wip = len(temp_df) + len(temp_df_2)
		return total_wip

	def calc_category_details(self, category: str, clean_df: pd.DataFrame, number_of_days: int) -> np.array:
		matching_clean_entries = clean_df[self.categories_column] == category
		temp_clean_df = clean_df.loc[matching_clean_entries]
		category_count = len(temp_clean_df)
		if category_count == 0:
			return np.array([])
		avg_lead_time = round(temp_clean_df['lead_time'].sum() / category_count, 2)
		avg_throughput = round((category_count / number_of_days) * 7, 2)
		return_array = np.array([category, category_count, avg_lead_time, avg_throughput])
		return return_array


def get_sprint_dataframe() -> pd.DataFrame:
	return Globals.SPRINT_INFO_DATAFRAME  # pragma: no cover


def get_flow_dataframe() -> pd.DataFrame:
	return Globals.INPUT_CSV_DATAFRAME  # pragma: no cover
