from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI
from langchain.tools.retriever import create_retriever_tool

TEMPLATE = """You are working with a pandas dataframe in Python. The name of the dataframe is `df`.
It is important to understand the attributes of the dataframe before working with it. This is the result of running `df.head().to_markdown()`

<df>
{dhead}
</df>

You are not meant to use only these rows to answer questions - they are meant as a way of telling you about the shape and schema of the dataframe.
You also do not have use only the information here to answer questions - you can run intermediate queries to do exporatory data analysis to give you more information as needed.

You have a tool called `person_name_search` through which you can lookup a person by name and find the records corresponding to people with similar name as the query.
You should only really use this if your search term contains a persons name. Otherwise, try to solve it with code.

For example:

<question>How old is Jane?</question>
<logic>Use `person_name_search` since you can use the query `Jane`</logic>

<question>Who has id 320</question>
<logic>Use `python_repl` since even though the question is about a person, you don't know their name so you can't include it.</logic>
"""  # noqa: E501

agent = create_csv_agent(
    ChatOpenAI(temperature=0),
    "titanic.csv",
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

agent.run("how many rows are there?")