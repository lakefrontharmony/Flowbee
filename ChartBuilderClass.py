import pandas as pd
import numpy as np
import Globals
from datetime import datetime, date, timedelta


class ChartBuilderClass:
	def __init__(self, st_col, end_col, chart_st, wip_limit):
		self.start_date = chart_st
		self.start_col = str(st_col).replace(' ', '')
		self.end_col = str(end_col).replace(' ', '')
		self.chart_start = datetime.strptime(chart_st, '%Y-%m-%d')
		self.wip_limit = wip_limit

		self.prep_going_good = True
		self.charts_going_good = True
		self.clean_df = None
		self.dates_df = None
		self.cfd_df = None

	def prep_for_charting(self):
		if self.prep_going_good:
			Globals.GOOD_FOR_GO = True

	def build_charts(self):
		self.build_cfd_df()
		self.build_aging_wip_df()
		self.build_wip_run_df()
		self.build_throughput_histogram_df()
		self.build_throughput_run_df()
		if self.charts_going_good:
			Globals.CHARTS_BUILT_SUCCESSFULLY = True

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
