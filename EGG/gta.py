import pandas as pd
from pyx.xl import *
import datetime as dtm

def atualizar_gtas(ws2, sheet):
	sorted_sheet = sheet.sort_values(by=['FARM_NAME', 'PRODUCTION_DATE', 'FARM_CODE', 'MTECH_FLOCK_ID', 'GTA_NUMBER'])
	sorted_sheet['PRODUCTION_DATE'] = sorted_sheet['PRODUCTION_DATE'].map(lambda x: (pd.to_datetime(x) + dtm.timedelta(days = 1)))
	sorted_sheet['MTECH_FLOCK_ID'] = sorted_sheet['FARM_CODE'].map(lambda x: '/'.join(sorted(sorted_sheet[sorted_sheet['FARM_CODE'] == x]['MTECH_FLOCK_ID'].unique())))
	sorted_sheet['FARM_CODE'] = sorted_sheet['FARM_CODE'].map(lambda x: x[4:])

	sorted_sheet = sorted_sheet.assign(TRANSFER_DATE=sorted_sheet['GTA_NUMBER'].map(lambda x: sorted_sheet[sorted_sheet['GTA_NUMBER'] == x]['PRODUCTION_DATE'].max()))

	wb = EmptyWorkbook()
	for fn in sorted_sheet['FARM_NAME'].unique():

		ws = wb.create_sheet(title=fn)
	
		df = sorted_sheet[sorted_sheet['FARM_NAME'] == fn]

		df = df.groupby(by=['TRANSFER_DATE', 'FARM_CODE', 'MTECH_FLOCK_ID', 'GTA_NUMBER']).sum()
		df = df.reset_index()
		#print(df)

		df['SÉRIE'] = ''
		df['DATA EMISSÃO'] = ''#df['TRANSFER_DATE']
		df['OVOS GTA'] = ''
		df = df[['GTA_NUMBER', 'SÉRIE', 'DATA EMISSÃO', 'TRANSFER_DATE', 'FARM_CODE', 'MTECH_FLOCK_ID', 'OVOS GTA', 'EGGS']]


		if fn not in wb2.sheetnames:
			wb2.create_sheet(title=fn)
			set_row(wb2[fn], 1, list(df.columns) + ['TOTAL'])
			set_range_border(wb2[fn], 1, 1, 1, len(df.columns) + 1)
			set_range_style(wb2[fn], 1, 1, 1, len(df.columns) + 1, fill=color_fill("FF0937B7"), font=Font(bold=True, color='FFFFFFFF'))
			set_content_alignment(wb2[fn])
			set_columns_width(wb2[fn], 15)
			wb2[fn].freeze_panes = 'A2'

		if wb2[fn].max_row > 1:
			last_date = pd.to_datetime(get_cell(wb2[fn], wb2[fn].max_row, 4).value, dayfirst=True)
			#last_date = last_date.strftime("%Y-%m-%d")
			#print([df['TRANSFER_DATE'], last_date])
			df = df[df['TRANSFER_DATE'] > last_date]

		#PINTAR AS LINHAS JÁ CONFERIDAS, OU SEJA, AS ANTERIORES A ESTA ATUALIZAÇÃO POR VIR
		set_range_style(wb2[fn], 2, 1, wb2[fn].max_row, 9, fill=color_fill("FFFFE699"))



		df['TRANSFER_DATE'] = df['TRANSFER_DATE'].map(lambda x: x.strftime("%d/%m/%Y"))

		df.rename(columns = {'GTA_NUMBER': 'Nº DA GTA', 'TRANSFER_DATE': 'DATA REAL', 'FARM_CODE': 'NÚCLEO', 'MTECH_FLOCK_ID': 'LOTE', 'EGGS': 'OVOS REAL'}, inplace=True)
		cols = len(df.columns)

		dfvalscpy(ws, df, 1, 1)
		#merge_vertically(ws, 1, 1, df.shape[0], 3)
		merge_vertically(ws, 1, 1, df.shape[0], 1)
		copy_merge(ws, [1, 1, df.shape[0], 1], 1, 2)
		copy_merge(ws, [1, 1, df.shape[0], 1], 1, 3)
		copy_merge(ws, [1, 1, df.shape[0], 1], 1, 4)
		copy_merge(ws, [1, 1, df.shape[0], 1], 1, 7)
		set_range_border_by_group(ws, 1, 1, df.shape[0], cols)

		set_range_style(ws, 1, 5, df.shape[0], 7, font=Font(bold=True))

		add_total_column(ws, 1, cols, cols + 1, 1, ws.max_row)


		set_content_alignment(ws)
	

		wscpy(wb2[fn], ws, wb2[fn].max_row + 1)
	print('Done!')
	return wb2