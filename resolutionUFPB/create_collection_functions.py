import chromadb
from urllib.parse import urlparse, urlunparse

import os

storelink_dir = os.path.join(os.getcwd(), './chromadb_storage')
os.makedirs(storelink_dir, exist_ok=True)

client = chromadb.PersistentClient(path="./chromadb_storage")
linkcollection = client.get_or_create_collection(name="document_links")

def normalize_url(url):
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, None, None, None))

    
def in_collection(file_url, file_name):
    items = linkcollection.get()
    # print("")
    # print("VENDO Minha collection")
    # print("")
    if not items["ids"]:  # Se a coleção estiver vazia
        return False
    for item_id, metadata in zip(items["ids"], items["metadatas"]):
        if item_id == file_url or metadata.get('file_name') == file_name:
            return True

    return False


def savelink(file_info_list):
    for file_url, file_name in file_info_list:
        if in_collection(file_url, file_name) == False:
            linkcollection.add(
                ids=[file_url],  
                documents=[file_name],  
                metadatas=[{"file_name": file_name}],  
            )
            print(f"Adicionado: {file_url}, {file_name}")
        else:
            print(f"Duplicado (não adicionado): {file_url}, {file_name}")



def printCollection():
    items = linkcollection.get()
    if items["ids"]:  
        for item_id, metadata in zip(items["ids"], items["metadatas"]):
            print(f"ID: {item_id}, Nome: {metadata['file_name']}")
    else:
        print("A coleção está vazia.")
