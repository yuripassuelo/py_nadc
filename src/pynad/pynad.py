
"""
Autor: Yuri Passuelo
Versão: v0
Data: 02/06/2021

Bibliotecas Linkadas no Arquivo:
    
@pandas
@numpy
@requests
@zipfile
@io


"""

import pandas as pd
import numpy as np
import requests
import zipfile
import io
import tqdm
import os

from bs4 import BeautifulSoup



"""
Função de Auxilio de listagem dos arquivos presentes em diretorios:
    
@url = URL relativo ao diretorio de arquivos.

"""


def listFD(url: str, ext=''):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    return [ node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]



"""
Função de Download de arquivos '.zip'

@url = URL Relativo ao arquivo que será baixado;
@fname = Nome do arquivo ZIP da PNAD a ser baixado.

"""

def download_pnad( url: str, fname: str):
    resp = requests.get(url+'/'+fname, stream=True)
    return zipfile.ZipFile(io.BytesIO(resp.content))
            
"""
Função para achar strings em uma lista de Strings:
    
@string = String que será buscada;
@vector = Lista de valores em String.

"""


def get_str_index( string: str, vector: str ):
    

    
    return np.where( list(map( lambda x: string in x, 
                     vector ) ))[0][0]


"""
Função de Download de arquivos com barra de progresso

@url = URL do arquivo a ser baixado, o endereço pode incluir o nome do arquivo em seu final
@filename = (opicional) nome do arquivo, caso o enderaço URL ja possua o nome do arquivo não é necessario o prenchimento
@verbose = (opicional)

"""

def download_file(url, filename=False, verbose = False):

    if not filename:
        local_filename = os.path.join(".",url.split('/')[-1])
    else:
        local_filename = filename
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
    
@ano = Ano relativo a pesquisa (Disponivel apartir de 2012);
@tri = Trimestre relativo a pesquisa parametro pode ir de '1','2','3','4'.

Valores dos parametros devem ser consultados antes de aplicados, caso sejam
Repassados parametros relativos a pesquisas ainda não existentes menssagens
de erros serão retornadas avisando da insdiponibilidade da pesquisa.

"""

def micro_data(ano, tri):
    
    url_principal = r'https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/'
    
    
    url = url_principal+'Trimestral/Microdados/'+ano+'/'
    
    url_dic = url_principal+'Trimestral/Microdados/Documentacao/'
    
    
    ### Conferes de Parametros Inputados
    
    if int(ano) < 2012:
        raise ValueError("Parametro 'Ano' Inferior a 2012")
        
    if int(tri) not in [1,2,3,4]:
        raise ValueError("Parametro 'Tri' Fora do Intervalo")
    
    if str(ano)+'/' not in listFD(url_principal+'Trimestral/Microdados/'):
        raise ValueError("Parametro 'Ano' não disponível")
        
    if sum([ 'PNADC_0'+tri+ano in i for i in listFD(url)]) == 0:
        raise ValueError("Parametro 'Tri' Selecionado Inexistente")
        
    
    ### Cria dicionario com nome de arquivos

    dict_nam = { "pnad_file": listFD(url)[ get_str_index( 'PNADC_0'+tri+ano, 
                                                          listFD(url) )],
                 "dict_file": listFD(url_dic)[get_str_index( 'Dicionario', 
                                                             listFD(url_dic) )],
                 "def_file": listFD(url_dic)[get_str_index( 'Deflatores', 
                                                             listFD(url_dic) )]} 

    ### Download Arquivo Microdados Pnad ###
    
    url = url_principal+'Trimestral/Microdados/'+ano+'/'
    
    print( 'Tentando Link Principal "' + url + dict_nam['pnad_file'] + '" ...' )
    print("")
    
    download_file( url + dict_nam['pnad_file'] )
    
    result = zipfile.ZipFile( open( dict_nam['pnad_file'],'rb') )
    
    
    print( 'Arquivo "'+ dict_nam['pnad_file'] +'" Baixado com sucesso')
    print("")
    
    ### Download Dicionario ###
    
    print( 'Tentando Link principal do Dicionario ' + url_dic + dict_nam['dict_file'])
    print("")
    
    download_file( url_dic + dict_nam['dict_file'])
    
    dic_zip = zipfile.ZipFile( open( dict_nam['dict_file'],'rb') )
    
    
    print( 'Arquivo "' + dict_nam['dict_file'] ,'" Baixado com Sucesso' )
    print("")
    
    
    dicionario = pd.read_excel( dic_zip.open(dic_zip.namelist()[get_str_index( 'dicionario', 
                                                                dic_zip.namelist())]),
                                header = 1 ).drop( [0,1], axis = 0)
    
    ### Download Deflatores ###
    
    download_file( url_dic + dict_nam['def_file'])
    
    def_zip = zipfile.ZipFile( open( dict_nam['def_file'],'rb') )
    
    
    print( 'Arquivo "' + dict_nam['def_file'] ,'" Baixado com Sucesso' )
    print("")
    
    deflatores = pd.read_excel( def_zip.open(def_zip.namelist()[0]))
    
    def_dict = { '1' : '01-02-03',
                 '2' : '04-05-06',
                 '3' : '07-08-09',
                 '4' : '10-11-12'}
    
    
    ### Leitura do Arquivo - Microdados ###
    
    
    print( 'Extraindo Microdados...')
    print("")
    
    micro_dta = pd.read_fwf( result.open( result.namelist()[0] ),
                             widths = list( map(int,dicionario['Tamanho'].dropna()) ) ,
                             names  = dicionario['Código\nda\nvariável'].dropna().unique() )
    
    ### Cruzando Deflatores com Microdados
    
    micro_dta = micro_dta.merge( 
                     deflatores.loc[ (deflatores['trim'] == def_dict[tri])&
                                     (deflatores['Ano'] == int(ano) )].\
                     drop(['Ano','trim'], axis = 1), 
                     how = "left",
                     on = "UF")
    
    print( "Extração Completa")
    

    return micro_dta

