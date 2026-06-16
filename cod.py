import pandas as pd
import numpy as np

tabela = pd.read_csv('demandas_time3.csv', sep=',')

#Definição das colunas que precisam ser transformadas em data e hora
colunas = ['created_date', 'last_modified_date']

for col in colunas:
    #Transforma o texto direto em Data/Hora
    tabela[col] = pd.to_datetime(tabela[col], errors='coerce')
    
    #Remove os microssegundos (a tabela veio com isso formatado)
    tabela[col] = tabela[col].dt.floor('s')
    
    #Remove o fuso horário (UTC), deixando a data "limpa"
    tabela[col] = tabela[col].dt.tz_localize(None)

#Remove as linhas vazias da coluna
tabela = tabela.dropna(subset=['case_number'])

#Linha para saber se existem duplicadas na coluna (FALSE = existe; TRUE = não existe)
print(tabela['case_number'].is_unique)

#Transforma a coluna em número inteiro
tabela['case_number'] = tabela['case_number'].astype(int)

#Remove os casos duplicados, mantendo apenas a primeira vez que o número aparece
tabela = tabela.drop_duplicates(subset=['case_number'], keep='first')

#Comparação numérica dos temas -------------------------------
#contador dos temas (ordenando do maior para o menor)
qnt_tema = tabela['theme'].value_counts().reset_index()

#Qual fila tem mais demanda -----------------------------------
#criamos uma segunda tabela para não mexer na original
tabela_nova = tabela[['created_date', 'queue', 'category']].copy()

#Linha para criar uma coluna no formato mes e ano
tabela_nova['mes_ano'] = tabela_nova['created_date'].dt.strftime('%m/%y')

#filtro para os 4 meses
filtro_mes = tabela_nova.loc[tabela_nova['mes_ano'].isin(['01/26', '02/26', '03/26', '04/26'])]

#agrupamento e contagem dos casos das filas
graf_fila = filtro_mes.groupby(['mes_ano', 'queue']).size().reset_index(name='quantidade').sort_values(by='mes_ano')

#Qual categoria mais apareceu nos últimos 4 meses --------------------------------------
#Filtro para contar as categorias
graf_categoria = filtro_mes['category'].value_counts()

#Qnt total de demandas --------------------------------------------
total_dem = tabela['case_number'].count()

#Qual fila mais recebe caso -------------------------------
qnt_total_fila = tabela['queue'].value_counts().reset_index()

#Total de erros na tabela ---------------------------------
#Pegamos somente oq é igual a - na tabela e somamos tudo
total_erros = (tabela == '-').sum().sum()

#Tranformação do df em csv
#tabela.to_csv("tabela.csv", index=False, sep=",", decimal=".")
