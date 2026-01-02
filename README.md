# ai_docker_run
Keep all docker-ai related learning here.

## Sample app
Using docker compose to bring up a container to run on an AI model installed locally

## Requirements
1. A model was previously installed:  
  docker model list  
  docker model pull smollm3  
2. A python environment with following files:  
  - docker-compose.yml
  - main.py
  - ackend.env
  - Dockerfile

## Operation  
docker compose build  
docker compose up  

Open browser pointing to the local url shown from compose up

Ref: https://www.youtube.com/watch?v=GOgfQxDPaDw


## Manually installing model that is not downloadable from Docker Hub
Microsoft's Phi-4 family model is recommended - Phi-4-Mini (3.8B) - The Smartest "Small" Model  

### Step 1: Download the Model File  
1. Go to the Hugging Face page for Phi-4-mini-instruct-GGUF.
2. Navigate to the Files and versions tab.
3. Download the file named: Phi-4-mini-instruct-Q5_K_M.gguf (Phi-4-mini-instruct-Q4_K_M.gguf is smaller if Q5 doesn't work).
4. Create "models" directory and put the downloaded gguf file there.

### Step 2: Configure your Project
You don't need to "build" the model like software; you just need to point your LLM engine to this file.  
1. In your project folder, create a new subfolder named /models.
2. Move the downloaded .gguf file into that /models folder.
3. Update your docker-compose.yml to mount this file into the container.

Update __docker-compose.yml__
```
services:
  llm:
    image: ghcr.io/ggerganov/llama.cpp:server  # Using the official llama.cpp engine
    volumes:
      - ./models:/models
    ports:
      - "12434:8080"
    command: ["-m", "/models/Phi-4-mini-instruct-Q5_K_M.gguf", "--host", "0.0.0.0", "--port", "8080"]
```

Update __backend.env__
```
BASE_URL=http://host.docker.internal:12434/v1/
MODEL=Phi-4-mini
API_KEY=anything
```

## Note
This Docker compose brings up 2 instances:
1. "app" using streamlit to send queries and receive LLM responses (http://localhost:8501). This can be used to interact with models programmatically.
2. Accessed LLM directly via http://localhost:12434 for conversations retaining.

To run a model directly, only docker model is needed:
docker model pull ai/gemma3
docker model list
docker model run ai/gemma3
