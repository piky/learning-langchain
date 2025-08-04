# LangChain Applications

## Pre-requisites
API Keys for the following services are required:
 - OpenRouter (URL: https://openrouter.ai/api/v1)
 - Tavily
### Create a `.env` file in the root directory with the following content:
```plaintext
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_API_KEY=<your_openrouter_api_key>
TAVILY_API_KEY=<your_tavily_api_key>
TOKENIZERS_PARALLELISM=false
POSTGRES_PASSWORD=<your_postgres_password>
POSTGRES_USER=<your_postgres_user>
POSTGRES_DB=<your_postgres_db>
```

### Dependencies 
To avoid issues, please ensure you have the following packages installed:
- Python 3.12+
- NumPy 1.26.4
- Sentence Transformers 5.0.0
- FAISS CPU 1.10
- LangChain 0.3.27
- LangChain Community 0.3.27
- LangChain Core 0.3.72
- LangChain HuggingFace 0.3.1
- LangChain OpenAI 0.3.28
- LangChain Ollama 0.3.6
- LangChain Tavily 0.2.11

## การเรียกใช้งานผ่าน API ของผู้ให้บริการ LLMs ค่ายต่างๆ
 - Ollama
 - OpenRouter

## การ Chain ขั้นตอนการทำงาน

## การสร้าง Prompt Template เพื่อกำหนดรูปแบบของข้อความที่ส่งไปยัง LLM

## Web Search (Tavily Search) ให้กับ LLM เพื่อให้สามารถค้นหาข้อมูล up-to-date จากเว็บได้

 ## RAG
  - structured data (Text2SQL) ให้ LLM รับคำสั่งจากผู้ใช้และแปลงเป็นคำสั่ง SQL เพื่อดึงข้อมูลจากฐานข้อมูล
  - unstructured data (Embedding) ให้ LLM สามารถค้นหาข้อมูลจากเอกสารที่เก็บไว้ในฐานข้อมูล vector databases
  - unstructure data (รูปภาพ, กราฟ, เสียง, binary files เช่น PDF, Word, Excel) ให้ LLM
สามารถค้นหาข้อมูลจากเอกสารที่เก็บไว้ในฐานข้อมูล vector databases
  - Similarity Search (Embedding) ให้ LLM
สามารถค้นหาข้อมูลที่มีความคล้ายคลึงกันจากเอกสารที่เก็บไว้ในฐานข้อมูล vector databases