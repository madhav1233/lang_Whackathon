import os
import sqlite3
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor

os.environ['OPENAI_API_KEY'] = "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"

# Connect to the database and execute the SQL script
conn = sqlite3.connect('tickets.db')
conn.close()

# Create the agent executor
db = SQLDatabase.from_uri("sqlite:///./tickets.db")
llm_instance = OpenAI(temperature=0)  # Create an instance of the OpenAI language model
toolkit = SQLDatabaseToolkit(db=db, llm=llm_instance)  # Pass the llm instance to the toolkit

# Here's the missing line where you create the agent_executor
agent_executor = create_sql_agent(
    llm=llm_instance,
    toolkit=toolkit,
    verbose=True
)

# Create the button callback
def userInput(query):
    result = agent_executor.run(query)
    return result

query = input("ask me anything! ")
print(userInput(query))
