import streamlit as st
from dotenv import load_dotenv
import utilities.password_check as pwd
import os

load_dotenv(override=True)
password = os.getenv('PASSWORD')

if not pwd.check_password(password):  
    st.stop()


st.markdown("""            
    # Data Source Selection                    
    """)

with st.container(border=True):
        st.image("images/overall_flow.png", caption="Example screenshot of Chatbot output", use_column_width=True)

st.markdown("""            
    ## Screenshot example of Chatbot                  
    """)

with st.container(border=True):
        st.image("images/overall_flow_eg.png", caption="Example screenshot of Chatbot output", use_column_width=True)


st.markdown("""            
    # Agentic Flow    
            """)

with st.container(border=True):
        st.image("images/agentic_flow.png", caption="Example screenshot of Chatbot output", use_column_width=True)


st.markdown("""            
    ## Screenshot example of Agentic output
    """)

with st.container(border=True):
        st.image("images/agentic_flow_eg.png", caption="Example screenshot of agent output", use_column_width=True)