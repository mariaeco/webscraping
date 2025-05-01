#CONVERTENDO RESOLUCOES NAO ENDITAVEIS EM WORD
#RODAR ESTE ARQUIVO PARA TRANSFORMAR PDFS NAO EDITAVEIS EM WORDS EDITAVEIS

import glob
import win32com.client
import os
from docx import Document #python-docx
from docx.shared import Pt


def ocr(pdfs_path):
    #lista de resolucoes com pdfs nao editaveis
    list_resolutions = ['2007','2006','2005','2004','2003','2002','2000','1999','1998','1997','1996',
                        '046_2007','061_2008','033_2015','028_2015','029_2015',
                        '020_2019','024_2019','025_2019','034_2019','035_2019',
                        '038_2019','043_2019','47_2013']



    #pdfs_path = "./data/downloaded_files/" # folder where the .pdf files are stored
    converted = 0

    word = win32com.client.Dispatch("Word.Application")
    word.visible = 1

    
    for i, doc in enumerate(glob.iglob(pdfs_path+"*.pdf")):
        if any(resolution in os.path.basename(doc) for resolution in list_resolutions):
            filename = doc.split('\\')[-1]
            in_file = os.path.abspath(doc)
            wb = word.Documents.Open(in_file)
            out_file = os.path.abspath(pdfs_path+filename[0:-4]+ ".docx".format(i))
            wb.SaveAs2(out_file, FileFormat=16) # file format for docx
            print("File",filename ,"successful converted to .docx")
            wb.Close()
            
            # Now modify the font size using python-docx
            document = Document(out_file)
            
            # Define the font size you want (in points)
            new_font_size = Pt(10)  # Example: size 12 points
            
            # Iterate through all paragraphs and set the font size
            for para in document.paragraphs:
                for run in para.runs:
                    run.font.size = new_font_size
            
            # Save the modified DOCX file
            document.save(out_file)
            
            #DELETE PDF FILE
            file_delete = pdfs_path+filename
            os.remove(file_delete)  # Deleta o arquivo
            print("File",filename ,"successful deleted")
            converted += 1
            

    word.Quit()
    print("Total de arquivos convertidos: ",converted)
    
 