import time
from datetime import datetime
import requests
import pandas as pd
import os
import tkinter as tk
from tkinter import simpledialog


# Project Files
from inspecao_lib import download_file, show_input_box,sanitize_file_name, extract_file_name_url, create_dir

def get_files_form(cache_folder, file_path, unidade, cod_pdf, cod_inspec):
    
    #Define a folder to download form in pdf in created folder named with value of 'unidade'
    download_path =  cache_folder + '\\' + unidade + '\\'
    create_dir(download_path)   

    # Read Excel form entries to set parameters of data management of each form
    if os.path.exists(file_path):
        df_form = pd.read_excel(file_path)
        df_form.rename(columns={'Informe o código enviado ao seu tribunal para continuar:':'cod_inspecao',
                                'ID da Entrada':'id_entrada'}, inplace=True)
        print('Total de registros carregados: ' + str(len(df_form)))
    else:
        print('Erro na leitura dos registros do formulário.')

#'Unidade inspecionada':'unidade_inspecionada'
    # Filter rows by cod_inspecao
    filter_df = df_form[df_form['cod_inspecao'] == cod_inspec]

    # Download form pdf by looping over a dataframe and handle form's data for each form
    for index, row in filter_df.iterrows():
        id_entrada = str(row.id_entrada)

        # In code below, row..iloc[] is the index of column 'Unidade inspecionada'
        match cod_pdf:
            case '65270dab80304': # 01.Presidência
                file_name = 'Formulário Presidência - ' + id_entrada + '.pdf'
            case '65270e3454ce2':  # 02.Vice-Presidência
                file_name = 'Formulário Vice-Presidência - ' + id_entrada + '.pdf'
            case '65270edd68479': # 03.Presidência de Sessões
                file_name = 'Formulário' + ' - ' + row.iloc[9] + ' - ' + id_entrada + '.pdf'
            case '65270f2475acd': # 04.Gabinete de Desembargador
                file_name = 'Formulário' + ' - ' + row.iloc[9] + ' - ' + id_entrada + '.pdf'
            case '65270f77e965f': # 05.Gabinete de Desembargador Presidente
                file_name = 'Formulário' + ' - ' + row.iloc[9] + ' - ' + id_entrada + '.pdf'
            case '65270fc85fbd4': # 06.Gabinete de Desembargador Vice-Presidente
                file_name = 'Formulário' + ' - ' + row.iloc[9] + ' - ' + id_entrada + '.pdf'
            case '6527100f143d4': # 07.Corregedoria
                file_name = 'Formulário' + ' - ' + row.iloc[9] + ' - ' + id_entrada + '.pdf'
            case '663e764bdf295': # 08.Desemb. Corregedor
                file_name = 'Formulário' + ' - ' + row.iloc[9] + ' - ' + id_entrada + '.pdf'
            case '6527104195a66': # 09.Precatórios
                file_name = 'Formulário' + ' - ' + row.iloc[9] + ' - ' + id_entrada + '.pdf'
            case '652710d67fbd9': # 10.Outorga delegações - extrajudicial
                file_name = 'Formulário Outorga Delegações' + ' - ' + id_entrada + '.pdf'
            case '6527108a86e59': # 11.Secretarias 2Grau
                file_name = 'Formulário' + ' - ' + row.iloc[8] + ' - ' + id_entrada + '.pdf'
            case '6527117094bc0': # 12.Serventias extrajudicial
                file_name = 'Formulário' + ' - ' + row.iloc[8] + ' - ' + id_entrada + '.pdf'
            case '652711bd7e878': # 13.Unidades 1 Grau
                file_name = 'Formulário' + ' - ' + row.iloc[8]+ ' - ' + id_entrada + '.pdf'    
            case '6527120b8514a': # 14.Unidades Administrativas
                file_name = 'Formulário' + ' - ' + row.iloc[14] + ' - ' + id_entrada + '.pdf'
            case '65147c4959bb9': # 15.TIC
                file_name = 'Formulário TIC' + ' - ' + id_entrada + '.pdf'
            case _:
                file_name = 'Não Informado'

        # Replace invalid character form windows file name
        file_name = sanitize_file_name(file_name)

        # download a form in pdf file
        download_file('https://formularios-corregedoria.cnj.jus.br/pdf/' + cod_pdf + '/' + id_entrada + r"/download/", download_path, file_name)

        #Download all files atached in forms
        for field_name, field_value in row.items():
            search_string = 'https://formularios-corregedoria.cnj.jus.br/index.php?gf-download'
            if search_string in str(field_value):
                dir_name = 'Anexo_Item_' + field_name.split('.')[0] + '.' + field_name.split('.')[1]
                file_sub_path = os.path.join(download_path, dir_name)
                url = field_value
                # Extract file name from givem url
                file_name = extract_file_name_url(url)
                try:
                    download_file(url, file_sub_path, file_name)
                except:
                    continue