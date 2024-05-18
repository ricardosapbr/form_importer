import requests
import os
import re
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox
from urllib.parse import urlparse, parse_qs
from pathlib import Path


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
        print('Iniciando o download em: ' + file_path)
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        #Create path, if not exists
        directory = Path(download_path) #Create path object
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)    
      
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
    download_url = download_url[0]
    return download_url.split('/')[-1]

# Create a dir using pathlib library
def create_dir(path):
    try:
        directory = Path(path) #Create path object
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
        return True    
    except:
        return False
