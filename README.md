# NetTransfer AI

NetTransfer AI is a simple AI-powered assistant designed to interact with a bank's transfer requests database and process fund transfers through natural language commands.

---

## Features

- Query and process transfer requests stored in an SQLite database.
- Perform fund transfers by calling a dedicated transfer API.
- Web-based user interface for entering requests and viewing AI responses.
- AI agent powered by LlamaIndex with Groq LLM and HuggingFace embeddings.
- RESTful Flask backend with two services:
  - **Main AI service** (`/ask` endpoint)
  - **Funds transfer service** (`/transfer_funds` endpoint)

---

## Architecture Overview

- **Frontend:**  
  A clean HTML/JS UI where users input transfer-related requests and receive AI-generated responses.

- **Backend:**  
  - **AI API:** Uses an LLM agent to handle natural language queries, query the SQLite `transfer_requests` table, and initiate transfers.  
  - **Transfer API:** Processes transfer commands and simulates fund transfers.

- **Database:**  
  SQLite database (`transfers.db`) with a `transfer_requests` table queried by the AI agent.

---

## Setup & Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/nettransfer-ai.git
   cd nettransfer-ai