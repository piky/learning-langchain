from os import getenv
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

"""This script demonstrates how to use LangChain with OpenRouter's free model
to answer a question based-on its trained data about the Prime Minister of a specified country."""


prompt = ChatPromptTemplate.from_template(
        "Who is the Prime Minister of {country}?"
)

llm = ChatOpenAI(
    openai_api_key = getenv("GITHUB_MODEL_TOKEN"),
    openai_api_base = getenv("GITHUB_MODEL_ENDPOINT"),
    model_name="openai/gpt-4o"
)

chain = prompt | llm | StrOutputParser()

response = chain.invoke({"country": "Thailand"})

print(response)