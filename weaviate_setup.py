# weaviate_setup.py
from dotenv import load_dotenv

import os
import weaviate
import weaviate.classes.config as wc

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_BEDROCK_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_BEDROCK_SECRET_ACCESS_KEY')
AWS_SESSION_TOKEN = os.getenv('AWS_BEDROCK_SESSION_TOKEN')

BEDROCK_ENDPOINT = 'https://bedrock.amazonaws.com'

def setup_weaviate(cluster_url, auth_credentials):
    """
    Set up the Weaviate connection and create a collection.
    
    Parameters:
    - cluster_url (str): URL of the Weaviate cluster.
    - auth_credentials (str): Weaviate API key or credentials.
    """

    # Weaviate Connection
    client = weaviate.connect_to_wcs(
         cluster_url=cluster_url,
         auth_credentials=weaviate.auth.AuthApiKey(auth_credentials),
          headers={
              "X-AWS-Access-Key": AWS_ACCESS_KEY_ID,
              "X-AWS-Secret-Key": AWS_SECRET_ACCESS_KEY,
              "X-AWS-Session-Token": AWS_SESSION_TOKEN
          },
        #timeout_config=weaviate.util.Config.Timeout(init=60),  # Uncomment to increase init timeout to 60 seconds
        #startup_config=weaviate.util.Config.Startup(skip_init_checks=True)  # Uncomment to skip startup checks
    )

    print(f'Client Ready with connect: {client.is_ready()}')

    # Delete the collection if it already exists
    if client.collections.exists("PersonProfile"):
        client.collections.delete("PersonProfile")

    client.collections.create(
        name="PersonProfile",
        vectorizer_config=wc.Configure.Vectorizer.text2vec_aws(
            model="cohere.embed-english-v3",
            service="bedrock",
            region="us-east-1"
        ),
        properties=[
            wc.Property(name="content", data_type=wc.DataType.TEXT),
        ]
    )

def process_documents(cluster_url, auth_credentials, folder_path):
    """
    Process documents and add them to the Weaviate collection.
    
    Parameters:
    - cluster_url (str): URL of the Weaviate cluster.
    - auth_credentials (str): Weaviate API key or credentials.
    - folder_path (str): Path to the folder containing text files.
    """

    client = weaviate.connect_to_wcs(
         cluster_url=cluster_url,
         auth_credentials=weaviate.auth.AuthApiKey(auth_credentials),
         headers={
              "X-AWS-Access-Key": AWS_ACCESS_KEY_ID,
              "X-AWS-Secret-Key": AWS_SECRET_ACCESS_KEY,
              "X-AWS-Session-Token": AWS_SESSION_TOKEN
         }
    )

    data = get_document_texts(folder_path)

    collection = client.collections.get("PersonProfile")

    with collection.batch.dynamic() as batch:
        for src_obj in data:
            weaviate_obj = {"content": src_obj}
            batch.add_object(properties=weaviate_obj)

def get_document_texts(folder_path):
    """
    Read and return the text content of files in a given folder.
    
    Parameters:
    - folder_path (str): Path to the folder containing text files.
    
    Returns:
    - list: List of text content from each file.
    """
    data = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), 'r',encoding='utf-8') as file:
                document_text = file.read()
                data.append(document_text)
    return data
