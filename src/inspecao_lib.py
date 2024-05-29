import requests
import os
import re
import tkinter as tk
from tkinter import simpledialog, messagebox
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from tabulate import tabulate

class Table:
    def __init__(self, headers, colalign=None):
        """
        Initialize the table with headers and optional column alignment.

        :param headers: List of column headers
        :param colalign: List of alignments for each column (default is None)
        """
        self.headers = headers
        self.data = []
        self.colalign = colalign if colalign else ['center'] * len(headers)

    def add_row(self, row):
        """
        Add a row to the table.

        :param row: List of row values
        """
        if len(row) != len(self.headers):
            raise ValueError("Row length does not match headers length.")
        self.data.append(row)

    def display(self, table_format="pretty"):
        """
        Display the table in the console.

        :param table_format: String format for the table (default is "pretty")
        """
        print()
        print(tabulate(self.data, headers=self.headers, tablefmt=table_format, colalign=self.colalign))

    def get_table_str(self, table_format="pretty"):
        """
        Get the table as a string.

        :param table_format: String format for the table (default is "pretty")
        :return: String representation of the table
        """
        return tabulate(self.data, headers=self.headers, tablefmt=table_format, colalign=self.colalign)

# Download file in given url
def download_file(url, download_path, file_name=''):
    """
    Download a file from the given URL and save it to the specified path.

    Parameters:
    - url (str): The URL of the file to download.
    - path (str): The local path where the downloaded file will be saved.
    - file_name(str):  File name save
    """

    if len(file_name) != 0:
        file_path = os.path.join(download_path, file_name)
    else:
        file_path = download_path    

    try:
        #Create path, if not exists
        print('Criando o diretório: ' + download_path)
        create_dir(download_path)
                
        if isinstance(url, str):
            list_url = [url]
        else:
            list_url = url    

        for item_url in list_url:
            print('Iniciando o download em: ' + file_path)
            response = requests.get(item_url)
            response.raise_for_status()  # Raise an exception for HTTP errors
        
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print("File downloaded successfully: " + file_name)
            # write_log("File downloaded successfully: " + save_as, save_as)
            return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return False

# Show a input box and return given value
def show_input_box(text):

    # Create a tkinter window
    root = tk.Tk()

    # Hide the main window
    root.withdraw()

    texto_retorno = simpledialog.askstring('Formulários de Inspeção', text)

    if texto_retorno  is None:
        texto_retorno = ''
    
    # Destroy the tkinter window
    root.destroy()

    return texto_retorno

def show_message_box(text):
    # Create a Tkinter root window
    root = tk.Tk()

    # Hide the root window
    root.withdraw()

    # Show a message dialog
    messagebox.showinfo("Formulários de Inspeção", text)

    # Main event loop
    root.mainloop()

# Replace invalid characters in windows files names
def sanitize_file_name(file_name):
    # Define a regular expression pattern to match characters not allowed in Windows file names
    invalid_chars_pattern = r'[<>:"/\\|?*]'

    # Replace invalid characters with an underscore
    sanitized_name = re.sub(invalid_chars_pattern, '_', file_name)

    return sanitized_name

# Extract file name from form url
def extract_file_name_url(url):
    # Extract file name from givem url
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    download_url = query_params.get('gf-download')
    # Check if download_url is not None before accessing its elements
    if download_url:
        download_url = download_url[0]
        return download_url.split('/')[-1]
    else:
        return "falha_nome_arquivo.pdf"
    
# Create a dir using pathlib library
def create_dir(path):
    try:
        directory = Path(path) #Create path object
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
        return True    
    except Exception as e:
        print(e)
        return False
    
# Singleton Instance
table = Table(["Unidade", "Formulário Enviados"], colalign=['left', 'center'])