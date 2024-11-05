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
    goal="Understand the audit report findings and propose remediation steps."
         "Understand AWS security controls and the risks."
         "Ensure that AWS cloud resources are secure by default.",
    tools=[tool_read_controls],
    verbose=False,
    backstory="""\
               As an AWS Cloud Security Architect, you are to understand the audit report findings and propose remediation steps.
               Your prowess in understanding the AWS security controls and remediation steps is unmatched.
               Your skills help identify security risks and gaps arising from misconfigured cloud resources."""
)


im8_auditor = Agent(
    role="IM8 Auditor",
    goal="Identify and flag out non-compliant AWS resources in accordance to IM8 clauses.",
    tools=[tool_read_cloudscape],
    verbose=False,
    backstory=("""\
               Equipped with analytical prowess, you analyze cloud reports and identify AWS resources that are non-compliant and flag them out for security remediation."""
    )
)

cloud_engineer = Agent(
    role="AWS Cloud Engineers",
    goal="List down detailed steps to achieve the setup requirements in the target AWS environment.",
    tools=[tool_read_environment],
    verbose=False,
    backstory=("""\
               Equipped with great operation and administration skills, you excel in configuring AWS resources given the setup requirements."""
    )
)

security_task = Task(
    description="""/
        Analyze the security controls obtained from the previous steps to extract key compliance and security mitigation required. 
        Use the tools to gather content and identify and propose changes to the cloud resources.""",
    expected_output="A structured list of proposed changes to cloud resources configuration with security controls and mitigation steps.",
    agent=security_architect,
    async_execution=False
)

audit_report_task = Task(
    description="""Compile a detailed cloud resources risk profile based on the current file. Utilize tools to extract and synthesize information from the file.""",
    expected_output="A list of AWS cloud resources that is non-compliant according to IM8 clauses.",
    agent=im8_auditor,
    async_execution=False
)


remediation_task = Task(
    description="""\
        Using the audit report and proposed changes obtained from previous tasks, propose changes to the cloud setup to mitigate all non-compliant areas. 
        Make sure to propose practical steps in making the changes and don't make up any information. 
        Update every non-compliant resource type.""",
    expected_output=
        "A concise remediation plan with clear detailed security risk mitigation steps for each non-compliant AWS cloud resource.",
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