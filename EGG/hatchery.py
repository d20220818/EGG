import pandas as pd
import pyx.array_utility as au

HE = [f'HE{i}' for i in range(1,5)]
XN = [f'X{i}' for i in range(1,5)]
XP = [f'X{i}P' for i in range(1,5)]
X = XN + XP
HEX = HE + X
SMASHED_NINHO = ['DY', 'DEF', 'D', 'SUJ', 'QUB', 'PEQ', 'CF', 'TA', 'NI']
SMASHED_PISO = [f'{x}P' for x in SMASHED_NINHO]
EGG_NINHO_CLASSES = HE + XN + SMASHED_NINHO
EGG_CLASSES = HE + XN + XP + SMASHED_NINHO + SMASHED_PISO

def egg_class_2(egg_class): return 'LIMPO' if egg_class in HE else 'X' if egg_class in X else 'NÃO INCUBÁVEL'

def egg_class_3(egg_class): return 'INCUBÁVEL' if egg_class in HEX else 'NÃO INCUBÁVEL'

def egg_height(egg_class): return egg_class[-1] if egg_class in HE + XN else egg_class[-2] if egg_class in XP else ''

def production(farm_code): return 'PRODUÇÃO EXTERNA' if 'EXT' in farm_code else 'PRODUÇÃO PRÓPRIA' #PRODUÇÃO IMPORTADA

#def generation(strain):

def line(strain):
	return au.group_of({'F': ['AP95', 'APN', 'F47', 'F72'], 'M': ['344', 'M35', 'M65', 'M77', 'ROM'], 'A': ['AH'], '1': ['AHB'], '4': ['BHB'], '7': ['CHB'], '8': ['DHB']}, strain)

def breed(strain):
	return au.group_of({'ROSS': ['AP95', 'APN', '344', 'ROM'], 'HUBBARD': ['F47', 'F72', 'M35', 'M65', 'M77']}, strain)

def join_hatch_and_dispatch(hatch, dispatch, on=['HATCH_DATE', 'STRAIN_CODE']):
	#hatch['LINE'] = hatch['STRAIN_CODE'].map(line)
	print(hatch)
	print(dispatch)
	dispatch = dispatch.reset_index()
	dispatch = dispatch.assign(**{'SALEABLE_DISPATCHED': pd.to_numeric(dispatch.loc[dispatch['LINE'] != 'A']['TO_CHICKS_DISPATCHED'])})
	dispatch = dispatch.assign(**{'BY_PRODUCT_DISPATCHED': pd.to_numeric(dispatch.loc[dispatch['LINE'] == 'A']['TO_CHICKS_DISPATCHED'])})
	dispatch['LINE'] = dispatch['STRAIN_CODE'].map(line) #Turn order line into line
	dispatch = dispatch[on + ['TO_CHICKS_DISPATCHED', 'SALEABLE_DISPATCHED', 'BY_PRODUCT_DISPATCHED']]
	#dispatch = dispatch.sort_values(by=on)
	#hatch = hatch.sort_values(by=on)
	dispatch = dispatch.groupby(by=on).sum(numeric_only = True).reset_index()
	hatch = hatch.groupby(by=on).sum(numeric_only = True).reset_index()
	result = hatch.set_index(on).join(dispatch.set_index(on)).reset_index()
	result['LEFTOVER'] = result['SALEABLE'] - result['SALEABLE_DISPATCHED']
	result['PRIME'] = result['SALEABLE'] + result['PRIME_CULLS']
	result['BY_PRODUCT'] = result['TO_CHICKS'] - (result['PRIME'] + result['PRE_SEX_CULLS'])
	result['BY_PRODUCT_LEFTOVER'] = result['BY_PRODUCT'] - result['BY_PRODUCT_DISPATCHED']
	return result
