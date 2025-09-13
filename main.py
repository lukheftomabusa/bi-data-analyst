from agent import my_agent

if __name__ == "__main__":
    # Example task for the agent
    task = "Summarize the sales data for this month."
    
    result = my_agent.run(task)
    print("Agent Response:", result)
    import os
from dotenv import load_dotenv
from crewai import Agent

# Load environment variables (for API keys etc.)
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# =====================
# Define Core Agents
# =====================

data_collector = Agent(
    role="Data Collector",
    goal="Fetch and load business data from files or databases.",
    backstory="You are skilled at finding and retrieving the right datasets.",
    openai_api_key=openai_api_key
)

data_cleaner = Agent(
    role="Data Cleaner & Preparer",
    goal="Clean and preprocess raw data to make it ready for analysis.",
    backstory="You specialize in handling missing values, duplicates, and formatting.",
    openai_api_key=openai_api_key
)

data_analyst = Agent(
    role="Business Intelligence & Data Analyst",
    goal="Analyze business data, extract insights, and calculate KPIs.",
    backstory="You are an expert BI analyst who helps businesses make data-driven decisions.",
    openai_api_key=openai_api_key
)

visualization_agent = Agent(
    role="Visualization Specialist",
    goal="Generate charts, tables, and summaries of the analysis results.",
    backstory="You are an expert in data visualization and storytelling with data.",
    openai_api_key=openai_api_key
)

report_writer = Agent(
    role="Report Writer",
    goal="Write structured and clear BI reports from analysis results.",
    backstory="You create professional summaries and detailed reports for decision makers.",
    openai_api_key=openai_api_key
)

business_advisor = Agent(
    role="Business Strategy Advisor",
    goal="Recommend business actions based on insights and trends.",
    backstory="You translate numbers into actionable strategies for management.",
    openai_api_key=openai_api_key
)

# =====================
# Supporting Agents
# =====================

orchestrator = Agent(
    role="Orchestrator",
    goal="Decide which agent to activate in the correct workflow order.",
    backstory="You are the manager of all other agents and make sure tasks are completed correctly.",
    openai_api_key=openai_api_key
)

memory_agent = Agent(
    role="Memory Keeper",
    goal="Remember past tasks, results, and context for consistency.",
    backstory="You act as a memory store, so the system doesn’t forget previous runs.",
    openai_api_key=openai_api_key
)

interface_agent = Agent(
    role="Interface Agent",
    goal="Communicate with the user and deliver results in a friendly format.",
    backstory="You are the bridge between the user and the analysis team.",
    openai_api_key=openai_api_key
)

# =====================
# Example Workflow
# =====================

if __name__ == "__main__":
    # Example task flow
    tasks = [
        ("Data Collector", "Fetch sales data from the dataset for July."),
        ("Data Cleaner", "Clean the sales data by handling missing values and duplicates."),
        ("Data Analyst", "Analyze the cleaned data and summarize key sales trends."),
        ("Visualization", "Create a chart of revenue by product category."),
        ("Report Writer", "Write a short report summarizing the analysis."),
        ("Business Advisor", "Suggest business actions based on the report.")
    ]

    # Run tasks in sequence
    for agent_name, task in tasks:
        print(f"\n🔹 {agent_name} Task: {task}")

        if agent_name == "Data Collector":
            result = data_collector.run(task)
        elif agent_name == "Data Cleaner":
            result = data_cleaner.run(task)
        elif agent_name == "Data Analyst":
            result = data_analyst.run(task)
        elif agent_name == "Visualization":
            result = visualization_agent.run(task)
        elif agent_name == "Report Writer":
            result = report_writer.run(task)
        elif agent_name == "Business Advisor":
            result = business_advisor.run(task)
        else:
            result = orchestrator.run(f"Manage task: {task}")

        # Memory agent keeps track
        memory_agent.run(f"Remember this result: {result}")

        # Deliver results through interface
        interface_agent.run(f"Deliver this result to the user: {result}")

        print(f"✅ {agent_name} Response:\n{result}")

        import pandas as pd
import guardrails
import sqlite3  # example for SQL DB connection

# Example: user input requesting data
user_input = "Show me all customer emails and salary"

# 1️⃣ Check input first
if guardrails.check_input(user_input):

    # 2️⃣ Connect to your SQL database safely
    conn = sqlite3.connect("example_db.sqlite")  # replace with your DB
    query = "SELECT Name, Email, Salary, Department FROM Customers"
    df = pd.read_sql_query(query, conn)
    
    # 3️⃣ Check DataFrame for sensitive info
    if guardrails.check_dataframe(df):
        safe_df = df
    else:
        # Remove sensitive columns automatically
        safe_df = guardrails.sanitize_dataframe(df)
    
    # 4️⃣ Check output before sending
    if guardrails.check_output(safe_df):
        print("Safe output:\n", safe_df)
    else:
        print("Output blocked by guardrails")
    
    conn.close()

else:
    print("Input blocked by guardrails")

