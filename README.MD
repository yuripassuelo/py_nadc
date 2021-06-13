# O que é
Pynad é um pacote que facilita o acesso as microdados trimestrais da PNAD Continua, ao utilizá-lo você obterá os microdados ja tratados da PNAD Continua contendo os valores de acordo com o dicionário e com a inclusão dos deflatores para cálculo de rendimentos reais.

Para mais informações a respeito da pesquisa acessar:
https://www.ibge.gov.br/estatisticas/sociais/populacao/9171-pesquisa-nacional-por-amostra-de-domicilios-continua-mensal.html?=&t=o-que-e

Para consultar o repositório de pesquisas PNAD do IBGE acessar:
https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/

# Instalação


# Utilização

A utilização do pacote deve seguir de acordo com a disponibilização dos dados da PNAD, portanto, caso haja a tentativa de importação de uma pesquisa ainda não efetuada e indisponível, ou de um período anterior ao realizado pela PNAD mensagens de erro serão mostradas indicando que os parâmetros selecionados não localizaram a pesquisa de referência.

```py
# importando biblioteca

import pynad

pnad_20_01 = pynad.micro_data('2020','1')
```
O resultado desse exemplo será um objeto pandas data frame e que, portanto, pode ser manipulado com as respectivas propriedades.
