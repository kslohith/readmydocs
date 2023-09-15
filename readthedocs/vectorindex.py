from llama_index import VectorStoreIndex, SimpleDirectoryReader, load_index_from_storage, StorageContext
import os
from flask import Flask, request
import spacy
import json
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import evadb

app = Flask(__name__)

def create_index_from_documentation(openai_key):
    os.environ["OPENAI_API_KEY"] = openai_key
    documents = SimpleDirectoryReader('data').load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist()

def get_response_from_AI(openai_key,query,cursor):
    os.environ["OPENAI_KEY"] = openai_key
    get_relevant_context(query,cursor)
    query_string = f"ChatGPT('{query}', data)"
    generate_summary_rel = cursor.table("sample_data1").select(query_string)
    response = generate_summary_rel.df()["chatgpt.response"][0]
    return str(response)

def get_relevant_context(query,cursor):
 
    nlp = spacy.load('en_core_web_md')

    with open("storage/docstore.json", "r", encoding="utf-8") as file:
        docstore = json.load(file)

    user_query = query

    query_embedding = nlp(user_query).vector

    results = []
    for record_id, record_data in docstore["docstore/data"].items():
        doc_text = record_data["__data__"]["text"]
        doc_embedding = nlp(doc_text).vector
        similarity = cosine_similarity([query_embedding], [doc_embedding])[0][0]
        results.append((doc_text, similarity))

    results.sort(key=lambda x: x[1], reverse=True)

    eva_context = ""
    count = 0
    for doc, similarity in results:
        count += 1
        eva_context += f"{doc} \n"
        if count > 3:
            break

    df = pd.DataFrame([{"data": doc}])
    df.to_csv('evadb_context.csv')
    cursor.query('CREATE TABLE IF NOT EXISTS sample_data1 (data TEXT(100))').execute()
    cursor.load('evadb_context.csv', "sample_data1", "csv").execute()


@app.route('/askQuestion')
def answer_query():
    openai_key = request.args.get('openai_key')
    query = request.args.get('query')
    connection = evadb.connect()
    cursor = connection.cursor()
    return get_response_from_AI(openai_key,query,cursor)

@app.route('/loadIndex')
def load_index():
    openai_key = request.args.get('openai_key')
    try:
        create_index_from_documentation(openai_key)
        return 'successfully loaded index'
    except:
        return 'error occured while loading index'

if __name__ == '__main__':
    app.run(debug=True)


