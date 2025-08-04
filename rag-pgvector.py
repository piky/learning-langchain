from os import getenv
import psycopg2
from langchain_openai.chat_models import ChatOpenAI
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()
""" This script connects to a PostgreSQL database, embeds documents using a SentenceTransformer model,
and allows querying the database for relevant documents based on user input.
It uses the LangChain library to interact with an OpenAI chat model for generating responses 
based on retrieved documents. Referenced source https://youtu.be/WWUB7uqhKJk?si=nfoF6of47hHN7OcV """

conn = psycopg2.connect(
    dbname = getenv("POSTGRES_DB"),
    user = getenv("POSTGRES_USER"),
    password = getenv("POSTGRES_PASSWORD"),
    host = "localhost",
    port = "5432"
)

cur = conn.cursor()

# from ollama import Chat
# llm = ollama.chat(
#     model = "scb10x/llama3.2-typhoon2-1b-instruct",
#     messages = [{"role": "user", "content": prompt}]
#     )

llm2 = ChatOpenAI(
    openai_api_key = getenv("OPENROUTER_API_KEY"),
    openai_api_base = getenv("OPENROUTER_BASE_URL"),
    model_name="moonshotai/kimi-k2:free",
)

# print(llm2.invoke(prompt).content)

# cur.execute("""
#             CREATE TABLE IF NOT EXISTS documents (
#                 id SERIAL PRIMARY KEY,
#                 content TEXT,
#                 embedding vector(1024)
#                 );
#             """)
# conn.commit()

documents = [
    "เปิดหลักสูตรระดับปริญญาตรี 5 สาขาวิชา ได้แก่ สาขาวิชาวิทยาการคอมพิวเตอร์ สาขาวิชานวัตกรรมดิจิทัล สาขาวิชาสารสนเทศการลงทุน สาขาวิชาคอมพิวเตอร์เกมและอีสปอร์ต และสาขาวิชาเทคโนโลยีสื่อสังคม",
    "เปิดหลักสูตรระดับปริญญาโท 3 สาขาวิชา ได้แก่ สาขาวิชาการจัดการความมั่นคงไซเบอร์และเทคโนโลยี สาขาวิชาเทคโนโลยีสื่อสังคม สาขาการจัดการนวัตกรรมดิจิทัล",
    "หลักสูตรระดับปริญญาโท สาขาการจัดการนวัตกรรมดิจิทัล เรียนแบบออนไลน์",
    "หลักสูตรระดับปริญญาโท สาขาวิชาการจัดการความมั่นคงไซเบอร์และเทคโนโลยี และสาขาวิชาเทคโนโลยีสื่อสังคม เรียนเสาร์อาทิตย์",
    "เปิดหลักสูตรระดับปริญญาเอก 2 สาขาวิชา ดังนี้ สาขาวิชาเทคโนโลยีสารสนเทศ และสาขาวิชาเทคโนโลยีสื่อสังคม",
    "คณบดีคือ รศ.ดร. เชฏฐเนติ ศรีสอ้าน",
    "วิทยาลัยเทคโนโลยีสารสนเทศและการสื่อสารแห่งมหาวิทยาลัยรังสิต ก่อตั้งเมื่อปี พ.ศ. 2537 ได้เปิดดำเนินการสอนทั้งในระดับปริญญาตรี ปริญญาโท และปริญญาเอกทางด้านสาขาวิชาที่เกี่ยวข้องทาง ด้านเทคโนโลยีสารสนเทศสำหรับกลุ่มนักศึกษา และคนทำงานที่มีพื้นฐานความรู้ที่หลากหลายและประสบการณ์ที่แตกต่างกัน เพื่อที่จะสามารถตอบสนองต่อความต้องการของสังคม",
    "ปรัชญาคือเหนือกว่าด้วยเทคโนโลยี ก้าวสู่ระดับสากล ปณิธานคือมุ่งมั่นสร้างบัณฑิตไอทีมืออาชีพสู่สังคม และวิสัยทัศน์คือเป็นผู้นำด้านให้บริการการศึกษาทางด้านเทคโนโลยีสารสนเทศ โดยเน้นการวิจัยและสร้างพันธมิตรทางวิชาการเพื่อการพัฒนาอย่างยั่งยืน"
]

## Embedding and adding documents to the database.
# for doc in documents:
#     add_document(doc)

## Verify that the documents were added.
# cur.execute("SELECT * FROM documents;")
# rows = cur.fetchall()
# for row in rows:
#     print(row)

embedder = SentenceTransformer("BAAI/bge-m3")

def add_document(text):
    embedding = embedder.encode(text).tolist()
    cur.execute("INSERT INTO documents (content, embedding) VALUES (%s, %s)", (text, embedding))
    conn.commit()

def query_postgresql(query_text, k=3):
    query_embedding = embedder.encode(query_text).tolist()
    # print(query_embedding)

    query_embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"

    sql_query = """
                SELECT content, embedding <=> %s::vector AS similarity_score
                FROM documents
                ORDER BY similarity_score ASC
                LIMIT %s;
            """
    cur.execute(sql_query, (query_embedding_str, k))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

def generate_respose(query_text):
    retrived_docs = query_postgresql(query_text)
    context = "\n".join([doc[0] for doc in retrived_docs])
    # print(context)

    prompt = f"""Answer the question based on the following context:\n{context}\n\n Question: {query_text}\n\n"""
    # print(prompt)

    return llm2.invoke(prompt).content

print(generate_respose("ปริญญาเอกเปิดสอนสาขาอะไรบ้าง?"))
