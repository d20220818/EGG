import pandas as pd
import pyx.osx as osx

async def read_File(obj, sheet_name=0):
	filepath_or_buffer = await to_bytes(obj)
	if osx.ext(obj.name) == '.csv':
		return pd.read_csv(filepath_or_buffer, sep=';', encoding='latin-1')
	elif osx.ext(obj.name) in ['.xls', '.xlsx']:
		return pd.read_excel(filepath_or_buffer, sheet_name=sheet_name)

async def read_FileList(ls):
	result = []
	for i in range(ls.length):
		result.append(await read_File(ls.item(i)))
	return result

async def from_fileInputIDs(fileInputIDs):
	result = []
	for x in fileInputIDs:
		#print(x)
		id = x if isinstance(x, str) else x[0]
		files = document.getElementById(id).files
		if files.length == 0:
			print(f'Arquivo(s) {id} ausente(s)')
			return False
		result.append(await read_File(files.item(0), sheet_name=0 if isinstance(x, str) else x[1]))
	return result

def strfdaterange(dates, format='%Y-%m-%d', sep=' A '):
	return dates.min().strftime(format) + sep + dates.max().strftime(format)