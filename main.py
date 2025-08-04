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
    openai_api_key = getenv("OPENROUTER_API_KEY"),
    openai_api_base = getenv("OPENROUTER_BASE_URL"),
    model_name="moonshotai/kimi-k2:free",
    # model="z-ai/glm-4.5-air:free",
)

chain = prompt | llm | StrOutputParser()

response = chain.invoke({"country": "Thailand"})

print(response)