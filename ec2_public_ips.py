"""
    Esse script tem como objetivo listar todas as EC2 que contém IP público.
"""

import jmespath
import json
from boto3 import Session

ACCESS_KEY = ''
SECRET_KEY = ''

session = Session(aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

client = session.client('ec2', 'us-east-1')
ec2 = client.describe_instances()

names = [name for name in jmespath.search("Reservations[*].Instances[*].KeyName", ec2)]
ips = [ip for ip in jmespath.search("Reservations[*].Instances[*].PublicIpAddress", ec2)]

parse = json.dumps(ec2, indent=4, sort_keys=True, default=str)
response = json.loads(parse)
parse_dict = dict(response)

with open('public_ips.txt', 'w') as file:
    for reservations in parse_dict['Reservations']:
        for instance in reservations['Instances']:
            if 'KeyName' and 'PublicIpAddress' in instance:
                file.writelines(instance['InstanceId'] + ' ' +instance['PublicIpAddress']+'\n')
            continue