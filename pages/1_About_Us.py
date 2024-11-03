import streamlit as st
from dotenv import load_dotenv
import utilities.password_check as pwd
import os

load_dotenv()
password = os.getenv('PASSWORD')

if not pwd.check_password(password):  
    st.stop()

st.markdown("""
### Describe the problem you are trying to solve
As a GCC cloud user, we are responsible for the provisioned resources, the cloud design and setup. These include configurations, settings and security controls that are necessary for IM8 compliance. There are also numerous best practices, guidelines and frameworks published by the CSPs. It is an iterative and time-consuming process to review and map all the above information to different cloud setup.  
            How do we ensure that the cloud setup is compliant, secure, reliable, performant and costs optimized in a fast and efficient manner?   
            Is there a way we can evaluate and verify all the different cloud setup and receive accurate recommendations for changes?

### What is wrong with the current situation?
Current approach is more reactive in nature, where we wait for alerts, scans and/or audits to happen. Current tools are limited e.g. CloudScape reports need further interpretation of security rules and controls. AI tools such as Amazon Q does not provide deeper insight or targeted solutions with WOG context. Trusted advisor's checks require assessment and research into the remediation steps. All these are further compounded by the dynamic nature of cloud resources. Depreciated/New features and settings need to be taken into account in the periodic review process.

### What is the magnitude of this problem?
This problem affects the public service officers and vendors using GCC.
            
### How would you try to solve this problem?
We plan to implement an agentic system that evaluate any cloud setup on the click on a button. The system will be loaded with web-scrapped data from published security controls and well-architected framework. The system will also have access to the cloud environment details via the end-user GCC SSO credentials. Additionally, the system will provide a chat interface for ad-hoc queries. This allows the user to efficiently and rapidly understand their cloud setup and design. 

### How would you think Large Language Model(s) can be used to support your solution?
LLMs will be the agents required for cloud evaluation. For the chat interface, the LLM will combine with RAG flow to provide accurate responses to the user queries. The system will leverage on LLMs for NLP and generative capabilities to provided up-to-date cloud recommendations. By using LLMs for evaluation, we can reduce human effort, biasness and errors that occur with larger scale of cloud setup. LLMs will enable the synthesis of larger amount of data and information.

### Are there any alternative solutions you have considered?
Alternatives include WOG CloudScape, Amazon Q, Trusted Advisors and many third-party tools. These are great tools and work well for focused and silo tasks. Potentially, we can integrate with these tools in the agentic system to help perform the cloud evaluation automatically in a unified platform.

### What are relevant data do you currently collect and already have?
We can web-scrapped/search online public data from the Internet. For the current setup, this will be done on-demand, and hence no data will be stored. 
For IM8 requirements, the data will be collected from the Security Controls.

### Is there any data that require approval to be used in the project?
No. Data used is already information accessible by the users using their own credentials. The data acccessed is with their own roles.

### What is the Classification/Sensitivity of Data?
Cloud environments settings and configuration will follow the system classification. Public internet data will be classified as “Official-Open(non-sensitive)”

### Can the data be down class to “Official (Closed)” by using mock data (or dummy data) of the same structure and characteristics?
Yes, all the data required for this POC can be mocked.

""")





