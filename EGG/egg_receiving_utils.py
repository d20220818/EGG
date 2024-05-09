import pandas as pd
from EGG.hatchery import *
from pyx.dataframe_utility import segment

def check(df, start_date=None, end_date=None):
	if start_date == None:
		start_date = df['PRODUCTION_DATE'].min()
	if end_date == None:
		end_date = df['PRODUCTION_DATE'].max()
	print(f"\nChecking eggs from {start_date.strftime('%d/%m/%Y')} to {end_date.strftime('%d/%m/%Y')}...\n")

	result = []
	for i, x in df[['STRAIN_CODE', 'MTECH_FLOCK_ID']].drop_duplicates().iterrows():
		df2 = df[(df['STRAIN_CODE'] == x['STRAIN_CODE']) & (df['MTECH_FLOCK_ID'] == x['MTECH_FLOCK_ID'])].sort_values(by='PRODUCTION_DATE')
		#row = []
		#row.append(f"{x['STRAIN_CODE']} {x['MTECH_FLOCK_ID']}")
		for d in pd.date_range(start=start_date,end=end_date):
			#print(df2['PRODUCTION_DATE'])
			tickets = len(df2[df2['PRODUCTION_DATE'] == d]['EGG_TICKET_NUMBER'].unique())
			#if tickets == 1: row.append('')
			#else: row.append(tickets - 1)
			if tickets < 1:
				print(f"Missing eggs of {x['STRAIN_CODE']} {x['MTECH_FLOCK_ID']} at {d.strftime('%d/%m/%Y')}")
			elif tickets > 1:
				print(f"{tickets} duplicated eggs of {x['STRAIN_CODE']} {x['MTECH_FLOCK_ID']} at {d.strftime('%d/%m/%Y')}")
		#result.append(row)
	#print(result)
	print('\nDone!')






def check_per_class(df, start_date=None, end_date=None):
	if start_date == None:
		start_date = df['PRODUCTION_DATE'].min()
	if end_date == None:
		end_date = df['PRODUCTION_DATE'].max()
	print(f"\nChecking eggs from {start_date.strftime('%d/%m/%Y')} to {end_date.strftime('%d/%m/%Y')}...\n")


	df = df[df['EGG_CLASS'].isin(HEX)]
	for i, x in df[['STRAIN_CODE', 'MTECH_FLOCK_ID', 'EGG_CLASS']].drop_duplicates().iterrows():
		
		df2 = df[(df['STRAIN_CODE'] == x['STRAIN_CODE']) & (df['MTECH_FLOCK_ID'] == x['MTECH_FLOCK_ID']) & (df['EGG_CLASS'] == x['EGG_CLASS'])].sort_values(by='PRODUCTION_DATE')
		print(f"{x['STRAIN_CODE']} {x['MTECH_FLOCK_ID']} {x['EGG_CLASS']}\n")
		dates = pd.date_range(start=start_date,end=end_date)
		for d in range(1, len(dates)):
			prev = df2[df2['PRODUCTION_DATE'] == dates[d-1]]['EGGS'].sum()
			cur = df2[df2['PRODUCTION_DATE'] == dates[d]]['EGGS'].sum()
			print(f"{dates[d].strftime('%Y/%m/%d')} - {cur - prev} - {(cur - prev) / prev}")
		print('\n\n')
	print('\nDone!')

def resume(df):
	#df['STRAIN_CODE'] = df['STRAIN_CODE'].map(lambda x: str(x))
	#df['LINE'] = df['STRAIN_CODE'].map(line)
	for df2 in segment(df, ['STRAIN_CODE']):
		s = df2['STRAIN_CODE'].iloc[0]
		print(f"{s} Incubáveis (Quantidades sem erros) - {df2[df2['EGG_CLASS'].isin(HEX)]['EGGS'].sum()}")
		print(f"{s} Não incubáveis (Quantidades com erros) - {df2[~df2['EGG_CLASS'].isin(HEX)]['EGGS'].sum()}")
		print(f"{s} Total - {df2['EGGS'].sum()}\n")
	print('\nDone!')