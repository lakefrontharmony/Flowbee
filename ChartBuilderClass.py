import pandas as pd
import numpy as np
import Globals
from datetime import datetime, date, timedelta


class ChartBuilderClass:
	def __init__(self, st_col, end_col, name_col, chart_st, wip_limit):
		self.start_date = chart_st
		self.start_col = st_col
		self.end_col = end_col
		self.name_col = str(name_col).replace(' ', '')
		self.chart_start = datetime.strptime(chart_st, '%Y-%m-%d')
		self.wip_limit = wip_limit

		self.prep_going_good = True
		self.charts_going_good = True
		self.clean_df = None
		self.dates_df = None
		self.cfd_df = None
		self.aging_wip_df = None
		self.run_df = None
		self.throughput_hist_df = None
		self.cycle_time_hist_df = None
		self.cycle_time_scatter_df = None
		self.date_col_names = []
		self.errors = []

	# =========================================
	# EXTERNALLY CALLED FUNCTIONS
	# =========================================
	def prep_for_charting(self):
		self.build_clean_df()
		if self.prep_going_good:
			self.build_dates_df()
		if self.prep_going_good:
			Globals.GOOD_FOR_GO = True
		else:
			Globals.GOOD_FOR_GO = False

	def build_charts(self):
		self.build_cfd_df()
		self.build_aging_wip_df()
		self.build_run_df()
		self.build_throughput_histogram_df()
		self.build_cycle_time_histogram_df()
		if self.charts_going_good:
			self.build_cycle_time_scatter_df()
		if self.charts_going_good:
			Globals.CHARTS_BUILT_SUCCESSFULLY = True
		else:
			Globals.CHARTS_BUILT_SUCCESSFULLY = False

	def get_cfd_df(self):
		return self.cfd_df

	def get_date_column_list(self):
		return self.date_col_names

	def get_aging_wip_df(self):
		return self.aging_wip_df

	def get_run_df(self):
		return self.run_df

	def melt_cfd_df_for_charting(self):
		return_df = self.cfd_df.melt(id_vars='Date', value_vars=self.date_col_names)
		return return_df

	def get_throughput_hist_df(self):
		return self.throughput_hist_df

	def get_cycle_time_hist_df(self):
		return self.cycle_time_hist_df

	def get_cycle_time_scatter_df(self):
		return self.cycle_time_scatter_df

	def get_errors(self):
		return self.errors

	# =========================================
	# ASSUMPTIONS
	# =========================================
	def get_assumptions(self):
		assumptions = [['Phases of your flow were sequential columns between the specified start/end columns.'],
					   ['Flow phase columns only contained valid dates and there were no gaps between dates.']]
		if 'Cancelled' in Globals.INPUT_CSV_DATAFRAME:
			assumptions.append(['Cancelled items were excluded from calculations.'])
		else:
			assumptions.append(['No cancelled column was found. (Column must be titled "Cancelled."'])
		assumptions_df = pd.DataFrame(assumptions, columns=['Assumption'])
		return assumptions_df

	# =========================================
	# PREP FUNCTIONS
	# =========================================
	# Build dataframe with non-null dates in end-column and start-column (include all columns between those two)
	# Convert date columns to datetime elements.
	def build_clean_df(self):
		self.clean_df = Globals.INPUT_CSV_DATAFRAME

		# filter to only items which have not been cancelled and items which have at least reached your start column
		if 'Cancelled' in self.clean_df:
			cancelled_mask = self.clean_df['Cancelled'] != 'Yes'
			self.clean_df = self.clean_df.loc[cancelled_mask]

		start_bool_series = pd.notnull(self.clean_df[self.start_col])
		self.clean_df = self.clean_df[start_bool_series]

		if self.clean_df is None:
			self.prep_going_good = False
			self.errors.append('No in-progress data to chart from the input set. '
							   'Verify there are valid dates in input file')
			return

		# convert date columns to datetime elements
		self.clean_df.loc[:, self.start_col:self.end_col] = \
			self.clean_df.loc[:, self.start_col:self.end_col].apply(pd.to_datetime, errors='coerce')
		# TODO: Add in a search with 'isnull()' to find any rows that may have invalid or missing dates.
		test_df = self.clean_df.loc[:, self.start_col: self.end_col]
		test_df.columns = \
			[f'{i}_{x}' for i, x in enumerate(test_df.columns, 1)]
		self.start_col = test_df.columns[0]
		self.end_col = test_df.columns[-1]
		self.clean_df = pd.concat([self.clean_df.loc[:, self.name_col].to_frame(),
								   test_df], axis=1)
		self.clean_df['WIPLimit'] = self.wip_limit

		self.date_col_names = self.clean_df.loc[:, self.start_col: self.end_col].columns.tolist()
		self.prep_going_good = True

	def build_dates_df(self):
		min_date = min(self.clean_df[self.start_col])
		rng = pd.date_range(min_date, datetime.today())
		self.dates_df = pd.DataFrame({'Date': rng, 'WIP': 0, 'Throughput': 0, 'Avg Cycle Time': 0})

	# =========================================
	# CHARTING FUNCTIONS
	# =========================================
	# Take the dates from the dates_df and build a new dataframe with the num of items that have entered each column
	# for each day.
	def build_cfd_df(self):
		self.cfd_df = pd.DataFrame({'Date': self.dates_df['Date']})
		self.cfd_df.set_index('Date')
		for col_name in self.date_col_names:
			self.cfd_df[col_name] = self.cfd_df.apply(lambda row: self.calc_completed_on_date(row, col_name), axis=1)
		self.charts_going_good = True

	# TODO: Can we rework this to not use 'for' loops?
	# TODO: Make items still in a current state (column) be the duration since today?
	# TODO: add column for average cycle time of completed items
	def build_aging_wip_df(self):
		self.aging_wip_df = pd.DataFrame({'Name': self.clean_df[self.name_col], 'Age': 0, 'Status': '', 'Done_Date': pd.NaT})

		for col_name in self.date_col_names:
			self.aging_wip_df[col_name] = 0
			status_mask = pd.notnull(self.clean_df[col_name])
			self.aging_wip_df['Status'].loc[status_mask] = col_name
		prev_column = self.end_col
		self.aging_wip_df[self.start_col] = 0

		for col_name in reversed(self.date_col_names):
			self.aging_wip_df[col_name] = (self.clean_df[prev_column] - self.clean_df[col_name]).dt.days
			self.aging_wip_df[col_name] = self.aging_wip_df[col_name].fillna(0)
			self.aging_wip_df['Age'] += self.aging_wip_df[col_name]
			prev_column = col_name
		done_mask = pd.notnull(self.clean_df[self.end_col])
		self.aging_wip_df['Done_Date'].loc[done_mask] = self.clean_df[self.end_col].loc[done_mask]

		self.charts_going_good = True

	def build_run_df(self):
		self.run_df = pd.DataFrame({'Date': self.dates_df['Date']})
		self.run_df['WIP'] = self.run_df.apply(lambda row: self.calc_in_progress_on_date(row), axis=1)
		# TODO: Review the SimulationCalcClass to see how I did this without cycling through each row before.
		self.run_df['Throughput'] = self.run_df.apply(lambda row: self.calc_throughput_on_date(row), axis=1)
		self.run_df['WIPLimit'] = self.wip_limit
		self.charts_going_good = True

	def build_throughput_histogram_df(self):
		value_counts = self.run_df['Throughput'].value_counts()
		self.throughput_hist_df = pd.DataFrame(value_counts)
		self.throughput_hist_df.reset_index(inplace=True)
		self.throughput_hist_df.rename(columns={'Throughput': 'Count', 'index': 'Throughput'}, inplace=True)

	def build_cycle_time_histogram_df(self):
		completed_mask = self.aging_wip_df['Status'] == self.end_col
		completed_items = self.aging_wip_df.loc[completed_mask].copy()
		age_counts = completed_items['Age'].value_counts()
		self.cycle_time_hist_df = pd.DataFrame(age_counts)
		self.cycle_time_hist_df.reset_index(inplace=True)
		self.cycle_time_hist_df.rename(columns={'Age': 'Count', 'index': 'Age'}, inplace=True)

	def build_cycle_time_scatter_df(self):
		completed_mask = self.aging_wip_df['Status'] == self.end_col
		self.cycle_time_scatter_df = self.aging_wip_df.loc[completed_mask].copy()

	# =========================================
	# INTERNAL FUNCTIONS
	# =========================================
	def calc_completed_on_date(self, row, in_col_name):
		found_matching_rows = self.clean_df[in_col_name] <= row['Date']
		return len(self.clean_df[found_matching_rows].index)

	def calc_in_progress_on_date(self, in_row):
		test_date = in_row['Date']
		date_mask = (self.clean_df[self.start_col] <= test_date) & (self.clean_df[self.end_col].isnull()) | \
					((self.clean_df[self.start_col] <= test_date) & (self.clean_df[self.end_col] > test_date))
		return len(self.clean_df.loc[date_mask].index)

	def calc_throughput_on_date(self, in_row):
		test_date = in_row['Date']
		date_mask = (self.clean_df[self.end_col] == test_date)
		return len(self.clean_df.loc[date_mask].index)