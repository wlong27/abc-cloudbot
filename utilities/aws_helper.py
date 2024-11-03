import boto3
import json

# Retrieve information from AWS environment
def list_ec2_instances_and_security_groups(aws_access_key_id, aws_secret_access_key, aws_session_token):
    ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token, region_name='ap-southeast-1')

    response = ec2_client.describe_instances()
    instances_info = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            security_groups = instance['SecurityGroups']

            # Prepare security group info
            sg_info = []
            for sg in security_groups:
                sg_id = sg['GroupId']
                sg_name = sg['GroupName']
                sg_rules = get_security_group_rules(sg_id, aws_access_key_id, aws_secret_access_key, aws_session_token)  # Get the rules for the security group

                # Add to security group info with clearer labels
                sg_info.append({
                    'SecurityGroup': {
                        'SecurityGroupId': sg_id,
                        'SecurityGroupName': sg_name,
                        'Rules': sg_rules
                    }
                })

            # Add instance info to the main dictionary with clearer labels
            instances_info.append({
                'InstanceId': instance_id,
                'SecurityGroups': sg_info
            })
    return instances_info

def list_ec2_instances_and_security_groups_llm(aws_access_key_id, aws_secret_access_key, aws_session_token):
    ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token, region_name='ap-southeast-1')

    response = ec2_client.describe_instances()
    instances_info = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            security_groups = instance['SecurityGroups']

            # Prepare security group info
            sg_info = f'Information on my EC2 instances in my AWS account. This instanceId={instance_id} has the following security groups:'
            for sg in security_groups:               
                sg_id = sg['GroupId']
                sg_name = sg['GroupName']
                sg_rules = get_security_group_rules(sg_id, aws_access_key_id, aws_secret_access_key, aws_session_token)  # Get the rules for the security group
               
                sg_info += f"GroupId={sg_id} with GroupName={sg_name} and with Rules={json.dumps(sg_rules)}, "                           

            # Add instance info to the main dictionary with clearer labels
            instances_info.append({
                'instanceId': instance_id,    
                'content': sg_info
            })
    return instances_info

def list_s3_buckets(aws_access_key_id, aws_secret_access_key, aws_session_token):
    s3_client = boto3.client('s3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
    )
    buckets_info = s3_client.list_buckets()
    return buckets_info
   
def get_security_group_rules(sg_id, aws_access_key_id, aws_secret_access_key, aws_session_token):
    ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token, region_name='ap-southeast-1')
    
    response = ec2_client.describe_security_groups(GroupIds=[sg_id])
    security_group = response['SecurityGroups'][0]

    rules = {
        'IngressRules': [],
        'EgressRules': []
    }

    # Get ingress rules
    for rule in security_group.get('IpPermissions', []):
        rules['IngressRules'].append({
            'FromPort': rule.get('FromPort'),
            'ToPort': rule.get('ToPort'),
            'Protocol': rule.get('IpProtocol'),
            'CidrBlocks': [ip_range['CidrIp'] for ip_range in rule.get('IpRanges', [])]
        })

    # Get egress rules
    for rule in security_group.get('IpPermissionsEgress', []):
        rules['EgressRules'].append({
            'FromPort': rule.get('FromPort'),
            'ToPort': rule.get('ToPort'),
            'Protocol': rule.get('IpProtocol'),
            'CidrBlocks': [ip_range['CidrIp'] for ip_range in rule.get('IpRanges', [])]
        })

    return rules

def get_account_aliases(aws_access_key_id, aws_secret_access_key, aws_session_token):
    iam_client = boto3.client('iam', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token,)

    # Retrieve the account aliases
    response = iam_client.list_account_aliases()

    # Extract the account aliases from the response
    account_aliases = response.get('AccountAliases', [])

    # Check if there are any aliases and print them
    if account_aliases:
        account_name = account_aliases[0]  # Get the first alias (if exists)
        return account_name
    else:
        return None