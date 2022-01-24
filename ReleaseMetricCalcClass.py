import pandas as pd
import json
from datetime import datetime, date

class ReleaseMetricCalcClass:

	def __init__(self):
		self.fix_version_col_name = 'Fix Version/s'
		self.release_system_col_name = 'System'
		self.release_date_col_name = 'Release Date'
		self.on_pipeline_col_name = 'On Pipeline'
		self.json_file = None
		self.json_dataframe = None
		self.release_df = None
		self.summary_df = None
		self.start_date = date.today()
		self.end_date = date.today()

	# ##################################
	# GETTERS
	# ##################################
	def get_json_file(self):
		return self.json_file   # pragma: no cover

	def get_json_dataframe(self):
		return self.json_dataframe   # pragma: no cover

	def get_release_df(self):
		return self.release_df   # pragma: no cover

	def get_release_summary_df(self):
		return self.summary_df   # pragma: no cover

	# ##################################
	# OPEN FILES
	# ##################################
	def read_json_file(self, input_file):
		self.json_file = json.load(input_file)
		self.normalize_json_to_df(self.json_file)

	def normalize_json_to_df(self, input_json):
		df_1 = pd.json_normalize(input_json)
		self.json_dataframe = pd.json_normalize(df_1.iat[0, 0])

	def read_releases_csv_file(self, in_csv):
		self.release_df = pd.read_csv(in_csv, keep_default_na=False)
		if self.fix_version_col_name not in self.release_df:
			# error if this column does not exist
			pass
		if self.release_date_col_name in self.release_df:
			self.release_df[self.release_date_col_name] = \
				pd.to_datetime(self.release_df[self.release_date_col_name]).dt.date
		else:
			# error if this column does not exist
			pass

	# ##################################
	# EXTERNAL FUNCTIONS
	# ##################################
	# excluding this Function from code coverage because all it does is call other internal functions which are included.
	def prepare_for_metrics(self, in_pipeline_file, in_releases_file):
		self.read_json_file(in_pipeline_file)  # pragma: no cover
		self.read_releases_csv_file(in_releases_file)  # pragma: no cover
		self.release_df = self.strip_release_name_of_version(self.release_df)  # pragma: no cover

	# excluding this Function from code coverage because all it does is call other internal functions which are included.
	def run_release_metrics(self, start_date=None, end_date=None):
		if start_date is None:  # pragma: no cover
			self.release_df = self.check_df_for_pipelines(self.release_df)  # pragma: no cover
		else:  # pragma: no cover
			self.release_df = self.check_df_for_pipelines_between_dates(self.release_df, start_date, end_date)  # pragma: no cover
		self.summary_df = self.build_summary_df(self.release_df)  # pragma: no cover

	# ##################################
	# INTERNAL FUNCTIONS
	# ##################################
	def strip_release_name_of_version(self, in_release_pd: pd.DataFrame) -> pd.DataFrame:
		# use self.release_df and perform str.split to replace name with just the name up to the first space
		temp_df = in_release_pd.copy()
		new_names = temp_df[self.fix_version_col_name].str.split(pat=' ', n=1, expand=True)
		temp_df[self.release_system_col_name] = new_names[0]
		return temp_df[[self.fix_version_col_name, self.release_system_col_name, self.release_date_col_name]]

	def check_df_for_pipelines(self, in_release_pd: pd.DataFrame) -> pd.DataFrame:
		temp_df = in_release_pd.copy()
		temp_df[self.on_pipeline_col_name] = temp_df.apply(self.pipeline_entry_exists_for_row, axis=1)
		return temp_df

	def check_df_for_pipelines_between_dates(self, in_release_pd: pd.DataFrame,
											 in_start_date: datetime.date, in_end_date: datetime.date) -> pd.DataFrame:
		temp_df = in_release_pd.copy()
		date_mask = (temp_df[self.release_date_col_name] >= in_start_date) & \
					(temp_df[self.release_date_col_name] <= in_end_date)
		temp_df = temp_df.loc[date_mask]
		temp_df.reset_index(drop=True, inplace=True)
		temp_df = self.check_df_for_pipelines(temp_df)
		return temp_df

	def pipeline_entry_exists_for_row(self, in_row):
		entry = in_row[self.release_system_col_name]
		return self.pipeline_entry_exists_for(entry)

	def pipeline_entry_exists_for(self, in_name):
		result = self.json_dataframe[(self.json_dataframe['slug'] == in_name) &
										  (self.json_dataframe['statusMessage'] == 'Available')]
		if result.empty:
			return 'False'
		else:
			return 'True'

	def build_summary_df(self, in_pd: pd.DataFrame) -> pd.DataFrame:
		temp_df = in_pd.copy()
		pipeline_counts = temp_df.groupby([self.on_pipeline_col_name]).size().reset_index(name='Count')
		return pipeline_counts
