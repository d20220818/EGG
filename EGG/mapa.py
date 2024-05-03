import pandas as pd
from pyx.dataframe_utility import join

def summary(objs, by): return [x.groupby(by=by).sum(numeric_only=True).reset_index() for x in objs]

def MAPA_production(clas, inc, nasc):

  for df in [clas, inc, nasc]:
	  df['MTECH_FLOCK_ID'] = df['FARM_CODE'].map(lambda x: '/'.join(df[df['FARM_CODE'] == x]['MTECH_FLOCK_ID'].unique()))
	  #df['BREED'] = df['STRAIN_CODE'].map(lambda x: breed(x))

  on = ['FARM_CODE', 'MTECH_FLOCK_ID']#, 'BREED']
  data = join(summary([clas, inc, nasc], on), on)

  data['TOTAL SALEABLE_2'] = data.apply(lambda x: x['TO_CHICKS_2'] - (x['PRE_SEX_CULLS_2'] + x['PRIME_CULLS_2']), axis=1)
  data = data[on + ['EGGS', 'EGGS_1', 'TO_CHICKS_2', 'TOTAL SALEABLE_2']].fillna(0)

  data['FARM_NAME'] = data['FARM_CODE'].map(lambda x: {'001': 'GRANJA 1.2', '004': 'GRANJA 4.6', '012': 'GRANJA SF', '014': 'GRANJA MINA', '022': 'GRANJA ITAPEVA', '013': 'GRANJA IPUIUNA', '007': 'GRANJA 7', '016': 'GRANJA LUZIANIA'}[x[:3]])

  data['PRODUCTION'] = data['FARM_CODE'].map(lambda x: production(x))

  """new_columns = [
	  'Identificação dos ovos', 'Origem dos ovos', 'Granja de origem', 'Núcleo de produção', 'Linhagem', 'Ovos recebidos', 'Ovos incubados',
	  'Pintos nascidos', 'Pintos vendáveis'
  ]

  data = data.rename(columns=dict(zip(['MTECH_FLOCK_ID', 'PRODUCTION', 'FARM_NAME', 'FARM_CODE', 'BREED', 'EGGS', 'EGGS_1', 'TO_CHICKS_2', 'TOTAL SALEABLE_2'], new_columns)))

  data = data.reindex(columns=new_columns)"""

  print(data)
  return data
