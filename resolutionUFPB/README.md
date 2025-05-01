# 📌 Webscraping UFPB Resolutions


Here we performed a web scraping on ufpb resolutions, available here "https://sigrh.ufpb.br/sigrh/public/colegiados/filtro_busca.jsf".

The web scraping is found in the scraper.py file.

Additionally the data was processed:
    Converts non-standard files, transforms HTML into PDF, performs OCR of non-editable PDFs. The UFPB resolutions database is not standardized, containing files in PDF, non-editable PDF, HTML, HTM, DOC, requiring standardization to PDF.


Used libriries:

    requests
    selenium
    playwright
    glob


    
    webscraping/
    │
    ├── resolutionUFPB/
    │   ├── scraper.py: scraper
    |   ├── download_functions.ipynb: donwload functions used in scraper
    |   ├── create_collection_functions.py: save data in ChromaDB storage
    |   ├── fix_file_type: verify if is a .docx file and not pdf and transforms files that are docs but named in pdf into .docx
    |   ├── html_to_pdf: transform files in html to pdf during scraping
    |   ├── ocr.py: transform non-editable pdf into editable pdf
    │   ├── requirements.txt
    |   ├── README.md
    │

