from os import getenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_tavily import TavilySearch
from dotenv import load_dotenv

load_dotenv()

""" Using LangChain AgentExecutor to search via Tavily with GPT-4o-mini. """

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that can answer questions using web search."),
    ("human", "Who is the current Prime Minister of {country}?"),
    ("placeholder", "{agent_scratchpad}"),
])

llm = ChatOpenAI(
    openai_api_key = getenv("OPENROUTER_API_KEY"),
    openai_api_base = getenv("OPENROUTER_BASE_URL"),
    model = "openai/gpt-4o-mini",
)

search_tool = TavilySearch(
    max_results=5,
    search_depth="basic",
    include_domains=[]
    )

tools = [search_tool]

agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

response = agent_executor.invoke({"country": "UK"})

print(response["output"])
