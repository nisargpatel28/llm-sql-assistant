import google.generativeai as genai
import sqlite3
import os
import streamlit as st
from dotenv import load_dotenv
import re
load_dotenv()  # Load all the env variables


# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to Load Gemini Model and provide sql query response


def get_gemini_response(question, prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content([prompt[0], question])
        return response.text
    except Exception as e:
        error_message = str(e)
        if "429" in error_message or "quota" in error_message.lower() or "exceeded" in error_message.lower():
            raise Exception(
                "⚠️ API Quota Exceeded: You have reached the rate limit for the Gemini API. Please wait a few moments and try again, or check your API plan and billing details at https://ai.dev/usage")
        else:
            raise Exception(f"API Error: {error_message}")

# Function to format SQL results into human-readable text


def format_results_to_text(question, sql_results):
    try:
        model = genai.GenerativeModel('gemini-2.5-pro')
        format_prompt = f"""
    The user asked: "{question}"
    
    The SQL query returned the following results:
    {sql_results}
    
    Please provide a clear, human-readable answer based on these results. 
    Format the answer in a conversational way without showing raw data tuples.
    """
        response = model.generate_content(format_prompt)
        return response.text
    except Exception as e:
        error_message = str(e)
        if "429" in error_message or "quota" in error_message.lower() or "exceeded" in error_message.lower():
            raise Exception(
                "⚠️ API Quota Exceeded: You have reached the rate limit for the Gemini API. Please wait a few moments and try again, or check your API plan and billing details at https://ai.dev/usage")
        else:
            raise Exception(f"API Error: {error_message}")

# Function to retrieve data from the sql database


def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows


# Define your prompt
prompt = ["""
    You are an expert financial data analyst. You have access to a SQL database named 'fintech.db' which contains a table called 'fintech' with the following columns:
    - id (INT, Primary Key)
    - transaction_id (INT)
    - amount (FLOAT)
    - status (VARCHAR(25))
    - date (TEXT)
    - description (TEXT)
    Use your SQL skills to analyze the data and provide insights based on user queries.
    The SQL Command will be something like: "SELECT * FROM fintech WHERE status = 'Completed';"\n
    Example Queries:
    1. "What is the total amount of completed transactions?"
    In above case, the SQL command will be:
        "SELECT SUM(amount) FROM fintech WHERE status = 'Completed';"
    2. "How many transactions are pending?"
    In above case, the SQL command will be:
    "SELECT COUNT(*) FROM fintech WHERE status = 'Pending';"
    3. "List all failed transactions."
    In above case, the SQL command will be:
    "SELECT * FROM fintech WHERE status = 'Failed';"
    Also, the sql code should be enclosed within triple backticks (```) in your response.

"""
          ]

# Streamlit App

st.set_page_config(page_title="Financial Data Analyst with Gemini Pro",
                   page_icon=":bar_chart:", layout="wide")
st.title("Financial Data Analyst with Gemini Pro :bar_chart:")
question = st.text_input("Ask your financial data related question here:")
submit = st.button("Get Answer")

# if submit button is clicked
if submit:
    try:
        response = get_gemini_response(question, prompt)
        print("Gemini Pro Response:", response)

        # Extract SQL query from the response (between triple backticks)
        sql_match = re.search(r'```(.*?)```', response, re.DOTALL)
        if sql_match:
            sql_query = sql_match.group(1).strip()
            # Remove 'sql' language identifier if present
            sql_query = re.sub(r'^sql\n', '', sql_query)
            data = read_sql_query(sql_query, 'fintech.db')

            # Format the results into human-readable text
            formatted_answer = format_results_to_text(question, data)
            st.subheader("Answer:")
            st.write(formatted_answer)
        else:
            st.error("Could not extract SQL query from the response")
    except Exception as e:
        st.error(str(e))
