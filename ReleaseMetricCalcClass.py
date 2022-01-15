import pandas as pd
import Globals
import json


class ReleaseMetricCalcClass:

	def __init__(self):
		self.json_file = None
		self.json_dataframe = None
		self.release_df = None

	###################################
	# GETTERS
	###################################
	def get_json_file(self):
		return self.json_file

	def get_json_dataframe(self):
		return self.json_dataframe

	###################################
	# OPEN FILES
	###################################
	def read_json_file(self, input_file):
		self.json_file = json.load(input_file)
		self.normalize_json_to_df(self.json_file)

	def normalize_json_to_df(self, input_json):
		df_1 = pd.json_normalize(input_json)
		self.json_dataframe = pd.json_normalize(df_1.iat[0, 0])

	def read_releases_csv_file(self, in_csv):
		self.release_df = pd.read_csv(in_csv)

	###################################
	# FUNCTIONS
	###################################
	def pipeline_entry_exists_for(self, in_name):
		result = self.json_dataframe[(self.json_dataframe['slug'] == in_name) &
										  (self.json_dataframe['statusMessage'] == 'Available')]
		if result.empty:
			return False
		else:
			return True
