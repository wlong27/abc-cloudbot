__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import os
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
#from langchain_text_splitters import RecursiveJsonSplitter
import utilities.qdrant_helper as qhelper
import utilities.webcrawler as webcrawler
import json
import traceback
import pandas as pd
import utilities.password_check as pwd
import utilities.aws_helper as aws

from agents.security_agent import crew



load_dotenv(override=True)

password = os.getenv('PASSWORD')

if not pwd.check_password(password):  
    st.stop()

openai_api_key = os.getenv('OPENAI_API_KEY')
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_session_token = os.getenv('AWS_SESSION_TOKEN')

# side bar for key entries
with st.sidebar:
    if openai_api_key is None:
        st.warning("Please add your OpenAI API key to continue.")
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    
    if aws_access_key_id is None or aws_secret_access_key is None or aws_session_token is None:
        st.info("Add AWS credentials for AWS account.")
        aws_access_key_id = st.text_input("AWS access key ID", key="aws_access_key_id", type="password")
        aws_secret_access_key = st.text_input("AWS secret access key", key="aws_secret_access_key", type="password")
        aws_session_token = st.text_input("AWS session token", key="aws_session_token", type="password")

with st.expander("ℹ️ Disclaimer"):
     st.write("""

IMPORTANT NOTICE: This web application is developed as a proof-of-concept prototype. The information provided here is NOT intended for actual usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.

Always consult with qualified professionals for accurate and personalized advice.

""")

st.warning("⚠️ For data sources classified up to OFFICIAL(CLOSED)/NON-SENSITIVE only.")

# Streamlit app UI
st.title("CloudBot")

# Data retrieval
st.subheader("Data Source")
st.warning("Use mock data to try this POC.")

option = st.radio(
    "Use mock data?",
    ("No", "Yes")
)
    
if option == "Yes":
    # 1. Load mock data for 
    ec2_controls_file = 'data/aws_ec2_controls.json'
    if os.path.exists(ec2_controls_file):
        with open(ec2_controls_file, 'r') as file:
            ec2_controls_json = json.load(file)
            qhelper.embed_json(ec2_controls_json, 'description')           
            with st.expander('Show EC2 controls from AWS Security Hub.'):
                df = pd.DataFrame(ec2_controls_json)
                st.dataframe(df)
    # 2. Load mock data for CloudScape
    cloudscape_file = 'data/cloudscape_report.csv'
    if os.path.exists(cloudscape_file):
            with st.expander('Show CloudScape report.'):
                df = pd.read_csv(cloudscape_file)
                st.dataframe(df)
                cloudscape_items = df.to_dict(orient='records')
                qhelper.embed_json(cloudscape_items, 'Description',{"url": "CloudScape"})    
    # 3. Load mock data for AWS environment
    env_info_file = 'data/aws_environment.json'
    if os.path.exists(env_info_file):
        with open(env_info_file, 'r') as file:
            env_info = json.load(file)
            qhelper.embed_json(env_info, 'content', {"url": "AWS account"})           
            with st.expander('List AWS resources in account.'):
                df = pd.DataFrame(env_info)
                st.dataframe(df)


else:
    # 1. Webscrap the EC2 controls from AWS Security hub
    main_url = 'https://docs.aws.amazon.com/securityhub/latest/userguide/ec2-controls.html'
    if st.checkbox(f'[AWS Security Hub EC2 controls]({main_url})'):
        obj_list = webcrawler.security_hub_web_scrape(main_url)
        if obj_list:
            st.success(f'Retrieved {len(obj_list)} controls.')
            qhelper.embed_json(obj_list, 'description')
            with st.expander('Show all controls.'):
                df = pd.DataFrame(obj_list)
                st.dataframe(df)
            # splitter = RecursiveJsonSplitter(max_chunk_size=300)
            # texts = splitter.split_text(json_data=obj_list, convert_lists=True)
            # st.write(texts)
            # qhelper.embed_json_chunks(obj_list, {"url": main_url})
            
    # 2. Extract info from uploaded report
    if st.checkbox("[CloudSCAPE](https://cloudscape.tech.gov.sg)"):
        csv_file = st.file_uploader("Upload report", type="csv")
        if (csv_file):
            df = pd.read_csv(csv_file)
            with st.expander('Show CloudScape report'):
                st.dataframe(df)
            cloudscape_items = df.to_dict(orient='records')        
            qhelper.embed_json(cloudscape_items, 'Description',{"url": "CloudScape"})        

    # 3. Extract info from provided AWS environment
    if st.checkbox("AWS account"):
        try:
            if (aws_access_key_id and aws_secret_access_key and aws_session_token):                         
                # Get EC2 instances and SGs
                instances_info = aws.list_ec2_instances_and_security_groups_llm(aws_access_key_id, aws_secret_access_key, aws_session_token)
                account_alias = aws.get_account_aliases(aws_access_key_id, aws_secret_access_key, aws_session_token)
                if instances_info:     
                    st.success(f'Retrieved AWS information for `{account_alias}`')                                 
                    qhelper.embed_json(instances_info, 'content', {"url": "AWS account"})                   
            else:            
                st.markdown(f'<p style="color:red;">Missing AWS credentials.</p>', unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f'<p style="color:red;">{e}</p>', unsafe_allow_html=True)
            traceback.print_exc()
    else:
        instances_info = None
        buckets_info = None


st.subheader("Agentic Recommendations")
if st.button("Get Security Recommendations"):
    with st.spinner("Loading...please wait"):
        result = crew.kickoff()
        with st.expander("Show outputs"):
            st.write(f"{result}")    
    
st.subheader("Chat with Bot")

# Store conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Create a prompt template for chat
template = ChatPromptTemplate.from_messages([
    ("system", f"You are a helpful assistant."),
    ("human", f"""
Use the following AWS resource information in <PASSAGE> and chat history to answer the user's question. 
Each passage has a <NAME> which is the source of the document. 
After your answer, leave a blank line and then give the source name of the passages you answered from. 
Put them each in a new list comma separated keeping only the distinct unique source name and prefixed with SOURCES:.
The format of the source name to be placed in comma separate list. :
   
If there are no sources, you can remove the prefix.
If there are no passages, just answer to the best of your ability.
If you don't know the answer, don't try to make up an answer.

Example:

Question: What many EC2 instances do I have?
Response:
You have a total of 10 EC2 instances. Some are identified as non-compliant due to missing security controls.

SOURCES: [source_name](https://example.com)

     
----

---
{{context}}
---

Question: {{user_input}}
Response:

""")
])


if openai_api_key:
    chatmodel = ChatOpenAI(
            openai_api_key=openai_api_key, 
            streaming=True, 
            temperature=0.7, 
            model="gpt-4o-mini"
        )

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    #Accept user input and return response
    if prompt := st.chat_input("E.g. List me all my EC2 instances."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        retrieved_docs = qhelper.retrieve_context(prompt)
        
        with st.expander('Show retrieved context'):
            st.write(retrieved_docs)
        
        context = ''
        for doc in retrieved_docs:
            name = ''
            passage = ''
            if 'url' in doc:
                name = doc['url']
            else:
                name = 'UNKNOWN'            
            
            if 'content' in doc:
                passage = doc['content']
            elif isinstance(doc, dict):
                df = pd.json_normalize(doc)
                passage = df.to_markdown(index=False)
            else:
                passage = str(doc)    
            
            context += f"\n<NAME> {name} </NAME>"
            context += f"\n<PASSAGE> {passage} </PASSAGE>\n"
        
        # with st.expander('Show retrieved context'):
        #     st.write(context)
        with st.chat_message("assistant"):
            chain = template | chatmodel
            response = chain.stream({
                "user_input":prompt,
                "context": context
                })             
            response_stream = st.write_stream(response)         
        st.session_state.messages.append({"role": "assistant", "content": response_stream})
else:
    st.warning("Please add your OpenAI API key to continue.")