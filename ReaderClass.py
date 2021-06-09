import csv
import pandas as pd


class CSVReader:
	def __init__(self, filename):
		with open(filename, 'r') as csv_file:
			self.csv_reader = csv.DictReader(csv_file)
			self.flowData = []
			for line in self.csv_reader:
				self.flowData.append(line)


class PandaReader:
	def __init__(self, filename):
		self.flowData = pd.read_csv(filename)
		self.flowData.columns = self.flowData.columns.str.replace(' ', '')

	def get_column_with_index(self, target_index):
		return self.flowData[target_index]

	def get_headers(self):
		return list(self.flowData.columns)

	def get_max_date(self, col_name):
		col_name = str(col_name).replace(' ', '')
		date_col = pd.to_datetime(self.flowData[col_name])
		return date_col.max()

	def get_min_date(self, col_name):
		col_name = str(col_name).replace(' ', '')
		date_col = pd.to_datetime(self.flowData[col_name])
		return date_col.min()

	def get_data(self):
		return self.flowData

	def write_csv_from_dataframe(self, inFrame):
		inFrame.to_csv('pi_data.csv', index=False)


# Pass in a dataframe and let this class manage it for you.
class CSVManager:
	def __init__(self, in_df):
		self.data = in_df

	def get_column_with_index(self, target_index):
		return self.data[target_index]

	def get_headers(self):
		return list(self.data.columns)

	def get_max_date(self, col_name):
		col_name = str(col_name).replace(' ', '')
		date_col = pd.to_datetime(self.data[col_name])
		return date_col.max()

	def get_min_date(self, col_name):
		col_name = str(col_name).replace(' ', '')
		date_col = pd.to_datetime(self.data[col_name])
		return date_col.min()

	def get_data(self):
		return self.data


class PandaWriter:
	def __init__(self, file_name, in_frame):
		in_frame.to_csv(file_name, index=False)
