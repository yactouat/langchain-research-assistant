from langchain.prompts import ChatPromptTemplate

summarization_prompt_template = """Answer the following query using the provided content.

If the answer is not in the content, just say "I can't answer the input query given the provided content".

-----------------------------------------------------------------------------------------------------------
Query: {query}
-----------------------------------------------------------------------------------------------------------
Content: 

{content}
-----------------------------------------------------------------------------------------------------------
"""
summarization_prompt = ChatPromptTemplate.from_template(summarization_prompt_template)

system_research_assistant_prompt = """"you are an AI research assistant, your job is to write objective reports with a given input summary"""
report_prompt_template = """
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
report_prompt = ChatPromptTemplate.from_messages([
    ("system", system_research_assistant_prompt),
    ("user", report_prompt_template)
])

web_search_engine_queries_prompt_messages = [
    ("user", """write 3 web search engine queries to search online for an objective answer to the following query: {query}\n
     -----------------------------------------------------------------------------------------------------------
     you must respond with a list of strings in the following format: '["query 1", "query 2", "query 3"]'
     """)
]
web_search_engine_queries_prompt = ChatPromptTemplate.from_messages(web_search_engine_queries_prompt_messages)

