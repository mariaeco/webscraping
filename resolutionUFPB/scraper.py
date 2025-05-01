import os
import time
from create_collection_functions import * 

#from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import re
from seleniumwire import webdriver
from splinter import Browser
from download_functions import *  #função para realziar o download
from fix_file_type import * #função para achar o tipo do arquivo e converter para o formato correto
from ocr import * #função para converter pdfs nao editaveis em word

#Essas  livrarias instalar assim:
#pip install selenium-wire
#pip install blinker==1.7.0
#playwright install   




revoked_list = [] #lista de resoluções revogadas

#Settings selenium
def setup_driver():
    service = ChromeService(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--enable-features=NetworkService,NetworkServiceInProcess")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=service, options=options)



def wait_for_element(driver, by, value, timeout=5):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )
    

def process_link(file_url, link_text, file_info_list):

    # Formata o nome do arquivo
    if 'nº' not in link_text:
        file_name = f'nº {link_text.replace("/", "_")}.pdf'
    else:
        file_name = f'{link_text.replace("/", "_")}.pdf'

    # Verifica se o link já existe na coleção
    if not in_collection(file_url, file_name):
        #link.click()  # Realiza o clique apenas se o link for novo
        file_info_list.append((file_url, file_name))
    # else:
    #     print(f"Link existente: {file_name}")


#do the scrape in the page
def scrape_page(driver, browser, file_info_list):
    download_links = []
    # download_links = wait_for_element(driver, By.XPATH, '//a[contains(@href, "downloadArquivo")]')
    list_items = driver.find_elements(By.XPATH, '//li[a[contains(@href, "downloadArquivo")]]')
    #print(list_items)
    
    for item in list_items:
        item_text = item.text.strip()
        
        if "REVOGOU a Resolução" in item_text:
            #print(item_text)
            pattern1 = r"nº\s(\d{3}/\d{4})"
            pattern2= r"(\d{3}/\d{4})"
            match = re.search(pattern1, item_text)
            if not match:
                match = re.search(pattern2, item_text)

            if match:        
                resolution_find = match.group(1)  
                revoked_list.append(resolution_find)
                revoked_list.append('nº' + resolution_find)
                #print(f"Resolução revogada: {resolution_find}")

    download_links = driver.find_elements(By.XPATH, '//a[contains(@href, "downloadArquivo")]')
    revoked_list_clean = [item.strip().replace(" ", "").lower() for item in revoked_list]

    #if link_text_clean not in revoked_list_clean:
    
    for link in download_links:
        #as resoluções da partir de 046/2007 a 059/2008 estão no formato htm, entao tenho que abrir o browser para conseguir o link .htm
        #eu poderia usar o browser.visit para todos dai teria os arquivos em .htm e em .pdf, mas daí o processo fica mais demorado
        #usando só para essas resoluções, que são poucas, torna o processo mais rápido.
        list_resol = ['059/2008', '057/2008', '052/2008', '051/2008', '050/2008', 
                        '046/2008', '31/2008', '016/2008', '015/2008', '014/2008', '013/2008', '013/2008', 
                        '001/2008', '062/2007', '054/2007', '053/2007', '049/2007', '048/2007', '046/2007',
                        'nº 059/2008', 'nº 057/2008', 'nº 052/2008', 'nº 051/2008', 'nº 050/2008', 
                        'nº 046/2008', 'nº 31/2008', 'nº 016/2008', 'nº 015/2008', 'nº 014/2008', 'nº 013/2008', 'nº 013/2008', 
                        'nº 001/2008', 'nº 062/2007', 'nº 054/2007', 'nº 053/2007', 'nº 049/2007', 'nº 048/2007', 'nº 046/2007']
        link_text = link.text.strip()
        link_text_clean = link_text.strip().replace(" ", "").lower()
        if link_text_clean not in revoked_list_clean: # se estiver na lista de revogados, não baixar
            if (link_text in list_resol):    #para achar os links .htm    
                browser.visit(link.get_attribute('href'))
                file_url = browser.url
            else:
                file_url = link.get_attribute('href')

            process_link(file_url, link_text, file_info_list)
        # else:
        #     print(f"Resolução revogada: {link_text}")
    #print(f"Resolução revogada: {revoked_list_clean}")
    savelink(file_info_list)



#go to the page or next page
def scrape_pages(driver, browser):
    file_info_list = []
    pagination_dropdown = wait_for_element(driver, By.ID, 'j_id_jsp_338632075_13:paginas')
    select = Select(pagination_dropdown)

    for i in range(0, len(select.options)-4): 
        pagination_dropdown = wait_for_element(driver, By.ID, 'j_id_jsp_338632075_13:paginas')
        select = Select(pagination_dropdown)

        page = f'Pag. {i + 1}'
        select.select_by_visible_text(page)
        search_button = wait_for_element(driver, By.XPATH, f'//option[@value={str(i)}]')
        search_button.click()
        #print(f"Indo para a página {page}")
        scrape_page(driver, browser, file_info_list)

    return file_info_list
    

        
def main():
    start_time = time.time()
    
    #Download path



    with setup_driver() as driver, Browser('chrome', options=Options()) as browser:
        url = 'https://sigrh.ufpb.br/sigrh/public/colegiados/filtro_busca.jsf'
        driver.get(url)

        # Preenche o campo de busca
        search_field = wait_for_element(driver, By.NAME, 'formulario:j_id_jsp_338632075_9')
        search_field.send_keys('Resolução')

        # Seleciona o item do dropdown
        dropdown = wait_for_element(driver, By.NAME, 'formulario:j_id_jsp_338632075_4')
        select = Select(dropdown)
        select.select_by_visible_text('Conselho Superior de Ensino, Pesquisa e Extensão')

        # Clica no botão de busca
        search_button = wait_for_element(driver, By.XPATH, '//input[@value="Buscar"]')
        search_button.click()

        # Realiza o scraping e o download
        file_info_list = scrape_pages(driver, browser)
        download_files()

    
    elapsed_time = time.time() - start_time
    print(f"Operação concluída em {elapsed_time:.2f} segundos.")

if __name__ == "__main__":
    download_dir = os.path.join(os.getcwd(), 'data/downloaded_files')
    os.makedirs(download_dir, exist_ok=True)
    folder_path = "./data/downloaded_files"
    main()        
    fix_file_type(folder_path)
    #ocr(folder_path)
    


