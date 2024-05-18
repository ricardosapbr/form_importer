import time
from datetime import datetime
import requests
import pandas as pd
import os
import sys
from pathlib import Path

# Project Files
import inspecao_lib
import form_presidencia

# Setting a folder to download form files
links_file = r"\\fluor02\Corregedoria\_Restrito\Automacao\form_inspecao\links_formularios.txt"
user_folder = os.path.join(os.path.expanduser('~'), 'Documents')

cod_acesso = inspecao_lib.show_input_box('Informe o código da inspeção (Senha do Formulário)')
cod_acesso = cod_acesso.upper()

if cod_acesso == '':
    #inspecao_lib.show_message_box('Informe um código de inspeção!')
    sys.exit('ERRO: Informe um código de inspeção!')
 
default_folder = r"\Arquivos Formulários de Inspeção" + '\\' + cod_acesso
cache_folder = user_folder + default_folder

#Create path object
inspecao_lib.create_dir(cache_folder)

#Get all forms registry and save in cache_folder
df_forms = pd.read_csv(links_file) # Get the links to download form entries in Excel and other informations

for row in df_forms.itertuples():
    url = row.link # Url of form entries
    file_name = str(row.indice).zfill(2) + '.' + row.unidade + '.xlsx' # Given name do Excel form entries
        
    # Download each Excel form entries in cache_folder
    if inspecao_lib.download_file(url, cache_folder, file_name) == True: 
        # Set the parameters to get pdf form and handle data of each forms
        file_path = cache_folder + '\\' + file_name
        unidade = str(row.indice).zfill(2) + '.' + row.unidade
        form_presidencia.get_files_form(cache_folder, file_path, unidade, row.cod_pdf, cod_acesso)
    else:
        print('INFO: Falha ao baixar arquivo de registros do formulário')

print('ARQUIVOS BAIXADOS COM SUCESSO EM: ' + cache_folder)   


