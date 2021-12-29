import pandas as pd
import numpy as np
import Globals
from datetime import datetime, date, timedelta


class ChartBuilderClass:
	def __init__(self, st_col, end_col, name_col, chart_st, wip_limit):
		self.start_date = chart_st
		self.start_col = str(st_col).replace(' ', '')
		self.end_col = str(end_col).replace(' ', '')
		self.name_col = str(name_col).replace(' ', '')
		self.chart_start = datetime.strptime(chart_st, '%Y-%m-%d')
		self.wip_limit = wip_limit

		self.prep_going_good = True
		self.charts_going_good = True
		self.clean_completed_df = None
		self.clean_wip_df = None
		self.dates_df = None
		self.cfd_df = None
		self.errors = []

	# =========================================
	# EXTERNALLY CALLED FUNCTIONS
	# =========================================
	def prep_for_charting(self):
		self.build_clean_df()
		#if self.prep_going_good:
		#	self.build_clean_wip_df()
		if self.prep_going_good:
			Globals.GOOD_FOR_GO = True
		else:
			Globals.GOOD_FOR_GO = False

	def build_charts(self):
		self.build_cfd_df()
		self.build_aging_wip_df()
		self.build_wip_run_df()
		self.build_throughput_histogram_df()
		self.build_throughput_run_df()
		if self.charts_going_good:
			Globals.CHARTS_BUILT_SUCCESSFULLY = True
		else:
			Globals.CHARTS_BUILT_SUCCESSFULLY = False

	def get_errors(self):
		return self.errors

	# =========================================
	# ASSUMPTIONS
	# =========================================
	def get_assumptions(self):
		assumptions = [[]]
		if 'Cancelled' in Globals.INPUT_CSV_DATAFRAME:
			assumptions.append(['Cancelled items were excluded from calculations'])
		else:
			assumptions.append(['No cancelled column was found. (Column must be titled "Cancelled"'])
		assumptions_df = pd.DataFrame(assumptions, columns=['Assumption'])
		return assumptions_df


	# =========================================
	# PREP FUNCTIONS
	# =========================================
	# Build dataframe with non-null dates in end-column and start-column (include all columns between those two)
	# Convert date columns to datetime elements.
	def build_clean_df(self):
		self.clean_completed_df = Globals.INPUT_CSV_DATAFRAME

		# filter to only items which have not been cancelled and items which have at least reached your start column
		if 'Cancelled' in self.clean_completed_df:
			cancelled_mask = self.clean_completed_df['Cancelled'] != 'Yes'
			self.clean_completed_df = self.clean_completed_df.loc[cancelled_mask]

		start_bool_series = pd.notnull(self.clean_completed_df[self.start_col])
		self.clean_completed_df = self.clean_completed_df[start_bool_series]

		if self.clean_completed_df is None:
			self.prep_going_good = False
			self.errors.append('No in-progress data to chart from the input set. '
							   'Verify there are valid dates in input file')
			return

		# convert date columns to datetime elements
		self.clean_completed_df.loc[:, self.start_col:self.end_col] = \
			self.clean_completed_df.loc[:, self.start_col:self.end_col].apply(pd.to_datetime, errors='coerce')
		# Concatenate down to just the name column and the date columns
		self.clean_completed_df = pd.concat([self.clean_completed_df.loc[:, self.name_col].to_frame(),
									   self.clean_completed_df.loc[:, self.start_col:self.end_col]], axis=1)

		print(self.clean_completed_df)
		self.prep_going_good = True

	# If I determine that I want to split dataframes to completed and in progress, I can re-instate these two functions.
	# def build_clean_completed_df(self):
	# 	base_df = Globals.INPUT_CSV_DATAFRAME
		# filter to only items which have not been cancelled
	# 	if 'Cancelled' in base_df:
	# 		cancelled_mask = base_df['Cancelled'] != 'Yes'
	# 		base_df = base_df.loc[cancelled_mask]
	# 	end_bool_series = pd.notnull(base_df[self.end_col])
	#	self.clean_completed_df = base_df[end_bool_series]
	#	start_bool_series = pd.notnull(self.clean_completed_df[self.start_col])
	#	self.clean_completed_df = self.clean_completed_df[start_bool_series]
	#	if self.clean_completed_df is None:
	#		self.prep_going_good = False
	#		self.errors.append('No completed data to chart from the input set. '
	#						   'Verify there are valid dates in input file.')
	#		return

		# convert date columns to datetime elements.
		# TODO: Add in a search with 'isnull()' to find any rows that may have invalid or missing dates.
	#	self.clean_completed_df.loc[:, self.start_col:self.end_col] = \
	#		self.clean_completed_df.loc[:, self.start_col:self.end_col].apply(pd.to_datetime, errors='coerce')
	#	self.clean_completed_df = pd.concat([self.clean_completed_df.loc[:, self.name_col].to_frame(),
	#										 self.clean_completed_df.loc[:, self.start_col:self.end_col]], axis=1)

	#	self.prep_going_good = True

	# def build_clean_wip_df(self):
	#	self.clean_wip_df = Globals.INPUT_CSV_DATAFRAME
		# filter to only items which have not been cancelled
	#	if 'Cancelled' in self.clean_wip_df:
	#		cancelled_mask = self.clean_wip_df['Cancelled'] != 'Yes'
	#		self.clean_wip_df = self.clean_wip_df.loc[cancelled_mask]
	#	start_bool_series = pd.notnull(self.clean_wip_df[self.start_col])
	#	self.clean_wip_df = self.clean_wip_df[start_bool_series]

	#	if self.clean_wip_df is None:
	#		self.prep_going_good = False
	#		self.errors.append('No in-progress data to chart from the input set. '
	#						   'Verify there are valid dates in input file')
	#		return

		# convert date columns to datetime elements
	#	self.clean_wip_df.loc[:, self.start_col:self.end_col] = \
	#		self.clean_wip_df.loc[:, self.start_col:self.end_col].apply(pd.to_datetime, errors='coerce')
	#	self.clean_wip_df = pd.concat([self.clean_wip_df.loc[:, self.name_col].to_frame(),
	#										 self.clean_wip_df.loc[:, self.start_col:self.end_col]], axis=1)

	#	date_mask = ((self.clean_wip_df[self.end_col].isnull()))
	#	self.clean_wip_df = self.clean_wip_df[date_mask]
	#	print(self.clean_wip_df)
	#	self.prep_going_good = True

	# =========================================
	# CHARTING FUNCTIONS
	# =========================================
	def build_cfd_df(self):
		pass

	def build_aging_wip_df(self):
		pass

	def build_wip_run_df(self):
		pass

	def build_throughput_histogram_df(self):
		pass

	def build_throughput_run_df(self):
		pass

	# =========================================
	# INTERNAL FUNCTIONS
	# =========================================
