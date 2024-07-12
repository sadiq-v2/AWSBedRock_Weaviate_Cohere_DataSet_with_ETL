# app.py
import os
import pandas as pd
from generate_summary_content import generate_summary_content
from sanitize_filename import sanitize_filename
from process_and_query import setup_weaviate, process_documents, query_weaviate

def main():
    # Set up Weaviate
    cluster_url = 'https://sadiq-v2-qoo9zcnn.weaviate.network'  # Replace with your Weaviate cluster URL
    auth_credentials = '8L8evblmIuJi3fhc9Iut5W6k8jEar10E2fda'  # Replace with your Weaviate auth credentials
    setup_weaviate(cluster_url, auth_credentials)

    # Load JSON data into a pandas DataFrame
    df = pd.read_json('all_json_objects.json', lines=True)

    # Create a directory to store output files (if it doesn't exist)
    output_directory = './output_files'
    os.makedirs(output_directory, exist_ok=True)

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        record = row.to_dict()
        summary_content = generate_summary_content(record)

        # Generate the file name based on the person's name and ID
        person_id = record["person_id"]
        name = record["name"].replace(" ", "_")
        sanitized_name = sanitize_filename(name)
        output_txt_file = os.path.join(output_directory, f'output_summary_{person_id}_{sanitized_name}.txt')

        # Save to individual TXT files
        with open(output_txt_file, 'w', encoding='utf-8') as file:
            employment_summary = summary_content.get('employment_summary')
            education_summary = summary_content.get('education_summary')
            aggregate_summary = summary_content.get('aggregate_summary')

            # Format each section as a full paragraph, skipping if None
            combined_summary = ""
            if employment_summary:
                combined_summary += "Employment Summary:\n" + employment_summary + "\n"
            if education_summary:
                combined_summary += "Education Summary:\n" + education_summary + "\n"
            if aggregate_summary:
                combined_summary += "Aggregate Summary:\n" + aggregate_summary + "\n"
            combined_summary += "-"*200 + "\n\n"

            file.write(combined_summary)

        print(f"Generated text summary saved to {output_txt_file}")

    # # Process documents and add to Weaviate
    process_documents(cluster_url, auth_credentials, output_directory)

    # # Query Weaviate
    query_weaviate(cluster_url, auth_credentials)

if __name__ == "__main__":
    main()
