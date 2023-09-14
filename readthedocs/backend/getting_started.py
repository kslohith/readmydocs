from flask import Flask, request
import evadb
import os
import pandas as pd

app = Flask(__name__)


@app.route('/getAnswerContext')
def hello_world():
        connection = evadb.connect()
        cursor = connection.cursor()
        question = request.args.get('question')
        os.environ['OPENAI_KEY'] = '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'
        # os.environ['OPENAI_KEY'] = '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'
        eva_context = ""
        with open('evadb_context.txt', 'r') as file:
                for line in file:
                        eva_context += f"{line} \n"
        df = pd.DataFrame([{"data": eva_context}])
        df.to_csv('evadb_context.csv')
        cursor.query('CREATE TABLE IF NOT EXISTS sample_data1 (data TEXT(100))').execute()
        cursor.load('evadb_context.csv', "sample_data1", "csv").execute()
        generate_summary_rel = cursor.table("sample_data1").select(
        "ChatGPT('{question}', data)"
        )
        response = generate_summary_rel.df()["chatgpt.response"]
        return response[0]

if __name__ == '__main__':
    app.run(debug=True)
