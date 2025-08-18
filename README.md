# copilot-rag-platform

A RAG service intended for enhancing your LLMs to give you curated, accurate responses based on your organization's data.

Currently supports local storage, to run add .txt files to your /data folder that contain context
to the problem you require solved. 

# Running the Service

Currently this setup only uses docker-compose, other options are currently a work in progress.

OpenAI API key is required, as text-embedding-3-large and gpt-4o-mini are the models used for RAG, and LLM querying respectively. To generate an API key visit: https://platform.openai.com/settings/organization/api-keys 

After getting your API key, add it to your environment variables and cd into infra directory.

Run: docker compose up --build

# Using the Service

After your docker-compose is running, query endpoint:

curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{"q":"INSERT YOUR PROMPT HERE"}'