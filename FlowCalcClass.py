import pandas as pd
import numpy as np
from datetime import datetime
import Globals


class FlowCalcClass:
	def __init__(self, start_col, end_col, start_sprint, end_sprint, wip_limit, item_names, categories, parent_toggle, parent_column):
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
		self.start_date = None
		self.end_date = None

		# find matching rows, get correct column as a series,
		# convert series to a ndarray of values, and select the first value (if it exists)
		start_row = Globals.SPRINT_INFO_DATAFRAME['SprintName'].values == start_sprint
		start_series = Globals.SPRINT_INFO_DATAFRAME[start_row]['StartDate'].values
		if start_series.size == 0:
			self.errors.append('No matching dates found for Start Sprint')
			self.prep_going_good = False
		else:
			self.start_date = pd.to_datetime(start_series[0])

		end_row = Globals.SPRINT_INFO_DATAFRAME['SprintName'].values == end_sprint
		end_series = Globals.SPRINT_INFO_DATAFRAME[end_row]['EndDate'].values
		if end_series.size == 0:
			self.errors.append('No matching dates found for End Sprint')
			self.prep_going_good = False
		else:
			self.end_date = pd.to_datetime(end_series[0])
		# ToDo: If end date is before start date, error out (as opposed to it abending)

		self.clean_df = None
		self.wip_df = None
		self.dates_df = None
		self.completed_items = None

	# =========================================
	# EXTERNALLY CALLED FUNCTIONS
	# =========================================
	def prep_for_metrics(self):
		if self.prep_going_good:
			self.build_clean_dataframe()
		if self.prep_going_good:
			self.build_wip_dataframe()
		if self.prep_going_good:
			self.build_dates_dataframe()
		if self.prep_going_good:
			self.build_throughput_run_dataframe()
		if self.prep_going_good & self.category_calc_toggle:
			self.prep_categories()
		if self.prep_going_good:
			self.final_values_preparation()
		if self.prep_going_good:
			Globals.GOOD_FOR_GO = True
		else:
			Globals.GLOBAL_ERROR_MSG = str(self.errors)

	def run_flow_metrics(self):
		avg_lead_time = self.calculate_average_lead_time()
		print('Done running Avg Lead Time')
		avg_throughput = self.calculate_average_throughput()
		print('Done running Avg Throughput')
		avg_wip = self.calculate_average_wip()
		print('Done running Avg WIP')
		wip_violations = self.calculate_wip_violations()
		print('Done running WIP Violations')
		flow_data = [[Globals.FLOW_METRIC_LEAD_TIME_KEY, avg_lead_time],
					 [Globals.FLOW_METRIC_WEEKLY_THROUGHPUT_KEY, avg_throughput],
					 [Globals.FLOW_METRIC_AVG_WIP_KEY, avg_wip],
					 [Globals.FLOW_METRIC_WIP_VIOLATIONS_KEY, wip_violations],
					 [Globals.FLOW_METRIC_WIP_VIOLATIONS_PCT_KEY,f'{round((wip_violations/self.number_of_days)*100, 2)}%']]
		Globals.FLOW_METRIC_RESULTS = pd.DataFrame(flow_data, columns=['Category', 'Value'])

		if self.calcs_going_good & self.category_calc_toggle:
			self.calculate_category_metrics()
			print('Done running category metrics')
		if self.parent_toggle:
			self.calculate_average_parent_wip()
			# TODO: Add print here once you build parent WIP calcs
			# print('Done running Avg Parent WIP')

	# This is a check for errors.
	# Return True if errors were found, False if there were no errors
	def errors_were_found(self):
		if self.prep_going_good:
			return False
		return True

	def get_error_msgs(self):
		return self.errors

	def get_completed_item_names(self):
		return self.completed_items

	# =========================================
	# ASSUMPTIONS
	# =========================================
	def get_flow_metric_assumptions(self):
		assumptions = [['Flow metrics are calculated on completed items only.'],
					   ['Date range is inclusive of start and end sprint.'],
					   ['"In Progress" is defined as an item which has started and has not completed by the end date.'],
					   ['Rounding could cause a trivial amount of difference in some of these calculations.']
					   ]
		if 'Cancelled' in Globals.INPUT_CSV_DATAFRAME:
			assumptions.append(['Cancelled items were excluded from calculations'])
		assumptions_df = pd.DataFrame(assumptions, columns=['Assumption'])
		return assumptions_df

	# =========================================
	# PREP FUNCTIONS
	# =========================================
	# Build dataframe with non-null dates in end-column and start-column (include all columns between those two)
	# Convert date columns to datetime elements.
	# Filter to only entries within the appropriate date range.
	# TODO: Add Parent Column to dataframe
	def build_clean_dataframe(self):
		base_df = Globals.INPUT_CSV_DATAFRAME
		# filter to only items which have not been cancelled
		if 'Cancelled' in base_df:
			cancelled_mask = base_df['Cancelled'] != 'Yes'
			base_df = base_df.loc[cancelled_mask]
		end_bool_series = pd.notnull(base_df[self.end_col])
		self.clean_df = base_df[end_bool_series]
		start_bool_series = pd.notnull(self.clean_df[self.start_col])
		self.clean_df = self.clean_df[start_bool_series]
		if self.clean_df is None:
			self.prep_going_good = False
			self.errors.append('Had no entries finish in this time frame')
			return

		# convert date columns to datetime elements.
		self.clean_df[self.start_col] = self.clean_df[self.start_col].apply(pd.to_datetime, errors='coerce')
		self.clean_df[self.end_col] = self.clean_df[self.end_col].apply(pd.to_datetime, errors='coerce')

		# return entries within the appropriate date range
		date_mask = (self.clean_df[self.end_col] >= self.start_date) & (
					self.clean_df[self.end_col] <= self.end_date)
		self.clean_df = self.clean_df.loc[date_mask]
		# Before we trim out to just the date fields, save off a df that can be displayed later
		self.completed_items = self.build_clean_completed_items_df(self.clean_df)
		# changed code to not gather all columns between start and end column.
		self.clean_df = self.clean_df.loc[:, [self.start_col, self.end_col, self.categories_column]]

		if len(self.clean_df.index) == 0:
			self.errors.append('No data to run flow metrics against. Select valid Sprint range')
			self.prep_going_good = False
			return

		self.prep_going_good = True

	def build_clean_completed_items_df(self, clean_df):
		temp_df = clean_df.loc[:, [self.item_names_column, self.start_col, self.end_col]]
		temp_df[self.start_col] = temp_df[self.start_col].astype(str)
		temp_df[self.end_col] = temp_df[self.end_col].astype(str)
		return temp_df
	# Build to only columns between start and end column
	# Use only items that started before the end date and are still in progress (null on end column or ended after period)
	# TODO: Add Parent Column to dataframe
	def build_wip_dataframe(self):
		base_df = Globals.INPUT_CSV_DATAFRAME
		# filter to only items which have not been cancelled
		if 'Cancelled' in base_df:
			cancelled_mask = base_df['Cancelled'] != 'Yes'
			base_df = base_df.loc[cancelled_mask]

		temp_df = base_df.loc[:, [self.start_col, self.end_col, self.categories_column]]
		temp_df = temp_df.apply(pd.to_datetime, errors='coerce')
		date_mask = (temp_df[self.start_col] <= self.end_date) & (temp_df[self.end_col].isnull()) | \
					((temp_df[self.start_col] <= self.end_date) & (temp_df[self.end_col] > self.end_date))
		self.wip_df = temp_df.loc[date_mask]

	# Build a dataframe for the dates within our range
	def build_dates_dataframe(self):
		rng = pd.date_range(self.start_date, self.end_date)
		self.dates_df = pd.DataFrame({'Date': rng, 'WIP': 0})
		self.prep_going_good = True

	# Build a Throughput_Run dataframe in the Globals file.
	def build_throughput_run_dataframe(self):
		rng = pd.date_range(self.start_date, self.end_date)
		temp_dates_df = pd.DataFrame({'Date': rng, 'Frequency': 0})
		date_counts = self.clean_df[self.end_col].value_counts()
		temp_df = pd.DataFrame(date_counts)
		temp_df = temp_df.reset_index()
		temp_df.columns = ('Date', 'Frequency')
		temp_df = pd.merge(left=temp_dates_df, right=temp_df, how='left', left_on='Date', right_on='Date')
		temp_df['Frequency_y'] = temp_df['Frequency_y'].fillna(0)
		temp_df = pd.DataFrame({'Date': temp_dates_df['Date'],
								'Frequency': temp_df['Frequency_x'] + temp_df['Frequency_y']})
		Globals.THROUGHPUT_RUN_DATAFRAME = temp_df
		self.prep_going_good = True

	# Build a Numpy Array of the categories in the main file.
	# Note that this may have categories outside of the selected date range, so when processing, make sure you check
	# for no values matching the category.
	def prep_categories(self):
		Globals.FLOW_METRIC_CATEGORY_RESULTS = pd.DataFrame(columns=[Globals.FLOW_METRIC_CATEGORY_KEY,
																	 Globals.FLOW_METRIC_CATEGORY_COUNT_KEY,
																	 Globals.FLOW_METRIC_LEAD_TIME_KEY,
																	 Globals.FLOW_METRIC_WEEKLY_THROUGHPUT_KEY])
		Globals.FLOW_METRIC_CATEGORIES = Globals.INPUT_CSV_DATAFRAME[self.categories_column].unique()
		if len(Globals.FLOW_METRIC_CATEGORIES) == 0:
			self.category_calc_toggle = False
			return
		self.prep_going_good = True

	# Any final value preparations that are helpful for future calculations
	def final_values_preparation(self):
		self.number_of_finished_items = len(self.clean_df)
		self.number_of_days = \
			(self.end_date - self.start_date) / np.timedelta64(1, 'D')
		stats_data = [[Globals.FLOW_METRIC_START_DATE_KEY, datetime.strftime(self.start_date, '%Y-%m-%d')],
					  [Globals.FLOW_METRIC_END_DATE_KEY, datetime.strftime(self.end_date, '%Y-%m-%d')],
					  [Globals.FLOW_METRIC_DAYS_KEY, self.number_of_days],
					  [Globals.FLOW_METRIC_COMPLETED_ITEMS_KEY, self.number_of_finished_items],
					  [Globals.FLOW_METRIC_IP_ITEMS_KEY, len(self.wip_df)]
		]
		Globals.FLOW_METRIC_STATS = pd.DataFrame(stats_data, columns=['Category', 'Value'])

	# =========================================
	# FLOW METRICS FUNCTIONS
	# =========================================
	# Find columns between the start and end date columns.
	# Calculate Cycle time from the start date to leaving each column (note the date in the columns is enter, not leave).
	def calculate_average_cycle_time(self):
		pass

	# Calculate the average time from start to end column.
	def calculate_average_lead_time(self):
		self.clean_df['lead_time'] = self.clean_df[self.end_col] - self.clean_df[self.start_col]
		self.clean_df['lead_time'] = self.clean_df['lead_time'] / np.timedelta64(1, 'D')
		self.calcs_going_good = True
		return round(self.clean_df['lead_time'].sum() / self.number_of_finished_items, 2)

	# Calculate the average number of items completed per week
	# Count how many items finished, divide by number of days in period, then multiply by 7 (days)
	def calculate_average_throughput(self):
		self.calcs_going_good = True
		return round((self.number_of_finished_items / self.number_of_days) * 7, 2)

	# Calculate the daily average wip for each column and as a whole system.
	# Check the clean_df for completed items, then the wip_df for in progress items.
	def calculate_average_wip(self):
		self.dates_df['WIP'] = self.dates_df.apply(lambda row: self.calc_wip_on_date(row, False), axis=1)
		self.calcs_going_good = True
		return round(self.dates_df['WIP'].sum()/len(self.dates_df), 2)

	# With the WIP limit known, calculate how many days were over that WIP limit
	def calculate_wip_violations(self):
		self.calcs_going_good = True
		matching_entries = self.dates_df['WIP'] > self.daily_wip_limit
		return len(self.dates_df.loc[matching_entries])

	# call function with np array of the categories
	# once completed, add the work mix type to the Dataframe
	def calculate_category_metrics(self):
		category_function = np.frompyfunc(self.calc_category_details, 1, 0)
		category_function(Globals.FLOW_METRIC_CATEGORIES)
		number_completed = Globals.FLOW_METRIC_CATEGORY_RESULTS[Globals.FLOW_METRIC_CATEGORY_COUNT_KEY].sum()
		Globals.FLOW_METRIC_CATEGORY_RESULTS[Globals.FLOW_METRIC_WORK_MIX_KEY] = \
			(Globals.FLOW_METRIC_CATEGORY_RESULTS[Globals.FLOW_METRIC_CATEGORY_COUNT_KEY] / number_completed).astype(float)
		Globals.FLOW_METRIC_CATEGORY_RESULTS[Globals.FLOW_METRIC_WORK_MIX_KEY] *= 100
		Globals.FLOW_METRIC_CATEGORY_RESULTS = \
			Globals.FLOW_METRIC_CATEGORY_RESULTS.round({f'{Globals.FLOW_METRIC_WORK_MIX_KEY}': 2})

	# Get unique list of parent items
	# Find the min start date for each parent item and the max end date (or end of period)
	# cycle through dates_df to see how many parents were IP each day
	def calculate_average_parent_wip(self):
		pass

	# Calculate the duration of all items within the historical range (that have completed)
	# Calculate the standard quantiles for historical duration
	# Calculate the age of each In Progress item.
	# Use WIP data set, not clean dataset.
	# Output:
	# 	Build a Dataframe for each column between start and finish
	# 	Items currently in progress have their age and ID put in the column in which they currently reside.
	def calculate_aging_wip(self):
		pass

	# =========================================
	# INTERNAL FUNCTIONS
	# =========================================
	def calc_wip_on_date(self, row, calculate_categories):
		found_completed_rows = (self.clean_df[self.start_col] <= row['Date']) & (self.clean_df[self.end_col] > row['Date'])
		temp_df = self.clean_df.loc[found_completed_rows]
		found_ip_rows = (self.wip_df[self.start_col] <= row['Date'])
		temp_df_2 = self.wip_df.loc[found_ip_rows]
		total_wip = len(temp_df) + len(temp_df_2)
		return total_wip

	def calc_category_details(self, category):
		matching_clean_entries = self.clean_df[self.categories_column] == category
		temp_clean_df = self.clean_df.loc[matching_clean_entries]
		category_count = len(temp_clean_df)
		if category_count > 0:
			avg_lead_time = round(temp_clean_df['lead_time'].sum() / category_count, 2)
			avg_throughput = round((category_count / self.number_of_days) * 7, 2)
			Globals.FLOW_METRIC_CATEGORY_RESULTS = \
				Globals.FLOW_METRIC_CATEGORY_RESULTS.append({Globals.FLOW_METRIC_CATEGORY_KEY: category,
															 Globals.FLOW_METRIC_CATEGORY_COUNT_KEY: category_count,
															 Globals.FLOW_METRIC_LEAD_TIME_KEY: avg_lead_time,
															 Globals.FLOW_METRIC_WEEKLY_THROUGHPUT_KEY: avg_throughput},
															ignore_index=True)
