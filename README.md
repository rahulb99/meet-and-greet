# Meet and Greet
Meet and talk to your favorite celebrites in a simulation game.

## Objective
Application of end-to-end agentic RAG workflow with prompt engineering, vector stores and LLMOps. The idea is to make incremental changes from the parent repo, for hands-on learning.

## Tech Stack
* Backend - FastAPI, MongoDB, LangGraph, LangChain 
* Frontend - PhaserJS
* LLMOps - Opik

## Incremental Changes
### Step 1
* Change domain: (dead) philosophers -> (alive) celebrities

### Step 2
* Tried different models for conversation and summarization (`openai/gpt-oss-20b`: much faster than Llama 3.3 70b, but higher hallucination rate, `deepseek-r1-distill-llama-70b` : slow and outdated)
* Add new tool (DuckDuckGo search) for current information
* Python 3.11 -> 3.13

### Step 3
* Mongo Atlas search -> Postgres with pgvector extension

## Acknowledgements
This repo is adapted from the [PhiloAgents Course](https://decodingml.substack.com/p/build-your-gaming-simulation-ai-agent) for the purposes of practical learning.
