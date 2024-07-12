1. BedRock Keys(cohere Embedding) & Weaviate URl&Key  mandatory
2.  cp env_exmaple as .env, Update latest bedrock keys
3.  Get dataset file input_people_data_03.json ,upon approval get the file by slack request
4.  docker build -t   person_summary .
5. docker run -it  person_summary
6. upon  "Enter your query (or type 'exit' to quit):" Enter the search query
