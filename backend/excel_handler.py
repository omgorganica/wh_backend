import logging
import pandas as pd
from datetime import timedelta


def handle_excel(path):
	df = pd.read_excel(path)
	essential_headers = ['Work Date', 'Time From', 'Pers No', 'Overall Transports', 'Boxes Picked Picking','Loadings']

	try:
		file_headers = list(df)
		if not all(item in file_headers for item in essential_headers):
			raise ValueError('File do not contains essential headers')
	except ValueError as err:
		logging.warning(err)
		return

	df = df[['Work Date', 'Time From', 'Pers No', 'Overall Transports', 'Boxes Picked Picking',
			 'Loadings']].sort_values(by=['Work Date', 'Time From'], ascending=[True, True]).reset_index(drop=True)

	def work_shift(row):
		dd = str(row['Time From'])
		h, m, s = dd.split(':')
		h = int(h)

		if h in range(20, 24):
			return row['Work Date'] + timedelta(1)
		else:
			return row['Work Date']

	df['DATE'] = df.apply(work_shift, axis=1)
	final = df.groupby(['Pers No', 'DATE'], sort=True).sum().reset_index().to_dict(orient='records')
	return final


if __name__ == '__main__':
	pass
