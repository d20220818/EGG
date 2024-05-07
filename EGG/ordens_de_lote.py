from EGG.hatchery import *

def gerar_relatorio(df, df2, df3): #args = NASCIMENTO, DESPACHO, SOBRAS

	df3.rename(columns = {'QTY': 'SOBRA DE PH'}, inplace=True)

	df = join_hatch_and_dispatch(df, df2, ['HATCH_DATE', 'STRAIN_CODE'])
	df = df.set_index(['HATCH_DATE', 'STRAIN_CODE']).join(df3.set_index(['HATCH_DATE', 'STRAIN_CODE'])).reset_index()
	df = df.fillna(0)


	df = df[['HATCH_DATE', 'STRAIN_CODE', 'SALEABLE_DISPATCHED', 'BY_PRODUCT_DISPATCHED', 'SALEABLE', 'TO_CHICKS', 'PRE_SEX_CULLS', 'PRIME_CULLS', 'SOBRA DE PH']]

	df['MATRIZ NASCIDA'] = df['SALEABLE'] + df['PRIME_CULLS']
	df['PH NASCIDO'] = df['TO_CHICKS'] - (df['MATRIZ NASCIDA'] + df['PRE_SEX_CULLS'])
	df['DESCARTE MISTO'] = df['PRE_SEX_CULLS']
	df['TOTAL NASCIDO'] = df['MATRIZ NASCIDA'] + df['PH NASCIDO'] + df['DESCARTE MISTO']


	df['SOBRA DE MATRIZ'] = df['SALEABLE'] - df['SALEABLE_DISPATCHED'] #EQUAL TO df['MATRIZ NASCIDA'] - (df['SALEABLE_DISPATCHED'] + df['PRIME_CULLS'])



	df.rename(columns = {'HATCH_DATE': 'NASCIMENTO', 'STRAIN_CODE': 'LINHA', 'SALEABLE_DISPATCHED': 'MATRIZ FATURADA', 'SALEABLE': 'MATRIZ SEM ERROS', 'BY_PRODUCT_DISPATCHED': 'PH FATURADO', 'PRIME_CULLS': 'MATRIZ COM ERROS'}, inplace=True)

	df['PH SEM ERROS'] = df['PH FATURADO'] + df['SOBRA DE PH']
	df['PH COM ERROS'] = (df['PH NASCIDO'] + df['SOBRA DE MATRIZ']) - df['PH SEM ERROS']

	df = df[['NASCIMENTO', 'LINHA', 'MATRIZ FATURADA', 'PH FATURADO', 'MATRIZ NASCIDA', 'PH NASCIDO', 'DESCARTE MISTO', 'TOTAL NASCIDO', 'MATRIZ SEM ERROS', 'PH SEM ERROS', 'MATRIZ COM ERROS', 'PH COM ERROS', 'SOBRA DE MATRIZ', 'SOBRA DE PH']]
	return df