from pyx.xl import *
import math

def gerar_controles(anomes, listas, wb):
	template = wb.worksheets[0]
	replace2(template, **{'#UNIDADE': 'INC RIO CLARO', '#ANOMES': anomes})
	if len(wb.worksheets) > 2:
		replace2(wb.worksheets[1], **{'#UNIDADE': 'INC RIO CLARO', '#ANOMES': anomes})
	for k in listas:
		listas[k] = listas[k].sort_values(by=['COLABORADOR']).reset_index(drop=True)
		#print(listas[k])
		row_count = 0
		while True:
			if find_address(template, f"#COLABORADOR{'{:02d}'.format(row_count+1)}") is None:
				break
			row_count += 1
		ws = []
		page_count = math.ceil(listas[k].shape[0] / row_count)
		for i in range(0, page_count):
			ws.append(wb.copy_worksheet(template))
			ws[-1].title = f"{k}{' ' + str(i+1) if i > 0 else ''}"
		for i, x in enumerate(listas[k]['COLABORADOR']):
			page = math.floor(i / row_count)
			row = i % row_count
			replace2(ws[page], **{f"#COLABORADOR{'{:02d}'.format(row+1)}": x, f"#CARGO{'{:02d}'.format(row+1)}": str(listas[k]['CARGO'][i])})
		for i in range(len(listas[k]['COLABORADOR']) % row_count, row_count):
			row = i % row_count
			replace2(ws[-1], **{f"#COLABORADOR{'{:02d}'.format(row+1)}": '', f"#CARGO{'{:02d}'.format(row+1)}": ''})
	wb.remove(template)
	return wb

def colabs_list(colabs):
	listas = {}
	listas['NOTURNO'] = colabs[colabs['TURNO'] == 'NOTURNO'][['COLABORADOR', 'CARGO']]	#['COLABORADOR']
	colabs = colabs[colabs['TURNO'] == 'DIURNO']
	colabs['SETOR'] = colabs['SETOR'].map(lambda x: 'APOIO E ESCRITÓRIO' if x in ['APOIO', 'ESCRITÓRIO'] else x)
	for st in colabs['SETOR'].unique():
		listas[st] = colabs[colabs['SETOR'] == st][['COLABORADOR', 'CARGO']]	#['COLABORADOR']
	return listas
