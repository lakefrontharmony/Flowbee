import pandas as pd
import Globals
import json


class ReleaseMetricCalcClass:

	def __init__(self):
		self.fix_version_col_name = 'Fix Version/s'
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
			return 'False'
		else:
			return 'True'

	def pipeline_entry_exists_for_row(self, in_row):
		entry = in_row[self.fix_version_col_name]
		return self.pipeline_entry_exists_for(entry)

	def strip_release_name_of_version(self, in_release_pd: pd.DataFrame) -> pd.DataFrame:
		# use self.release_df and perform str.split to replace name with just the name up to the first space
		temp_pd = in_release_pd.copy()
		new_names = temp_pd[self.fix_version_col_name].str.split(pat=' ', n=1, expand=True)
		temp_pd[self.fix_version_col_name] = new_names[0]
		return temp_pd

	def check_df_for_pipelines(self, in_release_pd: pd.DataFrame) -> pd.DataFrame:
		temp_pd = in_release_pd.copy()
		temp_pd['On Pipeline'] = temp_pd.apply(self.pipeline_entry_exists_for_row, axis=1)
		return temp_pd
