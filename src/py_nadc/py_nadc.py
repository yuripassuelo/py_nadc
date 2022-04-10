"""
Autor: Yuri Passuelo
Versao: v0.1
Data: 10/02/2022

Bibliotecas Linkadas no Arquivo:
    
@pandas
@numpy
@requests
@tqdm
@zipfile
@io
@tempfile
"""

import pandas as pd
import numpy as np
import requests
import tqdm
import zipfile
import os
import tempfile
import itertools 

from bs4 import BeautifulSoup



"""
Funcao de Auxilio de listagem dos arquivos presentes em diretorios:
    
@url = URL relativo ao diretorio de arquivos.

"""

def listFD(url: str, ext=''):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    return [ node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]
            
"""
Funcao para achar strings em uma lista de Strings:
    
@string = String que sera buscada;
@vector = Lista de valores em String.

"""

def get_str_index( string: str, vector: str ):
    return np.where( list(map( lambda x: string in x, 
                     vector ) ))[0][0]

"""
Funcao que checa se nomes podem ser interpretados como integer

@string = String nome.
"""

def check_names( string: str ):
    ex = [ i for i in string ][0:len(string)-1]
    try:
        if int( "".join(ex) ):
            return True
    except:
        return False
 
'''
Lista todos os periodos Disponiveis

@ No parameters needed

Funcao que lista todos os periodos em forma de dicionario, aonde as `keys` sao os anos, e os trimestres estao em formato
de lista

>>> list_periods( )
{'2012': ['01', '02', '03', '04'], 
 ... }

'''

def list_periods( ):
    main_url = r'https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Trimestral/Microdados/'
    years = list( filter( lambda x: check_names( x ), listFD( main_url ) ) )
    return { y[0:4] : [ int(i[6:8]) for i in list( filter( lambda x: "PNADC" in x, listFD( main_url+y ) ) ) ] for y in years }

'''
Checa se um determinado periodo esta disponivel

@year - Integer - Parametro relativo ao ano de interesse
@tri  - Integer - Parameter relativo ao trimestre de interesse

Funcao que checa se periodo existe, dado input de ano e trimestre

>>> check_period( ano = 2020, tri = 1 )
True

>>> check_period( ano = 2050, tri = 1 )
False

>>> check_period( ano = "2020", tri = 1 )
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 3, in check_period
ValueError: Parametro 'ano' nao e do tipo integer

>>> check_period( ano = 2020, tri = "1" )
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 5, in check_period
ValueError: Parametro 'tri' nao e do tipo integer

>>> check_period( 2011, 1 )   
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 7, in check_period
ValueError: Parametro 'ano' Inferior a 2012
'''

def check_period( ano : int, tri : int ):
    if type( ano ) != int:
        raise ValueError("Parametro 'ano' nao e do tipo integer")
    if type( tri ) != int:
        raise ValueError("Parametro 'tri' nao e do tipo integer")
    if ano < 2012:
        raise ValueError("Parametro 'ano' Inferior a 2012")
    if tri not in [1, 2, 3, 4]:
        raise ValueError("Parametro 'tri' fora do intervalo")
    dict_period = list_periods()
    if str( ano ) in dict_period.keys() :
        if tri in dict_period[str(ano)] :
            return True
    return False

"""
Funcao de Download de arquivos com barra de progresso

@url = URL do arquivo a ser baixado, o endereco pode incluir o nome do arquivo em seu final
@filename = (opicional) nome do arquivo, caso o enderaco URL ja possua o nome do arquivo nao e necessario o prenchimento
@verbose = (opicional)


Cria diretorio temporario para salvar base PNAD baixada
"""

def download_file(url, filename=False, verbose = False):

    #dir = tempfile.mkdtemp()

    if not filename:
        local_filename = os.path.join(".",url.split('/')[-1])
    else:
        local_filename = os.path.join(filename,url.split('/')[-1])
    r = requests.get(url, stream=True)
    file_size = int(r.headers['Content-Length'])
    chunk = 1
    chunk_size=1024
    num_bars = int(file_size / chunk_size)
    if verbose:
        print(dict(file_size=file_size))
        print(dict(num_bars=num_bars))

    with open(local_filename, 'wb') as fp:
        for chunk in tqdm.tqdm(
                                    r.iter_content(chunk_size=chunk_size)
                                    , total= num_bars
                                    , unit = 'KB'
                                    , desc = local_filename
                                    , leave = True # progressbar stays
                                ):
            fp.write(chunk)
    return 
    

"""
Download dos Microdados:
    
@ano       = Ano relativo a pesquisa (Disponivel apartir de 2012);
@tri       = Trimestre relativo a pesquisa parametro pode ir de '1','2','3','4'.
@directory = Diretorio de saída dos arquivos baixados - Padrão é usar diretorio temporario

Valores dos parametros devem ser consultados antes de aplicados, caso sejam
Repassados parametros relativos a pesquisas ainda nao existentes menssagens
de erros serao retornadas avisando da indisponibilidade da pesquisa.

"""

def get_pnadc( ano: int, tri: int, directory = None ):
    
    # Parametros URL

    url_principal = r'https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/'
    
    url_dic = url_principal+'Trimestral/Microdados/Documentacao/'
    
    # Conferes de Parametros Inputados

    if check_period( ano, tri) == False:
        raise ValueError("Periodo "+str(ano)+" "+str(tri)+" nao disponivel, consulte a funcao `list_periods( )`" )

    # URL Microdados

    url_md = url = url_principal+'Trimestral/Microdados/'+str(ano)+'/'
        
    # Cria dicionario com nome de arquivos

    dict_nam = { "pnad_file": listFD(url)[ get_str_index( 'PNADC_0'+str(tri)+str(ano), listFD(url) )],
                 "dict_file": listFD(url_dic)[get_str_index( 'Dicionario',  listFD(url_dic) )],
                 "def_file": listFD(url_dic)[get_str_index( 'Deflatores',  listFD(url_dic) )]} 

    # Cria pasta temporaria

    if directory != None:
        if os.path.exists( directory ):

            str_path = [ l for l in directory ]

            last_str = str_path[ len( str_path ) - 1 ]

            if "\\" in last_str or "/" in last_str:
                dir = directory 

            else :
                dir = directory + "/"

    if directory == None or not os.path.exists( directory ):
        dir = tempfile.mkdtemp()+"/"

    # Download Arquivo Microdados Pnad
    
    print( 'Tentando Link Principal "' + url_md + dict_nam['pnad_file'] + '" ...' )
    print("")
    
    download_file( url_md + dict_nam['pnad_file'], filename = dir )
    
    result = zipfile.ZipFile( open( dir+dict_nam['pnad_file'],'rb') )
    
    
    print( 'Arquivo "'+ dict_nam['pnad_file'] +'" Baixado com sucesso')
    print("")
    
    # Download Dicionario
    
    print( 'Tentando Link principal do Dicionario ' + url_dic + dict_nam['dict_file'])
    print("")
    
    download_file( url_dic + dict_nam['dict_file'], filename = dir )
    
    dic_zip = zipfile.ZipFile( open( dir+dict_nam['dict_file'],'rb') )
    
    
    print( 'Arquivo "' + dict_nam['dict_file'] ,'" Baixado com Sucesso' )
    print("")
    
    
    dicionario = pd.read_excel( dic_zip.open(dic_zip.namelist()[get_str_index( 'dicionario', 
                                                                dic_zip.namelist())]),
                                header = 1 ).drop( [0,1], axis = 0)
    
    # Download Deflatores
    
    download_file( url_dic + dict_nam['def_file'], filename = dir )
    
    def_zip = zipfile.ZipFile( open( dir+dict_nam['def_file'],'rb') )
    
    
    print( 'Arquivo "' + dict_nam['def_file'] ,'" Baixado com Sucesso' )
    print("")
    
    deflatores = pd.read_excel( def_zip.open(def_zip.namelist()[0]))
    
    def_dict = { '1' : '01-02-03',
                 '2' : '04-05-06',
                 '3' : '07-08-09',
                 '4' : '10-11-12'}
    
    
    # Extração dos Microdados
    # Etapa mais demorada uma vez que é feita por meio de função fwf

    # Pega nome da coluna de código da variavel

    poss_names = ["Codigo","Código","codigo","código"]

    vec_bool = [ np.any( [ t in w for t in poss_names ] ) for w in list( dicionario.columns ) ]
    
    var_name = list( itertools.compress( list( dicionario.columns ), vec_bool ) )

    #print( list( map(int,dicionario['Tamanho'].dropna()) ) )
    #print( np.unique( dicionario[var_name].dropna() ) )
    
    print( 'Extraindo Microdados...')
    print("")
    
    micro_dta = pd.read_fwf( result.open( result.namelist()[0] ),
                             widths = list( map(int,dicionario['Tamanho'].dropna()) ) ,
                             names  = dicionario[var_name[0]].dropna().unique() )
    
    ### Cruzando Deflatores com Microdados
    
    micro_dta = micro_dta.merge( 
                     deflatores.loc[ (deflatores['trim'] == def_dict[str(tri)])&
                                     (deflatores['Ano'] == ano )].\
                     drop(['Ano','trim'], axis = 1), 
                     how = "left",
                     on = "UF")
    
    print( "Extracao Completa")

    return micro_dta
