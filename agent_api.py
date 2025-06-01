import sqlite3
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
#from llama_index.llms.openai import OpenAI
from llama_index.llms.groq import Groq
from llama_index.core.agent import ReActAgent
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core.tools import QueryEngineTool
from llama_index.core.tools import FunctionTool
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import SQLDatabase
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    select,
)

# === Flask API ===
app = Flask(__name__)
CORS(app)

# === Define Global Settings Configuration===
Settings.llm = Groq(model="llama3-70b-8192", api_key=os.getenv("GROQ_API_KEY"))
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# === MCP Tool ===
def transfer_funds(recipient: str, amount: float, currency: str) -> str:
    response = requests.post(
        "http://localhost:5000/transfer_funds",  # use container name in Docker network
        json={"recipient": recipient, "amount": amount, "currency": currency}
    )
    if response.status_code == 200:
        return f"Transferred {amount} {currency} to {recipient}"
    else:
        return f"Failed to transfer {amount} {currency} to {recipient}"


# === SQLite Connection ===
#conn = sqlite3.connect("transfers.db")
engine = create_engine("sqlite:///transfers.db")

# Wrap it into SQLDatabase
sql_database = SQLDatabase(engine)

# === NLSQL Query Engine ===
query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database,
    tables=["transfer_requests"],
)


# === Create Tools ===
db_tool = QueryEngineTool.from_defaults(
    query_engine=query_engine,
    name="TransferRequestsDatabase",
    description="A tool to answer questions about the transfer_requests table."
)

transfer_tool = FunctionTool.from_defaults(fn=transfer_funds)


# === Initialize Agent ===
#llm = OpenAI(model="gpt-4o")  # Or gpt-4-turbo
#llm = Groq(model="meta-llama/llama-4-scout-17b-16e-instruct", api_key="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")

agent = ReActAgent.from_tools(
    tools=[db_tool, transfer_tool],
    verbose=True
)


# === API Endpoint ===
@app.route('/ask', methods=['POST'])
def ask_agent():
    data = request.json
    user_message = data.get('message')

    instruction = (
    "You are a bank operations assistant. "
    "Your task is to process transfer requests from the database using the QueryEngineTool. "
    "Do not guess. Use the tool to get the information."
    )

    response = agent.chat(instruction + user_message)

    return jsonify({
        "response": str(response)
    })


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
