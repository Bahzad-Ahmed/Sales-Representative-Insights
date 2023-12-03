# Sales-Representative-Insights

## How to run the code:

In order to run the code you must have a python environment >=3.9 and make sure pandas, langchain, openai, langchain-experimental and flask are installed use:
```pip install pandas langchain openai langchain-experimental flask```
and run the file main.py using ```python main.py```

## Code architecture and technologies used:

This Flask application serves as an API locally to analyze and retrieve insights from a sales performance dataset. The application utilizes Langchain, a natural language processing tool, to interact with a Pandas data frame using an agent powered by OpenAI to clean and then analyze the data in _sales_performance_data.csv_ and generate insights.
