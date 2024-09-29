import sqlite3
import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up the API keys
if not os.environ.get('GROQ_API_KEY'):
    os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
if not os.environ.get('LANGCHAIN_API_KEY'):
    os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
    os.environ['LANGCHAIN_TRACING_V2'] = 'true'

# Import after loading environment variables
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain_community.agent_toolkits import create_sql_agent

# Database and LLM setup
db = SQLDatabase.from_uri('sqlite:///job_data.db')
llm = ChatGroq(model='llama-3.1-70b-versatile')
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)

# CSS for aesthetic customization
st.markdown("""
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f7f7f7;
        }
        .title {
            text-align: center;
            color: #4CAF50;
            font-size: 3em;
            margin-bottom: 20px;
        }
        .message-box {
            width: 100%;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            font-size: 1.2em;
            border: 1px solid #ddd;
        }
        .submit-btn {
            background-color: #4CAF50;
            color: white;
            font-size: 1.1em;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
        }
        .chat-container {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .chat-message {
            background-color: #f1f1f1;
            padding: 10px;
            margin: 5px 0;
            border-radius: 8px;
        }
        .user-message {
            text-align: right;
            background-color: #4CAF50;
            color: white;
        }
        .bot-message {
            text-align: left;
        }
    </style>
""", unsafe_allow_html=True)

# Title at the top
st.markdown('<h1 class="title">Talk to SkillMap</h1>', unsafe_allow_html=True)

# Chat interface container
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# User input box
query = st.text_input("Ask anything!!", key="message_input", label_visibility="hidden", placeholder="Ask anything!!")
# When the user submits a question
if query:
    with st.spinner("Thinking..."):
        try:
            response = agent_executor.invoke({'input': """You are working with a database that has the following schema:
    Table: job_data
    Job Title,Degree Requirements,Skills,Tech Skills,Tools,Tech Languages,Libraries,Company,Ratings,Experience,Location
    DATA ANALYST,"BACHELORS DEGREE IN COMPUTER SCIENCE, MATHEMATICS, STATISTICS, ECONOMIC","STATISTICAL ANALYSIS, DATA MODELING, DATA MANIPULATION, ANALYTICAL, POWER BI, DATA ANALYTICS, DATA VISUALIZATION, SQL","STATISTICAL ANALYSIS, DATA MODELING, DATA MANIPULATION, ANALYTICAL, DATA ANALYTICS, DATA VISUALIZATION","POWER BI, SQL",,MASAI SCHOOL,4.0,3.0,0,

    basically 
    Job Title - contains name of the job role
    Degree Requirements - if any degree is required it is present else NONE
    Skills - all the skills required for the job role are present each separated by commas 
    Tools - name of different tools separated by commas
    Tech Languages - name of different tech languages used
    Libraries - name of different libraries separated by commas
    Company - name of the company providing job role
    Rating - the rating given to the job role
    Experience - range of experience it is sometimes represented as 4y or something like 4 which usually means 4 years
    Location - the location the job role is present at
    """ + query})['output']  # Execute the query using the agent
        except Exception as e:
            response = llm.invoke(query).content
        if "I don't know" in response:
            response = llm.invoke(query).content
        st.session_state.chat_history.append({"role": "bot", "message": response})
        st.session_state.chat_history.append({"role": "user", "message": query})

# Display the chat history dynamically
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for chat in st.session_state['chat_history'][::-1]:
    if chat['role'] == 'user':
        st.markdown(f'<div class="chat-message user-message">{chat["message"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message bot-message">{chat["message"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
