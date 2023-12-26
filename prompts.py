from langchain.prompts import ChatPromptTemplate

arxiv_search_queries_prompt_messages = [
    ("user", """write 4 arxiv search queries to search Arxiv with the following subject: {query}\n
     one of your output queries should be the original query, surrounded by double quotes
     -----------------------------------------------------------------------------------------------------------
     here are some some things you should know to help you write good Arxiv queries, don't include the backticks in your queries, they're here for highlighting examples =>

     - do not prefix a query with things like `title:`, `abstract:`, `author:`, etc. as this will limit the search to the specified field

     ## searching by author:

     - for the most precise name search, follow surname(s), forename(s) or surname(s), initial(s) pattern: example `Hawking, S or Hawking, Stephen`
     - for best results on multiple author names, separate individuals with a `;` (semicolon). Example: `Jin, D S; Ye, J`
     - author names enclosed in quotes will return only exact matches; for example, `"Stephen Hawking"` will not return matches for `Stephen W. Hawking`
     - diacritic character variants are automatically searched in the Author(s) field
     - queries with no punctuation will treat each term independently

     ## wildcards:

     - use `?` to replace a single character or `*` to replace any number of characters; this can be used in any field, but not in the first character position
     
     ## expressions:
     
     - TeX expressions can be searched, enclosed in single `$` characters
    
     ## phrases:
     
     - enclose phrases in double quotes for exact matches in title, abstract, and comments
     
     ## dates:
     
     - sorting by announcement date will use the year and month the original version (v1) of the paper was announced
     - sorting by submission date will use the year, month and day the latest version of the paper was submitted
     
     ## journal References:
     
     - if a journal reference search contains a wildcard, matches will be made using wildcard matching as expected; for example, `math*` will match `math`, `maths`, `mathematics`, etc.
     - if a journal reference search does not contain a wildcard, only exact phrases entered will be matched; for example, `math` would match `math` or `math` and science but not `maths` or `mathematics`
     - all journal reference searches that do not contain a wildcard are literal searches: a search for `Physica A` will match all papers with journal references containing `Physica A`, but a search for `Physica A, 245 (1997) 181` will only return the paper with journal reference `Physica A, 245 (1997) 181`
     -----------------------------------------------------------------------------------------------------------
     you must respond with a list of strings in the following format: '["query 1", "query 2", "query 3"]'
     """)
]
arxiv_search_queries_prompt = ChatPromptTemplate.from_messages(arxiv_search_queries_prompt_messages)

directed_summarization_prompt_template = """Answer the following query using the provided content.

If the answer is not in the content, just say "I can't answer the input query given the provided content".

-----------------------------------------------------------------------------------------------------------
Query: {query}
-----------------------------------------------------------------------------------------------------------
Content: 

{content}
-----------------------------------------------------------------------------------------------------------
"""
directed_summarization_prompt = ChatPromptTemplate.from_template(directed_summarization_prompt_template)

document_summarization_prompt_template = """Provide a summary based the follwing content.

Your summary will ONLY be based on the provided content and WILL NOT contain any additional data from your knowledge base.

-----------------------------------------------------------------------------------------------------------
Content: 

{content}
-----------------------------------------------------------------------------------------------------------
"""
document_summarization_prompt = ChatPromptTemplate.from_template(document_summarization_prompt_template)

free_summarization_prompt_template = """Provide a summary based the follwing content and query.

Your summary will ONLY be focused on the relationship between the provided content and the provided query.

Whether this relationship exists or not, you MUST explain this presence or absence of relationship in your summary.

-----------------------------------------------------------------------------------------------------------
Query: {query}
-----------------------------------------------------------------------------------------------------------
Content: 

{content}
-----------------------------------------------------------------------------------------------------------
"""
free_summarization_prompt = ChatPromptTemplate.from_template(free_summarization_prompt_template)

system_research_assistant_prompt = """"you are an AI research assistant, your job is to write objective reports with a given input summary"""

report_with_a_source_query_prompt_template = """
source: {source}
-----------------------------------------------------------------------------------------------------------
input summary: {summary}
-----------------------------------------------------------------------------------------------------------
using the above input summary only and without tapping into your own knowledge, generate a comprehsive report about the input summary;
at the top of the report should be a top-level heading saying reading "Summary of {source}";
right below the top level heading, the date should be written in the following format: {date};
write your answer as a structured report in Markdown with relevant headings and subheadings;
the report should contain a table of contents at the beginning, each item in the table of contents should be a link to the relevant header in the report using only Markdown syntax for links and not HTML;
at the end of the report, a level 2 heading of reading "Sources" should precede a bullet points list of all relevant URLs used in the report if such URLs are provided in the input summary;
"""
report_with_a_source_query_prompt = ChatPromptTemplate.from_messages([
    ("system", system_research_assistant_prompt),
    ("user", report_with_a_source_query_prompt_template)
])

report_with_query_prompt_template = """
-----------------------------------------------------------------------------------------------------------
input summary: {summary}
-----------------------------------------------------------------------------------------------------------
using the above input summary only and without tapping into your own knowledge, answer to the following query in a comprehensive manner;
at the top of the report should be a top-level heading reading "Answer to the query: {query}";
right below the top level heading, the date should be written in the following format: {date};
write your answer as a structured report in Markdown with relevant headings and subheadings;
the report should contain a table of contents at the beginning, each item in the table of contents should be a link to the relevant header in the report using only Markdown syntax for links and not HTML;
at the end of the report, a level 2 heading of reading "Sources" should precede a bullet points list of all relevant URLs used in the report if such URLs are provided in the input summary;
-----------------------------------------------------------------------------------------------------------
query: {query}
-----------------------------------------------------------------------------------------------------------
"""
report_with_query_prompt = ChatPromptTemplate.from_messages([
    ("system", system_research_assistant_prompt),
    ("user", report_with_query_prompt_template)
])

web_search_engine_queries_prompt_messages = [
    ("user", """write 3 web search engine queries to search online for an objective answer to the following query: {query}\n
     -----------------------------------------------------------------------------------------------------------
     you must respond with a list of strings in the following format: '["query 1", "query 2", "query 3"]'
     """)
]
web_search_engine_queries_prompt = ChatPromptTemplate.from_messages(web_search_engine_queries_prompt_messages)

