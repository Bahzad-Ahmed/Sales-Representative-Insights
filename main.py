import pandas as pd
from flask import Flask, request, jsonify
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.llms import OpenAI


# Initialize Flask app
app = Flask(__name__)

# Load sales data
df = pd.read_csv("sales_performance_data.csv")

# Initialize Langchain agent
openai_api_key = "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"
openai = OpenAI(temperature=0.0, openai_api_key=openai_api_key)
agent = create_pandas_dataframe_agent(openai, df, verbose=True, max_tokens=50)


def clean_data():
    
    data_cleaning_prompt_list = [
        "convert the created into datetime data type",
        "Create new columns for day, month and year using the created date",
        "Remove all rows with empty data.",
    ]

    for prompt in data_cleaning_prompt_list:
        agent.run(prompt)


def get_insights_for_representative(rep_id):
    results = []
    
    if rep_id not in df['employee_id'].values:
        return "Employee with id {id} was not found in the csv".format(id=rep_id)
    
    prompt_list = [

        "Total number of tours booked by employee {id} compared to overall team, output value by employee and overall team, percentage thereof.",
        "Total number of leads taken by employee {id} compared to overall team, output value by employee and overall team and percentage thereof.",
        "Average number of tours booked per lead by employee {id} compared to overall team, output value by employee and overall team.",
        "Average number of applications submitted per booked tour by employee {id} compared to overall team, output value by employee and overall team.",
        "Average number of applications submitted per lead by employee {id} compared to overall team, output value by employee and overall team.",
        "Total revenue confirmed by employee {id} compared to overall team, output value by employee and overall team and percentage thereof.",
        "Total revenue pending by employee {id} compared to overall team, output value by employee and overall team and percentage thereof.",
        "Number of tours(scheduled but not yet completed) by employee {id} compared to overall team, output value by employee and overall team and percentage thereof.",
        "Average value of deals closed by employee {id} compared to overall team, output value by employee and overall team.",
        "Percentage of tours booked that result in confirmed revenue by employee {id} compared to overall team, output value by employee and overall team and percentage thereof.",

    ]
    
    results = ' '.join([agent.run(prompt.format(id=rep_id)) for prompt in prompt_list])

    return results


def get_insights_for_team():
    results = []
    
    prompt_list = [
        "What is the total number of leads taken? What is the average number of leads taken daily (by grouping on dated)?",
        "Give me the total number of tours booked and the average number of tours booked daily (by grouping on date)",
        "What is the total number of applications (apps) per tour? What is the total number of applications (apps) per lead? Are more applications (apps) generated through tours or through leads?",
        "What is the average revenue confirmed, revenue pending and revenue runrate daily (by grouping on date)?",
        "Which employee has the highest revenue runrate and what is it?",
        "How many tours are in the pipeline daily (grouped by date)?",
        "Which employee has the highest average deal value for 30 days and what is it?",
        "What is the ratio of tours cancelled to tours scheduled?",
        "How frequently are sales texts done over sales calls?"
    ]
    
    results = ' '.join([agent.run(prompt) for prompt in prompt_list])
    
    return results


def get_insights_periodically(time_period):
    results = []
    
    if time_period not in ["weekly", "monthly", "bimonthly", "quarterly", "biannual", "yearly"]:
        return "Please use time_period argument as one of the following: weekly, monthly, bimonthly, quarterly, biannual, yearly"
    
    prompt_list = [
    "Generate an analysis of the total number of leads taken over {time_period} time period for the entire sales team. Identify trends and insights into lead generation.",
    "Generate an analysis of the total number of tours booked over {time_period} time period for the entire sales team. Identify trends and insights into booking patterns.",
    "Generate an analysis of the average number of tours booked per lead over {time_period} time period for the entire sales team. Identify trends and insights into conversion rates.",
    "Generate an analysis of the average number of applications submitted per booked tour over {time_period} period for the entire sales team. Identify trends and insights into application rates.",
    "Generate an analysis of the average number of applications submitted per lead over {time_period} time period for the entire sales team. Identify trends and insights into overall application efficiency.",
    "Generate an analysis of total confirmed revenue, pending revenue, and revenue runrate over {time_period} time period for the entire sales team. Identify trends and insights into revenue generation.",
    "Generate an analysis of the number of tours in the pipeline, average deal value, and average close rate over {time_period} time period for the entire sales team. Identify trends and insights into deal progression.",
    ]
    
    results = ' '.join([agent.run(prompt.format(time_period=time_period)) for prompt in prompt_list])
    
    return results

# Define Flask endpoints
@app.route('/rep_performance/<int:rep_id>', methods=['GET'])
def get_rep_performance(rep_id):
    result = get_insights_for_representative(rep_id)
    return jsonify(result)

@app.route('/team_performance', methods=['GET'])
def get_team_performance():
    result = get_insights_for_team()
    return jsonify(result)

@app.route('/performance_trends/<time_period>', methods=['GET'])
def get_performance_trends(time_period):
    result = get_insights_periodically(time_period)
    return jsonify(result)

if __name__ == '__main__':
    clean_data()
    app.run()
