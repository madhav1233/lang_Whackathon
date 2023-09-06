from flask import Flask, request, jsonify
import os
import sqlite3
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor

app = Flask(__name__)

# Use environment variable for the API key
api_key = os.environ.get('OPENAI_API_KEY')

# Connect to the database and execute the SQL script
conn = sqlite3.connect('tickets.db')
conn.close()

# Create the agent executor
db = SQLDatabase.from_uri("sqlite:///./tickets.db")
llm_instance = OpenAI(temperature=0, api_key=api_key)  # Pass the API key here
toolkit = SQLDatabaseToolkit(db=db, llm=llm_instance)

agent_executor = create_sql_agent(
    llm=llm_instance,
    toolkit=toolkit,
    verbose=True
)

@app.route('/query', methods=['POST'])
def get_response():
    data = request.json
    query = data.get('query')
    result = agent_executor.run(query)
    return jsonify(result)

if __name__ == '__main__':
    app.run()
