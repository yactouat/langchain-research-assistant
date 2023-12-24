from datetime import datetime
import json
from langchain.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

from functions import get_serp_links, scrape_webpage_text
from prompts import report_prompt, summarization_prompt, web_search_engine_queries_prompt

# TODO implement Arxiv chain

generate_web_search_engine_queries = web_search_engine_queries_prompt  | ChatOpenAI(model="gpt-4-1106-preview") | StrOutputParser() | json.loads

scrape_and_summarize_webpage = RunnablePassthrough.assign(
    summary=RunnablePassthrough.assign(
        # anonymous function that takes no arguments, and returns the output of `scrape_text`
        content=lambda input_obj: scrape_webpage_text(input_obj["url"])
    ) | summarization_prompt | ChatOpenAI(model="gpt-4-1106-preview") | StrOutputParser()
) | (lambda summarization_res: f"URL: {summarization_res['url']}\n\nSUMMARY: {summarization_res['summary']}")

# return a list of urls based on the input query,
# then construct a dictionary list with the query and each url,
# then we apply the webpage summarization chain to each dictionary using the chain `map` method
summarize_webpages = RunnablePassthrough.assign(
    urls=lambda input: get_serp_links(input["query"])
) | (lambda list_of_urls: [
    {
        "query": list_of_urls["query"],
        "url": link
    } for link in list_of_urls["urls"]
]) | scrape_and_summarize_webpage.map()

# what we get here is a list of lists,
# we basically deletegate to the LLM the generation of relevant web search engine queries,
# then we visit each SERP result (up to provided limit) and summarize the page we've found
search_the_web = generate_web_search_engine_queries | (lambda queries: [
    {
        "query": q,
    } for q in queries
]) | summarize_webpages.map()

generate_web_search_report = RunnablePassthrough.assign(
    date=lambda _: datetime.now().strftime('%B %d, %Y'),
    # joining the list of lists of search results into a string
    summary= search_the_web | (lambda search_results: "\n".join([f"---\n{' '.join([text for text in sr])}\n---" for sr in search_results]))
) | report_prompt | ChatOpenAI(model="gpt-4-1106-preview") | StrOutputParser()