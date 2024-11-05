from dotenv import load_dotenv
from crewai import Agent, Task, Crew

load_dotenv(override=True)

from crewai_tools import (
  FileReadTool,
  JSONSearchTool,
  CSVSearchTool
)

tool_read_controls = FileReadTool(file_path='./data/aws_ec2_controls.json')
tool_read_cloudscape = FileReadTool(file_path='./data/cloudscape_report.csv')
tool_read_environment = FileReadTool(file_path='./data/aws_environment.json')

# Agent 1: Researcher
security_architect = Agent(
    role="AWS Cloud Security Architect",
    goal="Summarize AWS security controls and the risks."
         "Ensure that AWS cloud resources are secure by default.",
    tools=[tool_read_controls],
    verbose=False,
    backstory="""As an AWS Cloud Security Architect, you are to recommend changes to the AWS resources and propose steps to secure them.
               Your prowess in understanding the AWS security controls and cloud architecture is unmatched.
               You are skilled in identifying security risks and gaps in AWS cloud resources."""
)


im8_auditor = Agent(
    role="IM8 Auditor",
    goal="Identify and flag out non-compliant AWS resources in accordance to IM8 clauses.",
    tools=[tool_read_cloudscape],
    verbose=False,
    backstory=("""Equipped with analytical prowess, you analyze reports and identify AWS resources that are non-compliant and flag them out for security remediation."""
    )
)

cloud_engineer = Agent(
    role="AWS Cloud Engineers",
    goal="List down detailed steps to change the AWS resources setup and configuration.",
    tools=[tool_read_environment],
    verbose=False,
    backstory=("""Equipped with great operation and administration skills, you are good in configuring AWS resources given the compliance requirements."""
    )
)

security_task = Task(
    description="""/
        Analyze the security controls obtained and summarize the security mitigation required. 
        Use the tools to gather content and identify and propose changes to the AWS cloud resources.""",
    expected_output="A structured list of proposed changes to cloud resources configuration with security controls and mitigation steps.",
    agent=security_architect,
    async_execution=False
)

audit_report_task = Task(
    description="""Compile an audit report listing the non-compliant AWS cloud resources according to IM8 clauses. 
    Utilize tools to extract the non-compliant AWS resources name and information from the file.""",
    expected_output="A security report in markdown listing all the non-compliant AWS cloud resources, their information and relevant mitigation steps.",
    agent=im8_auditor,
    async_execution=False
)


remediation_task = Task(
    description="""Using the audit report from previous tasks, create a remediation plan with changes to the AWS cloud resources.
        The plan should address all the non-compliant AWS resources in the security report.
        Each AWS resources must have mitigation steps to mitigate the security risk flagged in the audit report.
        """,
    expected_output="""A concise remediation plan with the necessary details and AWS resources listed in bullet points in markdown.
    """,
    output_file="security_recommendations.md",
    context=[security_task, audit_report_task],
    agent=cloud_engineer
)

crew = Crew(
    agents=[security_architect,
            im8_auditor,
            cloud_engineer],

    tasks=[security_task,
           audit_report_task,
           remediation_task],

    verbose=True
)