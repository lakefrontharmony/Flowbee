import pandas as pd
import numpy as np
from datetime import datetime
import Globals


class FlowCalcClass:
	def __init__(self):
		self.prep_going_good = True
		self.calcs_going_good = True
		self.errors = []

	# =========================================
	# EXTERNALLY CALLED FUNCTIONS
	# =========================================
	def prep_for_metrics(self):
		pass

	def run_release_metrics(self):
		pass

	# This is a check for errors.
	# Return True if errors were found, False if there were no errors
	def errors_were_found(self):
		if self.prep_going_good:
			return False
		return True

	def get_error_msgs(self):
		return self.errors

	# =========================================
	# ASSUMPTIONS
	# =========================================
	def get_flow_metric_assumptions(self):
		assumptions = [[]]
		assumptions_df = pd.DataFrame(assumptions, columns=['Assumption'])
		return assumptions_df
