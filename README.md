# open-mcp-agents

Exploring agent infrastructure with a focus on MCP-based orchestration with Fast MCP, Langchain and LangGraph.

---

## Overview

This project demonstrates a modular agent infrastructure using MCP (Model-Context Protocol). It leverages Fast MCP, Langchain, and LangGraph to connect a client agent to multiple backend MCP microservices (e.g., todo, weather, math servers).

## Architecture

![Architecture](image.png)

## Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv)
- Docker & Docker Compose
- A valid `GROQ_API_KEY`

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/adilsaid64/open-mcp-agents
cd open-mcp-agents
```

### 2. Set up environment variables
Copy the template and fill in your API key:
```bash
cp app/.template.env app/.env
# Edit app/.env and set GROQ_API_KEY
```

### 3. (Recommended) Run with Docker Compose
This will build and start the client and todo-server. You can extend the compose file to add more services.
```bash
docker-compose up --build
```


## Environment Variables
- `GROQ_API_KEY`: Your API key for Groq (required by the client)
