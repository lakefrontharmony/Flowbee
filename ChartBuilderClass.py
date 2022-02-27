import pandas as pd
import Globals
from datetime import datetime, date


class ChartBuilderClass:
	def __init__(self, st_col, end_col, name_col, use_start_date, chart_st, end_date, wip_limit):
		self.start_date = datetime.strptime(chart_st, '%Y-%m-%d').date()
		self.start_col = st_col
		self.end_col = end_col
		self.name_col = str(name_col).replace(' ', '')
		self.use_start_date = use_start_date
		self.end_date = end_date
		self.wip_limit = wip_limit

		self.prep_going_good = True
		self.charts_going_good = True
		self.clean_df = None
		self.completed_items_df = None
		self.dates_df = None
		self.cfd_df = None
		self.cfd_vectors = None
		self.aging_wip_df = None
		self.run_df = None
		self.throughput_hist_df = None
		self.cycle_time_hist_df = None
		self.cycle_time_scatter_df = None
		self.date_col_names = []
		self.errors = []

		self.cycle_time_85_confidence = 0
		self.cycle_time_50_confidence = 0
		self.cycle_time_average = 0
		self.throughput_85_confidence = 0
		self.throughput_50_confidence = 0
		self.throughput_average = 0

	# =========================================
	# EXTERNALLY CALLED FUNCTIONS
	# =========================================
	def prep_for_charting(self):
		self.clean_df = self.build_clean_df(get_flow_dataframe())
		if self.prep_going_good & self.use_start_date:
			self.clean_df = self.filter_clean_df_to_start_date(self.clean_df)
		if self.prep_going_good:
			self.dates_df = self.build_dates_df(self.clean_df, self.end_date)
		if self.prep_going_good:
			self.completed_items_df = self.build_completed_df(self.clean_df)
		if self.prep_going_good:
			self.calc_completed_stats(self.completed_items_df, self.end_date)

	# This is a check for errors.
	# Return True if errors were found, False if there were no errors
	def prep_errors_were_found(self) -> bool:
		if self.prep_going_good:  # pragma: no cover
			return False  # pragma: no cover
		return True  # pragma: no cover

	def build_charts(self):
		self.cfd_df = self.build_cfd_df(self.dates_df, self.date_col_names, self.clean_df)
		self.cfd_vectors = self.build_cfd_vectors(self.date_col_names, self.cfd_df)
		self.aging_wip_df = self.build_aging_wip_df(self.clean_df, self.date_col_names, self.end_date)
		self.run_df = self.build_run_df(self.dates_df, self.clean_df)
		self.throughput_hist_df = self.build_throughput_histogram_df(self.run_df)
		self.cycle_time_hist_df = self.build_cycle_time_histogram_df(self.aging_wip_df)
		self.cycle_time_scatter_df = self.build_cycle_time_scatter_df(self.aging_wip_df)

	def build_errors_were_found(self) -> bool:
		if self.charts_going_good:
			return False
		return True

	def get_clean_df(self):  # pragma: no cover
		return self.clean_df  # pragma: no cover

	def get_cfd_df(self):  # pragma: no cover
		return_df = self.cfd_df.copy()  # pragma: no cover
		return_df['Date'] = return_df['Date'].dt.date  # pragma: no cover
		return return_df  # pragma: no cover

	# Unused for now
	def melt_cfd_df_for_charting(self):  # pragma: no cover
		return_df = self.cfd_df.melt(id_vars='Date', value_vars=self.date_col_names)  # pragma: no cover
		return return_df  # pragma: no cover

	def get_cfd_vectors(self):  # pragma: no cover
		return self.cfd_vectors  # pragma: no cover

	def get_date_column_list(self):  # pragma: no cover
		return self.date_col_names  # pragma: no cover

	def get_aging_wip_df(self):  # pragma: no cover
		return_df = self.aging_wip_df.copy()  # pragma: no cover
		return_df['Done_Date'] = return_df['Done_Date'].dt.date  # pragma: no cover
		return return_df  # pragma: no cover

	def get_run_df(self):  # pragma: no cover
		return_df = self.run_df.copy()  # pragma: no cover
		return_df['Date'] = return_df['Date'].dt.date  # pragma: no cover
		return return_df  # pragma: no cover

	def get_throughput_hist_df(self):  # pragma: no cover
		return self.throughput_hist_df  # pragma: no cover

	def get_cycle_time_hist_df(self):  # pragma: no cover
		return self.cycle_time_hist_df  # pragma: no cover

	def get_cycle_time_scatter_df(self):  # pragma: no cover
		return_df = self.cycle_time_scatter_df.copy()  # pragma: no cover
		return_df['Done_Date'] = return_df['Done_Date'].dt.date  # pragma: no cover
		return return_df  # pragma: no cover

	def get_errors(self):  # pragma: no cover
		return self.errors  # pragma: no cover

	# =========================================
	# ASSUMPTIONS
	# =========================================
	def get_assumptions(self):  # pragma: no cover
		assumptions = [['Phases of your flow were sequential columns between the specified start/end columns.'],  # pragma: no cover
					   ['Flow phase columns only contained valid dates.'],  # pragma: no cover
					   ['Any gaps in dates between phases were back-filled from the next valid date.']]  # pragma: no cover
		if ('Cancelled' in Globals.INPUT_CSV_DATAFRAME) | ('Status' in Globals.INPUT_CSV_DATAFRAME):  # pragma: no cover
			assumptions.append(['Cancelled items were excluded from calculations.'])  # pragma: no cover
		else:  # pragma: no cover
			assumptions.append(['No cancelled column was found. (Column must be titled "Cancelled" or "Status")'])  # pragma: no cover
		assumptions_df = pd.DataFrame(assumptions, columns=['Assumption'])  # pragma: no cover
		return assumptions_df  # pragma: no cover

	# =========================================
	# PREP FUNCTIONS
	# =========================================
	# Build dataframe with non-null dates in end-column and start-column (include all columns between those two)
	# Convert date columns to datetime elements.
	def build_clean_df(self, in_df: pd.DataFrame) -> pd.DataFrame:
		return_df = in_df.copy()
		# filter to only items which have not been cancelled
		return_df = self.remove_cancelled_rows(return_df)

		start_idx = return_df.columns.get_loc(self.start_col)
		end_idx = return_df.columns.get_loc(self.end_col)
		if start_idx >= end_idx:
			self.errors.append('The End Status column must be AFTER the Start Status column')
			self.prep_going_good = False
			return pd.DataFrame()

		start_bool_series = pd.notnull(return_df[self.start_col])
		return_df = return_df.loc[start_bool_series]
		# since the date columns have not been converted to dates yet, it was not seeing an empty string as null.
		# Added this statement in to get rid of things that have not yet reached the start column.
		start_bool_series = return_df[self.start_col].ne('')
		return_df = return_df.loc[start_bool_series]

		if return_df is None:
			self.errors.append('No in-progress data to chart from the input set. ' 
							   'Verify there are valid dates in input file')
			self.prep_going_good = False
			return pd.DataFrame()

		# convert date columns to date elements (NOT DATETIME)
		test_df = return_df.loc[:, self.start_col: self.end_col]
		test_df = test_df.loc[:, self.start_col: self.end_col].applymap(lambda x: pd.to_datetime(x, errors='coerce').date())

		length_check = test_df.dropna(subset=[self.start_col])
		if len(length_check.index) == 0:
			self.errors.append('There are no valid entries using this Start Status column')
			self.prep_going_good = False
			return pd.DataFrame()

		test_df = self.fillna_dates(test_df)
		test_df.columns = \
			[f'{i}_{x}' for i, x in enumerate(test_df.columns, 1)]
		self.start_col = test_df.columns[0]
		self.end_col = test_df.columns[-1]
		return_df = pd.concat([return_df.loc[:, self.name_col].to_frame(),
								   test_df], axis=1)
		return_df['WIPLimit'] = self.wip_limit

		self.date_col_names = return_df.loc[:, self.start_col: self.end_col].columns.tolist()

		# give a fresh index to the dataframe
		return_df.reset_index(drop=True, inplace=True)
		self.prep_going_good = True
		return return_df

	def remove_cancelled_rows(self, in_df: pd.DataFrame) -> pd.DataFrame:
		return_df = in_df.copy()
		if 'Cancelled' in return_df:
			cancelled_mask = (return_df['Cancelled'] != 'Yes') & (return_df['Cancelled'] != 'Cancelled')
			return_df = return_df.loc[cancelled_mask]
			return_df.reset_index(drop=True, inplace=True)
		elif 'Resolution' in return_df:
			cancelled_mask = (return_df['Resolution'] != 'Yes') & (return_df['Resolution'] != 'Cancelled')
			return_df = return_df.loc[cancelled_mask]
			return_df.reset_index(drop=True, inplace=True)
		return return_df

	def filter_clean_df_to_start_date(self, in_df: pd.DataFrame) -> pd.DataFrame:
		return_df = in_df.copy()
		include_mask = (pd.isnull(return_df[self.end_col])) | (return_df[self.end_col] >= self.start_date)
		return_df = return_df.loc[include_mask]
		# give a fresh index to the dataframe
		return_df.reset_index(drop=True, inplace=True)
		return return_df

	def build_dates_df(self, in_df: pd.DataFrame, end_date: datetime.date) -> pd.DataFrame:
		min_date = min(in_df[self.start_col])
		if self.use_start_date:
			min_date = self.start_date
		rng = pd.date_range(min_date, end_date)
		# NOTE: A range creates a datetime list and many of the other dataframes are storing dates.
		return_dates_df = pd.DataFrame({'Date': rng, 'WIP': 0, 'Throughput': 0, 'Avg Cycle Time': 0})
		self.prep_going_good = True
		return return_dates_df

	def build_completed_df(self, in_df: pd.DataFrame) -> pd.DataFrame:
		completed_mask = pd.notnull(in_df[self.end_col])
		completed_items_df = in_df.loc[completed_mask]
		self.prep_going_good = True
		return completed_items_df

	def calc_completed_stats(self, in_completed_items_df: pd.DataFrame, end_date: date):
		cycle_time_col = (in_completed_items_df[self.end_col] - in_completed_items_df[self.start_col]).dt.days
		self.cycle_time_85_confidence = cycle_time_col.quantile(0.85)
		self.cycle_time_50_confidence = cycle_time_col.quantile(0.50)
		self.cycle_time_average = round(sum(cycle_time_col) / cycle_time_col.count(), 2)

		throughput_count = in_completed_items_df[self.end_col].value_counts()
		self.throughput_85_confidence = throughput_count.quantile(0.85)
		self.throughput_50_confidence = throughput_count.quantile(0.50)
		num_days = (end_date - in_completed_items_df[self.end_col].min()).days
		self.throughput_average = round(sum(throughput_count) / num_days, 2)

		self.prep_going_good = True

	# =========================================
	# CHARTING FUNCTIONS
	# =========================================
	# Take the dates from the dates_df and build a new dataframe with the num of items that have entered each column
	# for each day.
	def build_cfd_df(self, in_dates_df: pd.DataFrame, in_col_names: list, in_clean_df: pd.DataFrame) -> pd.DataFrame:
		return_cfd_df = pd.DataFrame({'Date': in_dates_df['Date']})
		return_cfd_df.set_index('Date')
		for col_name in in_col_names:
			return_cfd_df[col_name] = return_cfd_df.apply(
				lambda row: self.calc_completed_on_date(row, col_name, in_clean_df), axis=1)
		self.charts_going_good = True
		return return_cfd_df

	def build_cfd_vectors(self, in_col_names: list, in_cfd_df: pd.DataFrame) -> pd.DataFrame:
		vector_array = []
		for col_name in in_col_names:
			start_location = in_cfd_df.loc[in_cfd_df[col_name] > 0].idxmin()
			start_date = in_cfd_df['Date'].loc[start_location[0]]
			start_count = in_cfd_df[col_name].loc[start_location[0]]
			end_date = in_cfd_df['Date'].iloc[-1]
			end_count = in_cfd_df[col_name].iloc[-1]
			vector_array.append([col_name, start_date, start_count])
			vector_array.append([col_name, end_date, end_count])

		return pd.DataFrame(vector_array, columns=['Status', 'Date', 'Count'])

	def build_aging_wip_df(self, in_clean_df: pd.DataFrame, in_date_col_names: list, end_date: date) -> pd.DataFrame:
		# Create a copy of clean_df and set all of the NaT dates to today's date
		# (this makes the date math work in the reverse cycle through the date_col_names list)
		temp_clean_df = in_clean_df.copy()
		temp_clean_df.fillna(end_date, inplace=True)
		return_aging_wip_df = pd.DataFrame({'Name': in_clean_df[self.name_col], 'Age': 0, 'Status': '',
										  'Start_Date': in_clean_df[self.start_col], 'Done_Date': pd.NaT})

		return_aging_wip_df['Start_Date'] = return_aging_wip_df['Start_Date'].apply(pd.to_datetime, errors='coerce')
		return_aging_wip_df['Done_Date'] = return_aging_wip_df['Done_Date'].apply(pd.to_datetime, errors='coerce')

		# set duration of each column to 0 and set the status of each item to the last status which is not null
		for col_name in in_date_col_names:
			return_aging_wip_df[col_name] = 0
			status_mask = pd.notnull(in_clean_df[col_name])
			return_aging_wip_df.loc[status_mask, 'Status'] = col_name

		# walk the date_col_name list backwards to do math of how long the item spent in each status.
		prev_column = self.end_col
		for col_name in reversed(in_date_col_names):
			return_aging_wip_df.loc[:, col_name] = (temp_clean_df[prev_column] - temp_clean_df[col_name]).dt.days
			return_aging_wip_df.loc[:, 'Age'] += return_aging_wip_df[col_name]
			prev_column = col_name

		done_mask = pd.notnull(in_clean_df[self.end_col])
		return_aging_wip_df.loc[done_mask, 'Done_Date'] = in_clean_df[self.end_col].loc[done_mask]
		return_aging_wip_df.loc[:, 'CycleTime85'] = self.cycle_time_85_confidence
		return_aging_wip_df.loc[:, 'CycleTime50'] = self.cycle_time_50_confidence
		return_aging_wip_df.loc[:, 'CycleTimeAvg'] = self.cycle_time_average
		self.charts_going_good = True
		return return_aging_wip_df

	def build_run_df(self, in_dates_df: pd.DataFrame, in_clean_df: pd.DataFrame) -> pd.DataFrame:
		return_run_df = pd.DataFrame({'Date': in_dates_df['Date']})
		return_run_df['WIP'] = return_run_df.apply(lambda row: self.calc_in_progress_on_date(row, in_clean_df), axis=1)
		# TODO: Review the SimulationCalcClass to see how I did this without cycling through each row before.
		return_run_df['Throughput'] = return_run_df.apply(lambda row: self.calc_throughput_on_date(row, in_clean_df), axis=1)
		return_run_df['WIPLimit'] = self.wip_limit
		self.charts_going_good = True
		return return_run_df

	def build_throughput_histogram_df(self, in_run_df: pd.DataFrame) -> pd.DataFrame:
		value_counts = in_run_df['Throughput'].value_counts()
		return_throughput_hist_df = pd.DataFrame(value_counts)
		return_throughput_hist_df.reset_index(inplace=True)
		return_throughput_hist_df.rename(columns={'Throughput': 'Count', 'index': 'Throughput'}, inplace=True)
		return_throughput_hist_df['Throughput85'] = self.throughput_85_confidence
		return_throughput_hist_df['Throughput50'] = self.throughput_50_confidence
		return_throughput_hist_df['ThroughputAvg'] = self.throughput_average
		return return_throughput_hist_df

	def build_cycle_time_histogram_df(self, in_aging_wip_df: pd.DataFrame) -> pd.DataFrame:
		completed_mask = in_aging_wip_df['Status'] == self.end_col
		completed_items = in_aging_wip_df.loc[completed_mask].copy()
		age_counts = completed_items['Age'].value_counts()
		return_cycle_time_hist_df = pd.DataFrame(age_counts)
		return_cycle_time_hist_df.reset_index(inplace=True)
		return_cycle_time_hist_df.rename(columns={'Age': 'Count', 'index': 'Age'}, inplace=True)
		return_cycle_time_hist_df['CycleTime85'] = self.cycle_time_85_confidence
		return_cycle_time_hist_df['CycleTime50'] = self.cycle_time_50_confidence
		return_cycle_time_hist_df['CycleTimeAvg'] = self.cycle_time_average
		return return_cycle_time_hist_df

	# This is aging wip, but only on completed items
	def build_cycle_time_scatter_df(self, in_aging_wip_df: pd.DataFrame) -> pd.DataFrame:
		completed_mask = in_aging_wip_df['Status'] == self.end_col
		return_cycle_time_scatter_df = in_aging_wip_df.loc[completed_mask].copy()
		return return_cycle_time_scatter_df

	# =========================================
	# INTERNAL FUNCTIONS
	# =========================================
	def calc_completed_on_date(self, row, in_col_name, in_clean_df):
		found_matching_rows = in_clean_df[in_col_name] <= row['Date'].date()
		return len(in_clean_df[found_matching_rows].index)

	def calc_in_progress_on_date(self, row: pd.Series, in_clean_df: pd.DataFrame):
		test_date = row['Date'].date()
		date_mask = (in_clean_df[self.start_col] <= test_date) & (in_clean_df[self.end_col].isnull()) | \
					((in_clean_df[self.start_col] <= test_date) & (in_clean_df[self.end_col] > test_date))
		return len(in_clean_df.loc[date_mask].index)

	def calc_throughput_on_date(self, row, in_clean_df: pd.DataFrame):
		test_date = row['Date'].date()
		date_mask = (in_clean_df[self.end_col] == test_date)
		return len(in_clean_df.loc[date_mask].index)

	def fillna_dates(self, in_df: pd.DataFrame) -> pd.DataFrame:
		temp_df = in_df.fillna(axis=1, method='bfill')
		return temp_df


def get_flow_dataframe() -> pd.DataFrame:
	return Globals.INPUT_CSV_DATAFRAME  # pragma: no cover
