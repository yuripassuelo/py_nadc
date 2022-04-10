# O que é
Pynad é um pacote que facilita o acesso as microdados trimestrais da PNAD Continua, ao utilizá-lo você obterá os microdados ja tratados da PNAD Continua contendo os valores de acordo com o dicionário e com a inclusão dos deflatores para cálculo de rendimentos reais.

Para mais informações a respeito da pesquisa acessar:
https://www.ibge.gov.br/estatisticas/sociais/populacao/9171-pesquisa-nacional-por-amostra-de-domicilios-continua-mensal.html?=&t=o-que-e

Para consultar o repositório de pesquisas PNAD do IBGE acessar:
https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/

# Instalação

Atualmente o pacote se encontra em versão de testes e está sujeito a melhorias continuas, o pacote pode ser baixado e testado via TestPyPi.
:fa-windows:
```
pip install -i https://test.pypi.org/simple/ py-nadc-yuripassuelo

```
:fa-linux:/:fa-apple:
```
python3 -m pip install --index-url https://test.pypi.org/simple/ py-nadc-yuripassuelo
```
# Utilização

A utilização do pacote deve seguir de acordo com a disponibilização dos dados da PNAD, portanto, caso haja a tentativa de importação de uma pesquisa ainda não efetuada e indisponível, ou de um período anterior ao realizado pela PNAD mensagens de erro serão mostradas indicando que os parâmetros selecionados não localizaram a pesquisa de referência.

```py
# importando biblioteca

>>> import py_nadc

>>> pnad_20_01 = py_nadc.get_pnadc(2020,1)
>>> pnad_20_01.head()

    Ano  Trimestre  UF  Capital  RM_RIDE        UPA  ...    V1028197    V1028198    V1028199  V1028200  Habitual   Efetivo
0  2020          1  11     11.0      NaN  110000016  ...  134.165977  247.795500  258.208202       0.0  1.123105  1.124706
1  2020          1  11     11.0      NaN  110000016  ...  134.165977  247.795500  258.208202       0.0  1.123105  1.124706
2  2020          1  11     11.0      NaN  110000016  ...  134.165977  247.795500  258.208202       0.0  1.123105  1.124706
3  2020          1  11     11.0      NaN  110000016  ...  134.165977  247.795500  258.208202       0.0  1.123105  1.124706
4  2020          1  11     11.0      NaN  110000016  ...  125.504237  227.923366  232.363250       0.0  1.123105  1.124706
```
O resultado desse exemplo será um objeto pandas data frame e que, portanto, este pode ser manipulado com os seus respectivos atributos.

Os resultados contemplam todos os valores de forma já deflacionada pelos índices disponibilizados pelo IBGE, para o cálculo dos rendimentos agregados ou desagregados, ou da estimativa populacional é necessario utilizar-se dos pesos disponibilizados pelo IBGE, os pesos correspondem pelas variáveis `V1027`, `V1028`, `V1029` e `V1033`.

# Diretórios

Ao realizar a utilização da função `get_pnadc` é possível apontar um diretório de saída dos arquivos `PNADC`, `Deflatores` e 	`Dicionários`, como no exemplo abaixo, caso o diretório não seja apontado, uma pasta temporaria será criada na memória e os arquivores serão salvos nela.

``` python
>>> import py_nadc
>>> import os

>>> teste = py_nadc.get_pnadc( 2020, 1, r"./Pasta_Dicas/" )

>>> os.listdir( r"./Pasta_Dicas/" )
['Deflatores.zip', 'Dicionario_e_input_20220224.zip','PNADC_012020_20220224.zip']

```

# Deflatores

Para o calculo dos Rendimentos habituais e Efetivos reais é necessario deflacionar os valores, para isso é necessario utilizar as colunas `Habitual` e `Efetivo`, como mostrado no exemplo abaixo, aonde é calculada a renda Habitual e Efetiva real e nominal a nível Brasil.

```python

>>>
>>>
>>>


```


Para dúvidas, sugestões entre em contato:

:email:  e-mail       : yuri.mpassuelo@gmail.com
:briefcase: linkedin : https://br.linkedin.com/in/yuri-passuelo-39759412b
:computer: github  : yuripassuelo.github.io