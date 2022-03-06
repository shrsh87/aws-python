"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws

NAME = 'iac-example'

# VPC

vpc = aws.ec2.Vpc(
    resource_name = f'vpc-{NAME}',
    cidr_block = "10.0.0.0/16",
    enable_dns_hostnames = True,
    enable_dns_support = True,
    tags = {
        'Name': 'my-vpc',
    },
)

# Subnet: public/private/db

zones = ['ap-northeast-2a', 'ap-northeast-2c']
public_subnet_ids = []
private_subnet_ids = []
db_subnet_ids = []

public_zone_size, private_zone_size, db_zone_size = 1, 5, 10

for zone in zones:
    if zone == 'ap-northeast-2a':
        zone_index = 1
    elif zone == 'ap-northeast-2c':
        zone_index = 3

    # public subnet (for web/jump)
    public_subnet = aws.ec2.Subnet(
        f'my-public-web-subnet-{zone}',
        assign_ipv6_address_on_creation = False,
        vpc_id = vpc.id,
        map_public_ip_on_launch = True,
        cidr_block = f'10.0.{public_zone_size*zone_index}.0/24',
        availability_zone = zone,
        tags={
            'Name': f'my-public-web-subnet-{zone}',
        },
    )
    public_subnet_ids.append(public_subnet.id)

    # private subnet (for app)
    private_subnet = aws.ec2.Subnet(
        f'my-private-app-subnet-{zone}',
        assign_ipv6_address_on_creation = False,
        vpc_id = vpc.id,
        cidr_block = f'10.0.{private_zone_size*zone_index}.0/24',
        availability_zone = zone,
        tags = {
            'Name': f'my-private-app-subnet-{zone}',
        },
    )
    private_subnet_ids.append(private_subnet.id)

    # private subnet (for db)
    db_subnet = aws.ec2.Subnet(
        f'my-private-db-subnet-{zone}',
        assign_ipv6_address_on_creation = False,
        vpc_id = vpc.id,
        cidr_block = f'10.0.{db_zone_size*zone_index}.0/24',
        availability_zone = zone,
        tags = {
            'Name': f'my-private-db-subnet-{zone}',
        },
    )
    db_subnet_ids.append(db_subnet.id)    

pulumi.export("public subnet ids", public_subnet_ids)
pulumi.export("private subnet ids", private_subnet_ids)
pulumi.export("db subnet ids", db_subnet_ids)