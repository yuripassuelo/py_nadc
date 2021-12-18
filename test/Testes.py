
import sys

sys.path.append(r'C:\Users\T-Gamer\Desktop\pynad\src\pynad')

import pynad

pnad_20_01 = pynad.micro_data('2020','1')

"""
Calculando Rendas Habituais e Efetivas Reais

@VD4020 = Renda Efetiva
@VD4019 = Renda Habitual


@Habital = Deflator Renda Habitual
@Efetiva = Deflator Renda Efetiva


"""

result = pnad_20_01[['UF','V1028','VD4019','VD4020','Habitual','Efetivo']].\
    assign( Renda_Habitual_Nom  = lambda x: x['VD4019']*x['V1028']/1000000,
           
            Renda_Efetiva_Nom   = lambda x: x['VD4020']*x['V1028']/1000000,
            
            Renda_Habitual_Real = lambda x: x['Renda_Habitual_Nom']*x['Habitual'],
            
            Renda_Efetiva_Real  = lambda x: x['Renda_Efetiva_Nom']*x['Efetivo']).\
    drop(['VD4019','VD4020','Habitual','Efetivo'], axis=1).groupby(['UF'], as_index= False ).sum()
  

"""
Construção da Piramide Etaria Brasileira

Periodo: 1º Trimestre de 2020


"""


idade_pnad = pnad_20_01[['V2009','V2007','V1028']].groupby(['V2009','V2007'], as_index = False ) .sum()

def classifica_idade( vector ):
    
    cat = [ "80 anos ou mais" if i == 80 else str(i)+" a "+str(i+4)+" anos" for i in range(0,81,5)]

    lista = [ [80,110] if i == 80 else[i,i+4] for i in range(0,81,5)]
    
    saida = []
    
    for i in range(0,len(vector)):
        
        for j in range(0,len(lista)):
            
            if vector[i] >= lista[j][0] and vector[i] <= lista[j][1]:
                
                saida.append( cat[j])
    
    return saida

idade_pnad['Class'] = classifica_idade( idade_pnad['V2009'])


fim = idade_pnad.drop(['V2009'], axis= 1).groupby(['Class','V2007'],as_index = False ).sum().\
        pivot( index= 'Class', columns= 'V2007', values= 'V1028').\
        rename(columns = {1:"Masculina",2:"Feminina"}).\
        assign( Feminina = lambda x: x['Feminina']*(-1))

fim.reset_index(inplace=True)

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

clas = [ "80 anos ou mais" if i == 80 else str(i)+" a "+str(i+4)+" anos" for i in range(0,81,5)]

sns.barplot( x='Masculina', y='Class' , data= fim, order= clas[::-1], color= '#CCCCFF' )
sns.barplot( x='Feminina' , y='Class' , data= fim, order= clas[::-1], color= '#F79E9A' )
plt.show()


"""
Calculo Curva de GINI

- Filtro Apenas Maiores de 18

- Retirando observações com dados de Renda Efetiva 'N/A'

"""



gini = pnad_20_01.loc[ (pnad_20_01['V2009'] >= 18) &
                       (pnad_20_01['VD4020']).notna() ,['V1028','VD4020']].\
        assign( VD4020    = lambda x: x['VD4020'].fillna(0)).sort_values(['VD4020'], 
                                                                         ascending = True).\
        assign( share_pop = lambda x: np.cumsum(x['V1028'])/sum(x['V1028']) ,
                
                share_inc = lambda x: np.cumsum(x['VD4020'])/sum(x['VD4020']),
                
                perc      = lambda x: 1/len(x['V1028']),
                
                Base      = lambda x: np.cumsum( x['perc'] ) )
        


plt.plot( gini['share_pop'], gini['share_inc'])
plt.plot( gini['Base'],gini['Base'], color = 'black', linestyle='--')
plt.xlabel("Percentual da População")
plt.ylabel("Percentual da Renda")
plt.title("Curva de Gini 1 trimestre 2020")
plt.show()

"""
Calculando taxa de desocupação por UF

Variavel de Classificação: 
    - VD4001 - Condição em relação a força de trabalho (PIA e PINA);
    - VD4002 - Condição de Ocupação (PEA e PEI);
    
Desemprego:
    - PEI/PIA (%)


"""


import pandas as pd

df = pd.concat([pnad_20_01[['UF','VD4001','V1028']].groupby(['UF','VD4001'],as_index = False).sum().\
            pivot( index= 'UF', columns= 'VD4001', values= 'V1028').\
            rename(columns= {1.0:"PIA",2.0:"PINA"}),
           pnad_20_01[['UF','VD4002','V1028']].groupby(['UF','VD4002'],as_index = False).sum().\
            pivot( index= 'UF', columns= 'VD4002', values= 'V1028').\
            rename(columns= {1.0:"PEA",2.0:"PEI"})], axis = 1).\
    assign( Desemprego = lambda x: x['PEI']/x['PIA'] )
    
df.reset_index(inplace=True)
    
sns.barplot( x = 'UF', y = 'Desemprego', data = df, color= "blue" )




