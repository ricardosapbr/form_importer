import pandas as pd
import os
import sys
from pathlib import Path

# Project Files
import inspecao_lib
import inspecao_importer

# Define quais registros de inspeção serão baixados
cod_acesso = inspecao_lib.show_input_box('Informe o código da inspeção (Senha do Formulário)')
cod_acesso = cod_acesso.upper()

# Setting a folder to download form files
user_folder = os.path.join(os.path.expanduser('~'), 'Documents')
cache_folder = user_folder + r"\Arquivos Formulários de Inspeção"

url_links = 'https://formularios-corregedoria.cnj.jus.br/wp-content/uploads/2024/05/links_formularios_inspecao.txt'
inspecao_lib.download_file(url_links, cache_folder,'links_formularios_inspecao.txt')
links_file = user_folder + r"\Arquivos Formulários de Inspeção" + r"\links_formularios_inspecao.txt"

# Links de teste
#links_file = user_folder + r"\teste_link_form.txt"
#links_file = user_folder + r"\links_formularios_inspecao.txt"

if cod_acesso == '':
    #inspecao_lib.show_message_box('Informe um código de inspeção!')
    sys.exit('ERRO: Informe um código de inspeção!')
 
inspecao_folder = cache_folder + '\\' + cod_acesso

#Create path object
inspecao_lib.create_dir(inspecao_folder)

#Get all forms registry and save in cache_folder
df_forms = pd.read_csv(links_file) # Read file with all links to access form entries in excel

for row in df_forms.itertuples():
    url = row.link # Url of form entries
    file_name = str(row.indice).zfill(2) + '.' + row.unidade + '.xlsx' # Given name for Excel form entries
        
    # Download each Excel form entries in cache_folder
    if inspecao_lib.download_file(url, cache_folder, file_name) == True: 
        # Set the parameters to get pdf form and handle data of each forms
        file_path = cache_folder + '\\' + file_name
        unidade = str(row.indice).zfill(2) + '.' + row.unidade
        inspecao_importer.get_files_form(inspecao_folder, file_path, unidade, row.cod_pdf, cod_acesso)
    else:
        print('INFO: Falha ao baixar arquivo de registros do formulário')

print('ARQUIVOS BAIXADOS COM SUCESSO EM: ' + inspecao_folder)
inspecao_lib.table.display()
input('Tecle enter para fechar o importador.')  


