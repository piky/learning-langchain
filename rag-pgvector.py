from os import getenv
import psycopg2
from langchain_openai.chat_models import ChatOpenAI
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname="mydb",
    user="postgres",
    password=getenv("POSTGRES_PASSWORD"),
    host="localhost",
    port="5432"
)

cur = conn.cursor()
# cur.execute("""
#     CREATE TABLE IF NOT EXISTS documents (
#         id SERIAL PRIMARY KEY,
#         content TEXT,
#         embedding vector(1536)
#     )
# """)
# conn.commit()
# cur.close()
# conn.close()

# prompt = """Who is the Prime Minister of Thailand?"""

# llm = ollama.chat(
#     model = "scb10x/llama3.2-typhoon2-1b-instruct",
#     messages = [{"role": "user", "content": prompt}]
#     )

# llm2 = ChatOpenAI(
#     openai_api_key = getenv("OPENROUTER_API_KEY"),
#     openai_api_base = getenv("OPENROUTER_BASE_URL"),
#     model_name="moonshotai/kimi-k2:free",
# )

# print(llm2.invoke(prompt).content)
# cur = conn.cursor()
# cur.execute("""
#             CREATE TABLE IF NOT EXISTS documents (
#                 id SERIAL PRIMARY KEY,
#                 content TEXT,
#                 embedding vector(1536)
#             )
# """)

# conn.commit()
 
embedder = SentenceTransformer("BAAI/bge-m3")

def add_document(text):
    embedding = embedder.encode(text).tolist()
    cur.execute("INSERT INTO documents (content, embedding) VALUES (%s, %s)", (text, embedding))
    conn.commit()
