import arxiv
from bs4 import BeautifulSoup
from langchain.utilities import DuckDuckGoSearchAPIWrapper
import requests

# getting a list of arxiv papers summaries and their metadata formatted as strings
def get_arxiv_search_results(query: str, num_results: int = 5):
    client = arxiv.Client()
    search = arxiv.Search(
        max_results=num_results,
        query=query,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    results_formatted = []
    for paper in client.results(search):
        authors_str = ", ".join([author.name for author in paper.authors])
        links_str = ", ".join([link.href for link in paper.links])
        published_str = paper.published.strftime('%B %d, %Y')
        results_formatted.append({
            "authors": authors_str,
            "id": paper.get_short_id(),
            "links": links_str,
            "published": published_str,
            "summary": paper.summary,
            "title": paper.title,
        })
    return [f"""Title: {result["title"]}
            
        ID: {result["id"]}
        
        Authors: {result["authors"]}

        Published: {result["published"]}

        Summary: {result["summary"]}

        Links: {result["links"]}
        
    """ for result in results_formatted]

def get_serp_links(query: str, num_results: int = 5):
    ddg_search = DuckDuckGoSearchAPIWrapper()
    results = ddg_search.results(query, num_results)
    return [r["link"] for r in results]

def scrape_webpage_text(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            # BeautifulSoup transforms a complex HTML document into a tree of Python objects,
            # such as tags, navigable strings, or comments
            soup = BeautifulSoup(r.text, 'html.parser')
            # separating all extracted text with a space
            text = soup.get_text(separator=" ", strip=True)
            return text
        else:
            return f"failed to scrape webpage with status: {r.status_code}"
    except Exception as e:
        return f"failed to scrape webpage with error:\n{e}"
