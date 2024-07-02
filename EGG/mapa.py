import pandas as pd
from pyx.pandasx import join, fillnext
from EGG.hatchery import products, production, farm_names

def summary(objs, by): return [x.groupby(by=by).sum(numeric_only=True).reset_index() for x in objs]

def MAPA_production(clas, inc, nasc, db):

  for df in [clas, inc, nasc]:
	  df['MTECH_FLOCK_ID'] = df['FARM_CODE'].map(lambda x: '/'.join(sorted(df[df['FARM_CODE'] == x]['MTECH_FLOCK_ID'].unique())))
	  #df['BREED'] = df['STRAIN_CODE'].map(lambda x: breed(x))
	  df['PRODUCT'] = products(db['STRAIN'], df['STRAIN_CODE'])

  on = ['FARM_CODE', 'MTECH_FLOCK_ID', 'PRODUCT']#'BREED']
  data = join(summary([clas, inc, nasc], on), on)

  data['TOTAL SALEABLE_2'] = data.apply(lambda x: x['TO_CHICKS_2'] - (x['PRE_SEX_CULLS_2'] + x['PRIME_CULLS_2']), axis=1)
  data = data[on + ['EGGS', 'EGGS_1', 'TO_CHICKS_2', 'TOTAL SALEABLE_2']].fillna(0)

  data['FARM_NAME'] = farm_names(db['FARM'], data['FARM_CODE'])
  #data['FARM_CODE'].map(lambda x: {'001': 'GRANJA 1.2', '004': 'GRANJA 4.6', '012': 'GRANJA SF', '014': 'GRANJA MINA', '022': 'GRANJA ITAPEVA', '013': 'GRANJA IPUIUNA', '007': 'GRANJA 7', '016': 'GRANJA LUZIANIA'}[x[:3]])

  data['PRODUCTION'] = data['FARM_CODE'].map(lambda x: production(x))

  new_columns = [
	  'Identificação dos ovos', 'Origem dos ovos', 'Granja de origem', 'Núcleo de produção', 'Linhagem', 'Ovos recebidos', 'Ovos incubados',
	  'Pintos nascidos', 'Pintos vendáveis'
  ]

  #data = data.rename(columns=dict(zip(['MTECH_FLOCK_ID', 'PRODUCTION', 'FARM_NAME', 'FARM_CODE', 'BREED', 'EGGS', 'EGGS_1', 'TO_CHICKS_2', 'TOTAL SALEABLE_2'], new_columns)))
  data = data.rename(columns=dict(zip(['MTECH_FLOCK_ID', 'PRODUCTION', 'FARM_NAME', 'FARM_CODE', 'PRODUCT', 'EGGS', 'EGGS_1', 'TO_CHICKS_2', 'TOTAL SALEABLE_2'], new_columns)))
	
  data = data.reindex(columns=new_columns)

  #print(data)
  return data


def consumo_mensal(cadastro, saida, ano, mes): #CONSUMO DE VACINAS NO MÊS
	cadastro = cadastro[cadastro['Categoria'] == 'Vacina']
	#print(cadastro)

	saida['Data'] = pd.to_datetime(saida['Data'], format='%Y-%m-%d')

	saida = saida.loc[(saida['Data'].dt.year==ano) & (saida['Data'].dt.month==mes)]#, 'selected_column'] = new_column_values

	saida = saida[saida['Observações'].isnull()]


	saida = saida[['Cod. Produto', 'Nome Produto', 'Observações', 'Qtde.']]

	saida = saida.groupby(by=['Cod. Produto', 'Nome Produto']).sum(numeric_only = True).reset_index()

	saida = saida.set_index(['Cod. Produto', 'Nome Produto']).join(cadastro.set_index(['Cod. Produto', 'Nome Produto'])).reset_index()

	saida = saida[saida['Categoria'] == 'Vacina']

	saida['Total'] = saida['Qtde.'] * saida['Un.']
	return saida



def MAPA_vaccines(cadastro, saida, partidas, ordens, year, month): #Cadastro de vacinas, saída de vacinas, aves vacinadas
	saida = consumo_mensal(cadastro, saida, year, month)

	#AVES VACINADAS
	partidas = partidas[partidas['Categoria'] == 'Vacina'].reset_index()

	ordens['HATCH DATE'] = pd.to_datetime(ordens['HATCH DATE'], dayfirst=True)

	fillnext(ordens, ['ORDER STATUS', 'HATCH DATE', 'VACCINES'])
	print(ordens)
	ordens = ordens[ordens['ORDER STATUS'] != 'Cancelled'].reset_index()
	ordens['TO_CHICKS_DISPATCHED'] = ordens['MALES'] + ordens['FEMALES']
	
	ordens = ordens.loc[(ordens['HATCH DATE'].dt.year==year) & (ordens['HATCH DATE'].dt.month==month) & (ordens['TO_CHICKS_DISPATCHED'] > 0)]
	ordens = ordens.reset_index()


	vac2 = pd.DataFrame(data=[], columns=['Doenças', 'Nome', 'Laboratório', 'Partida', 'Validade', 'Produtos', 'Aves vacinadas'])


	partidas['Código'] = partidas['Código'].map(lambda x: str(x))

	for i in range(ordens.shape[0]):
		vaccine_numbers = str(ordens.iloc[i, ordens.columns.get_loc('VACCINES')])
		print(vaccine_numbers)
		if pd.isnull(vaccine_numbers): continue
		vaccine_numbers = vaccine_numbers.replace(' ', '').replace('.', ',').split(',')
		for cod in vaccine_numbers:
			row = partidas[partidas['Código'] == cod]
			if row.shape[0] == 0: continue
			row = row.iloc[0]
			vac2.loc[len(vac2)] = [row['Doenças'], row['Nome'], row['Laboratório'], row['Partida'], row['Validade'], row['Produtos'], ordens.loc[i]['TO_CHICKS_DISPATCHED']]

	#print(vac2)

	vac2 = vac2.groupby(by=['Doenças', 'Nome', 'Laboratório', 'Partida', 'Validade', 'Produtos']).sum(numeric_only = True).reset_index()
	vac2 = vac2.sort_values(by=['Doenças', 'Laboratório', 'Nome'])

	def doses_usadas(df, produtos): return df[df['Cod. Produto'].isin(produtos)]['Total'].sum()

	vac2['Produtos'].fillna('', inplace=True)

	saida['Cod. Produto'] = saida['Cod. Produto'].map(lambda x: str(int(x)))
	vac2['Doses'] = vac2['Produtos'].map(lambda x: doses_usadas(saida, str(x).replace(' ', '').replace('.', ',').split(',')))


	vac2['Oleosa'] = ''
	vac2['Aquosa'] = ''
	vac2 = vac2[['Nome', 'Doenças', 'Laboratório', 'Partida', 'Doses', 'Oleosa', 'Aquosa', 'Validade', 'Aves vacinadas']]
	return vac2
