import os
import magic #pip install python-magic-bin==0.4.14
from os import chdir, getcwd, listdir
from os.path import isfile

#Aqui passamos por todos os arquivos e verificamos se são PDFs ou DOCs, se for docx, convertemos para .docx

def fix_file_type(folder_path):
    # Cria um objeto para detectar o tipo de arquivo
    #mime = magic.Magic(mime=True)

    chdir(folder_path)

    # Itera sobre os arquivos na pasta
    for filename in os.listdir():
        
        #file_path = os.path.join(folder_path, filename)
        file_type = magic.from_buffer(open(filename, "rb").read(2048))
        
        # Mapeia tipos MIME para extensões
        if "PDF" in file_type:
            continue
        elif "Microsoft Word" in file_type:
            base = os.path.splitext(filename)[0]
            os.rename(filename, base + ".docx")
        else:
            print(f"Corrupted file: {filename}")
            continue

