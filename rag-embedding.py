from os import getenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# Load ocument
loader = TextLoader("data.txt",encoding="utf-8")
documents = loader.load()
# print(documents)

# Split document
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100,chunk_overlap=50)
chunks = text_splitter.split_documents(documents)

# Embed chunks
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")

# Store into vector DB
vectorstore = FAISS.from_documents(chunks, embeddings)

# Retrive from vector DB
retrievers = vectorstore.as_retriever()

# Create Prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system","ใช้ข้อมูลจากเอกสารในการตอบคำถามให้สั้นกระชับด้วยความสุภาพเป็นกันเอง"),
    ("human","คำถาม : {question} , ข้อมูลที่เกี่ยวข้อง : {context}")
])

# Instantiate model 
llm = ChatOpenAI(
    openai_api_key = getenv("OPENROUTER_API_KEY"),
    openai_api_base = getenv("OPENROUTER_BASE_URL"),
    model = "openai/gpt-4o-mini",
)

# Chain all stages
rag_chain = (
    {"context":retrievers,"question":RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

result = rag_chain.invoke("มีสินค้าและบริการอะไรบ้าง")

print(result)