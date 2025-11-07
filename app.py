from dotenv import load_dotenv
load_dotenv() ## Load all the env variables

import streamlit as st
import os
import sqlite3

import google.generativeai as genai

## Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to Load Gemini Model and provide sql query response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

## Function to retrieve data from the sql database
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

##Define your prompt
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

#Streamlit App

st.set_page_config(page_title="Financial Data Analyst with Gemini Pro", page_icon=":bar_chart:", layout="wide")
st.title("Financial Data Analyst with Gemini Pro :bar_chart:")
question = st.text_input("Ask your financial data related question here:")
submit = st.button("Get Answer")

# if submit button is clicked
if submit:
    response = get_gemini_response(question, prompt)
    print("Gemini Pro Response:", response)
    data = read_sql_query(response, 'fintech.db')
    st.subheader("Answer:")
    for row in response:
        print(row)
        st.header(row)
        