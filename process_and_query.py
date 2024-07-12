# process_and_query.py
from dotenv import load_dotenv

import os
import weaviate
from weaviate_setup import setup_weaviate, process_documents

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_BEDROCK_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_BEDROCK_SECRET_ACCESS_KEY')
AWS_SESSION_TOKEN = os.getenv('AWS_BEDROCK_SESSION_TOKEN')

def query_weaviate(cluster_url, auth_credentials):
    """
    Allow user to enter queries and perform them on the Weaviate collection.
    
    Parameters:
    - cluster_url (str): URL of the Weaviate cluster.
    - auth_credentials (str): Weaviate API key or credentials.
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

    collection = client.collections.get("PersonProfile")

    while True:
        user_query = input("Enter your query (or type 'exit' to quit): ")
        if user_query.lower() == 'exit':
            break
        
        response = collection.query.near_text(
            query=user_query,
            limit=10,
            return_metadata=weaviate.classes.query.MetadataQuery(distance=True)
        )
        
        for o in response.objects:
            print(o.properties)
            print(o.metadata.distance)


if __name__ == "__main__":
    # Replace with your cluster URL and auth credentials
    cluster_url = 'https://sadiq-v2-qoo9zcnn.weaviate.network'  # Replace with your Weaviate cluster URL
    auth_credentials = '8L8evblmIuJi3fhc9Iut5W6k8jEar10E2fda'  # Replace with your Weaviate auth credentials
   
    # Setup Weaviate
    setup_weaviate(cluster_url, auth_credentials)
    
    # Set the folder path containing the documents
    folder_path = '/output_files/'
    
    # Process documents and add to Weaviate
    process_documents(cluster_url, auth_credentials, folder_path)
    
    # Query Weaviate
    query_weaviate(cluster_url, auth_credentials)
