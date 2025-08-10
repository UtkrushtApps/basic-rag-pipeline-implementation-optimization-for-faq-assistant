# FAQ RAG Assistant: Retrieval Optimization and Prompt Engineering Task

## Task Overview
A user-facing FAQ assistant enables users to ask questions and get accurate, well-cited answers, leveraging an automated ChromaDB vector store populated with OpenAI-embedded FAQ documents. Your job is to finish the RAG pipeline—build the query encoder, retriever, context builder, and controlled prompt. Focus on ensuring relevant retrieval, citation annotation, prompt engineering for better LLM grounding, token budgeting for context windows, and simple category-based search filters. All infrastructure and database setup is done for you!

---

## Current Gaps to Address
- Retrieval logic: Only placeholder code exists—no semantic search or filtering implemented.
- Context control: Chunks are sometimes too long or irrelevant, causing context dilution.
- Prompt construction: System/user/assistant prompt not customized, and answers lack citation markers.
- Token budgeting: Context windows may exceed LLM input length, risking answer truncation or error.
- Latency and token metrics: Not monitored/logged for QA or optimization.

## What to Focus On
- Write the complete RAG pipeline in `rag_retrieval.py`:
  - Embed user input and perform vector similarity search over pre-embedded FAQ chunks
  - Limit context size using tiktoken/tokenizer so that the LLM prompt stays under 3500 tokens
  - Add citation markers (e.g., [doc_id:chunk_idx]) next to evidence in the answer/response
  - Allow optional filtering by FAQ category using chunk metadata
  - Build a simple few-shot prompt incorporating at least 2 Q&A examples from `sample_queries.txt` and returned evidence chunks
  - Log latency from retrieval to response and the total tokens used in the prompt
- Return a structured JSON object:
  - 'answer': the generated response
  - 'citations': list of (doc_id, chunk_index, snippet) supporting evidence
  - 'latency_ms': latency for retrieval+response (ms)
  - 'prompt_tokens': total number of tokens sent to the LLM API

## Database Access & Details
- Chroma DB runs locally with collection "faq_kb"
- All FAQ docs split into 256-token chunks (32-token overlap), each labeled with doc_id, chunk_index, category, orig_pos
- Connection code is pre-built in `database_client.py` and configured via `config/database.json`
- Review `sample_queries.txt` for realistic test inputs

## Objectives
- Retrieve and ground answers in correct chunks and categories
- Respect a strict token budget and use citation markers for traceability
- Optimize search for relevance while logging latency and prompt usage
- Pass provided functional tests using `sample_queries.txt` (relevant chunk returned, citations present, prompt and latency logged)

## How to Verify
- Run a few queries from `sample_queries.txt`. Check:
  - Are the most relevant FAQ chunks retrieved and cited?
  - Is the answer concise, relevant, and does not hallucinate non-existent facts?
  - Are citations included and correctly linked to document metadata?
  - Are retrieval latency and prompt token usage returned with each response?
- Use the built-in assertions/examples to test robustness and accuracy.

---

Feel free to use and adapt LangChain, tiktoken, and OpenAI API (or mock/stub) for generation. Do not change database or infrastructure code. See below for definitions and use only the internals of `rag_retrieval.py` to complete the challenge!