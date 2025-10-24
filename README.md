# **Chatbot with Retrieval-Augmented Generation (RAG) + Fine-Tuning (QLoRA to GGUF Q4_K_M)**

**For students of Rajamangala University of Technology Isan Khon Kaen Campus**\
This project implements a chatbot powered by Retrieval-Augmented Generation (RAG) combined with fine-tuned LLMs using QLoRA exported to GGUF (Q4_K_M) format for efficient inference.
Deployment is containerized via Docker for streamlined setup and scaling.

### Features
**Retrieval-Augmented Generation (RAG):** Enhances chatbot responses with external knowledge retrieval.\
**Fine-Tuning with QLoRA:** Efficient low-rank adaptation for large language models.\
**GGUF Support:** Optimized model format for use with Ollama and other GGUF-compatible runtimes.


**Prerequisites**\
Docker & Docker Compose installed on your system.\
**Access keys for:**
- Resend API
- Google OAuth
- LINE OAuth + LINE LIFF + LINE Messaging API
- Typhoon OCR API


## Installation
**Step 1. Configure Environment Variables**\
Config a .env file in the project root.
```
RESEND_API_KEY=""
GOOGLE_CLIENT_ID=""
GOOGLE_CLIENT_SECRET=""
LINE_CLIENT_ID=""
LINE_CLIENT_SECRET=""
LIFF_ID=""
TYPHOON_OCR_API_KEY=""
LINE_CHANNEL_ACCESS_TOKEN=""
LINE_CHANNEL_SECRET=""
RESPONSE_MODEL="guff_model_8b-q4_k_m.gguf"
```
Endpoint for Google ouath ```http://localhost:3000/api/auth/callback/google```\
Endpoint for Line Login ```http://localhost:3000/api/auth/callback/line```\
Endpoint for Line webhook ```https://localhost:8020/ecp-ai/chat/webhook```\
\
**Step 2. Download Embedding Model**\
Download the `bge-m3` embedding model from Hugging Face: [Download bge-m3.](https://huggingface.co/BAAI/bge-m3)

Place the model inside:
```
ai/
 |_ embed/
      |_ bge-m/      <- This is Embedding Model.
      |_ README.md
```
\
**Step 3. Download Fine-Tuned Model (GGUF)**\
Download the `Fine-Tuned Model GGUF` from Hugging Face: [Model GGUF.](https://huggingface.co/PakornNZ/llama3.1_8b-q4_k_m) \
After that, go to `Files and Versions` and select the download `guff_model_8b-q4_k_m.gguf`.
> You cannot use **git clone** for Hugging Face.


Place the model inside:
```
ai/
 |_ finetune/
      |_ llama3.1_8b-q4_k_m/
               |_ guff_model_8b-q4_k_m.gguf    <- This is Model.
      |_ Modelfile.txt
      |_ README.md
```

> NOTE \
> If the filename is different, update: `ai/finetune/Modelfile.txt`

> NOTE \
> You may also change the model name via .env: `RESPONSE_MODEL="your_model_name.gguf"`

\
**Step 4. Deploy with Docker**\
From the project root (/), run:
```
docker compose up -d
```
After containers are built, wait 3–5 minutes for internal setup.\
Once ready, you can access and interact with the chatbot.

> IMPORTANT \
> If your system has CUDA-enabled NVIDIA GPUs, you can enable GPU support for the Ollama service by modifying `docker-compose.yml`.
> Uncomment and adjust the following section under the Ollama service:
```
# deploy:
#   resources:
#     reservations:
#       devices:
#         - driver: nvidia
#           capabilities: [gpu]
#           count: all
```
This will allow Docker to allocate GPU resources for model inference, which can significantly improve performance.\

Config Role :\
```$ docker exec -it database-postgres psql -U postgres -d ecp-ai -h localhost -p 5432```\
```$ UPDATE web_users SET role_id = 2 WHERE web_user_id = {user id};```

Resend API: [Resend](https://resend.com/emails) \
Typhoon API: [Typhoon](https://playground.opentyphoon.ai/) \
Dataset: [Google Drive](https://drive.google.com/drive/folders/1HCiKwp1E4tvrADRqfJZ3mRCO1HuYxFvG?usp=sharing)
