import pandas as pd
import os
import re




# Project Files
from inspecao_lib import download_file, show_input_box,sanitize_file_name, extract_file_name_url, create_dir

def get_files_form(cache_folder, excel_file_path, unidade, cod_pdf, cod_inspec):
    """
    Baixa arquivos PDF e seus anexos com base nas entradas do formulário em arquivo Excel e parâmetros fornecidos.

    Args:
        cache_folder (str): O diretório base para os arquivos excel com as entradas do formulário.
        excel_file_path (str): O caminho para o arquivo Excel contendo os dados do formulário.
        unidade (str): O valor usado para criar a pasta de download.
        cod_pdf (str): O código usado para determinar o caminho do arquivo PDF do formulário.
        cod_inspec (str): O código de inspeção usado para filtrar os dados no arquivo Excel.

    Raises:
        FileNotFoundError: Se o arquivo Excel não for encontrado no caminho especificado.

    """
    
    #Define a folder to download form in pdf in created folder named with value of 'unidade'
    download_path =  cache_folder + '\\' + unidade + '\\'
    create_dir(download_path)   

    # Read Excel form entries to set parameters of data management of each form
    if os.path.exists(excel_file_path):
        df_form = pd.read_excel(excel_file_path)
        df_form.rename(columns={'Informe o código enviado ao seu tribunal para continuar:':'cod_inspecao',
                                'ID da Entrada':'id_entrada'}, inplace=True)
    else:
        print('Erro na leitura dos registros do formulário.')

#'Unidade inspecionada':'unidade_inspecionada'
    # Filter rows by cod_inspecao
    filter_df = df_form[df_form['cod_inspecao'] == cod_inspec]
    print('Total de registros encontrados: ' + str(len(filter_df)))

    # Download form pdf by looping over a dataframe and handle form's data for each form
    if len(filter_df) > 0:
        for index, row in filter_df.iterrows():
            id_entrada = str(row.id_entrada)
            nome_unidade = str(row.iloc[9])

            # In code below, row..iloc[] is the index of column 'Unidade inspecionada'
            match cod_pdf:
                case '65270dab80304': # 01.Presidência
                    file_name = 'Formulário Presidência - ' + id_entrada + '.pdf'
                case '65270e3454ce2':  # 02.Vice-Presidência
                    file_name = 'Formulário Vice-Presidência - ' + id_entrada + '.pdf'
                case '65270edd68479': # 03.Presidência de Sessões
                    file_name = 'Formulário' + ' - ' + nome_unidade + ' - ' + id_entrada + '.pdf'
                case '65270f2475acd': # 04.Gabinete de Desembargador
                    file_name = 'Formulário' + ' - ' + nome_unidade + ' - ' + id_entrada + '.pdf'
                case '65270f77e965f': # 05.Gabinete de Desembargador Presidente
                    file_name = 'Formulário' + ' - ' + nome_unidade + ' - ' + id_entrada + '.pdf'
                case '65270fc85fbd4': # 06.Gabinete de Desembargador Vice-Presidente
                    file_name = 'Formulário' + ' - ' + nome_unidade + ' - ' + id_entrada + '.pdf'
                case '6527100f143d4': # 07.Corregedoria
                    file_name = 'Formulário' + ' - ' + nome_unidade + ' - ' + id_entrada + '.pdf'
                case '663e764bdf295': # 08.Desemb. Corregedor
                    file_name = 'Formulário' + ' - ' + nome_unidade + ' - ' + id_entrada + '.pdf'
                case '6527104195a66': # 09.Precatórios
                    file_name = 'Formulário' + ' - ' + nome_unidade + ' - ' + id_entrada + '.pdf'
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
                    file_name = 'Formulário' + ' - ' + id_entrada + '.pdf'

            # Replace invalid character form windows file name
            file_name = sanitize_file_name(file_name)

            # download a form in pdf file
            download_file('https://formularios-corregedoria.cnj.jus.br/pdf/' + cod_pdf + '/' + id_entrada + r"/download/", download_path, file_name)

            #Download all files atached in forms
            pattern = r'\d+\.\d+'
            for field_name, field_value in row.items():
                matches = re.findall(pattern, field_name)
                dir_name = 'não_numerado'
                if len(matches)>=1:
                    dir_name = 'Anexo_Item_' + matches[0]
                file_sub_path = os.path.join(download_path, dir_name)
                
                search_string = 'https://formularios-corregedoria.cnj.jus.br/index.php?gf-download'
                multi_files_str = 'Múltiplos arquivos:'
            
                if multi_files_str in str(field_value):
                    cleaned_field_value = re.sub(r'\s+','',str(field_value)) # remove white spaces.
                    cleaned_field_value = re.sub('Múltiplosarquivos:', '', cleaned_field_value)
                    url = cleaned_field_value.split(',')
                elif search_string in str(field_value):
                    url = [field_value]
                else:
                    url = []    
                
                if len(url) > 0:
                    for item_url in url:
                        print('url for extract_name = ' + item_url)
                        file_name = extract_file_name_url(item_url) # Extract file name from givem url
                        try:
                            download_file(item_url, file_sub_path, file_name)
                        except:
                            continue