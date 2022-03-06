"""
Availability Zones  : ap-northeast-2
AMI                 : Amazon Machine Image
IAM Role            : how to set Session Manager in iam role
EC2 Instance        : how to use Session Manager in EC2 instance
                      how to use user data
"""

import json
import pulumi
import pulumi_aws as aws

## Availability Zones
ap_northeast_2_zones = aws.get_availability_zones()
zones = ['ap-northeast-2a', 'ap-northeast-2c']

## Get ami
ec2_ami = aws.ec2.get_ami(
    filters=[
        aws.ec2.GetAmiFilterArgs(
            name="name",
            values=["amzn2*"],
        )
    ],
    most_recent=True,
    owners=["amazon"])

## Ec2 NodeGroup Role
ec2_role = aws.iam.Role(
    'ec2-nodegroup-iam-role',
    assume_role_policy=json.dumps({
        'Version': '2012-10-17',
        'Statement': [
            {
                'Action': 'sts:AssumeRole',
                'Principal': {
                    'Service': 'ec2.amazonaws.com'
                },
                'Effect': 'Allow',
                'Sid': ''
            }
        ],
    }),
)

aws.iam.RolePolicyAttachment(
    'ec2-nodegroup-policy-attachment',
    role=ec2_role.id,
    policy_arn='arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore',
)

testSSMProfile = aws.iam.InstanceProfile(
    "testSSMProfile", 
    name="testSSMProfile", 
    role=ec2_role)

## EC2 instance
ec2_servers = []
for zone in zones:
    server = aws.ec2.Instance(
        resource_name=f"ec2-server-{zone}",
        ami=ec2_ami.id,
        instance_type="t2.micro",
        availability_zone=f"{zone}",
        #key_name = "aws-iac-remote-login-key",
        iam_instance_profile=testSSMProfile,
        user_data=f"""#!/bin/bash
            set -ex
            cd /tmp
            sudo yum install -y https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_amd64/amazon-ssm-agent.rpm
            sudo systemctl enable amazon-ssm-agent
            sudo systemctl start amazon-ssm-agent
            """,
        tags={"Name": f"my-app-server-{zone}"}
        )
    ec2_servers.append(server)

pulumi.export("availability zones", ap_northeast_2_zones)
pulumi.export("ami id", ec2_ami.id)
for i in range(0, 2):
    pulumi.export(f"instance id-{i}", ec2_servers[i].id)

"""
Setup Session Manager for Windows: https://s3.amazonaws.com/session-manager-downloads/plugin/latest/windows/SessionManagerPluginSetup.exe
To modify your PATH variable (Windows)
C:\Program Files\Amazon\SessionManagerPlugin\bin
session-manager-plugin
aws ssm start-session --target instance_id (i-09181f7fab11ee265)
"""

