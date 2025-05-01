from create_collection_functions import * 
import hashlib
import shutil
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from html_to_pdf import * #função para converter htm em pdf

download_dir = os.path.join(os.getcwd(), 'data/downloaded_files')
os.makedirs(download_dir, exist_ok=True)

def get_file_hash(file_path):
    """Calculate the MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
    


def wait_for_download_complete(file_path, timeout=60):
    # Aguarda até que o arquivo seja completamente baixado, verificando o arquivo temporário
    start_time = time.time()
    while True:
        # Verifica se o arquivo temporário .part desapareceu
        if not os.path.exists(file_path + '.part'):
            return True
        # Se o tempo de espera exceder o timeout, retorna False
        if time.time() - start_time > timeout:
            return False
        time.sleep(1)  # Espera 1 segundo antes de verificar novamente

     
    
def download_file(file_url, file_name, download_dir, downloaded_files):
    temp_file = os.path.join(download_dir, file_name + '.part')
    final_file = os.path.join(download_dir, file_name)
    url_hash = hashlib.md5(file_url.encode()).hexdigest()

    if url_hash in downloaded_files:
        print(f"Skipping duplicate file: {file_name}")
        return

    try:
        response = requests.get(file_url, stream=True)
        if response.status_code == 200:
            with open(temp_file, 'wb') as f:
                shutil.copyfileobj(response.raw, f)

            # Verifica se o arquivo foi completamente baixado antes de renomear
            if wait_for_download_complete(temp_file):
                os.rename(temp_file, final_file)
                print(f"Downloaded {file_name}")

                # Verifica se o conteúdo do arquivo é duplicado
                file_hash = get_file_hash(final_file)
                if file_hash in downloaded_files.values():
                    print(f"Duplicate content detected. Removing {file_name}")
                    os.remove(final_file)
                else:
                    downloaded_files[url_hash] = file_hash
            else:
                print(f"Failed to download {file_name} completely.")
                os.remove(temp_file)  # Remove o arquivo temporário em caso de falha

        else:
            print(f"Failed to download {file_name}, status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading {file_name}: {str(e)}")
    

def download_files():    
    downloaded_files = {}  
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        items = linkcollection.get()
        if items["ids"]:  # Verifica se há itens na coleção
            for item_id, metadata in zip(items["ids"], items["metadatas"]): #primeiro verifico se o link está salvo já
                file_url, file_name = item_id, metadata['file_name']
                
                if (file_url.endswith('.htm')):  
                    output_path = download_dir +'/'+file_name
                    asyncio.run(url_to_pdf(file_url, output_path))

                else:
                    futures.append(executor.submit(download_file, item_id, metadata['file_name'], download_dir, downloaded_files))

        else:
            print("A coleção está vazia.")
    
        for future in futures:
            future.result()
    print(f"Total unique files downloaded: {len(downloaded_files)}")
       