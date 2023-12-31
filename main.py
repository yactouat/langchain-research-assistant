#!/usr/bin/env python
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from langserve import add_routes
import uvicorn

from chains import (
    generate_arxiv_search_report,
    generate_sql_nlp_response,
    generate_pdf_report, 
    generate_web_search_report
)

app = FastAPI(
  title="research assistant api",
  version="1.0",
  description="a web API that serves an AI research assistant that can generate reports by crawling various sources for relevant information and summarizing it",
)
add_routes(
    app,
    generate_web_search_report,
    path="/generate-web-search-report",
)
add_routes(
    app,
    generate_arxiv_search_report,
    path="/generate-arxiv-search-report",
)
add_routes(
    app,
    generate_pdf_report,
    path="/generate-pdf-report",
)
add_routes(
    app,
    generate_sql_nlp_response,
    path="/sql-qa",
)
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)