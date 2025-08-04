from langchain_tavily import TavilySearch
from dotenv import load_dotenv

load_dotenv()

""" Using TavilySearch directly without LLM for a simple search. """

tool = TavilySearch(
    max_results=5,
    search_depth="basic",
    include_domains=[]
    )

response = tool.invoke({"query": "Who is the current Prime Minister of Thailand?"})

for result in response["results"]:
    print(result["content"])
