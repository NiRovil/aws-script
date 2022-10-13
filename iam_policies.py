"""
    Esse script tem como objetivo obter todas as policies e seus respectivos atributos. 
"""

import json
from boto3 import Session

ACCESS_KEY = ''
SECRET_KEY = ''

session = Session(aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

client = session.client('iam')
policies = client.list_policies()

with open('arquivo.txt', 'w') as file:
    for item in policies['Policies']:
        get_policy = client.get_policy(PolicyArn=item['Arn'])

        for policy in get_policy['Policy']:
            get_policy_version = client.get_policy_version(PolicyArn=item['Arn'], VersionId=get_policy['Policy']['DefaultVersionId'])
            
            parse = json.dumps(get_policy_version, indent=4, sort_keys=True, default=str)
            response = json.loads(parse)
            parse_dict = dict(response)

        for version in parse_dict:
            file.write('{\"%s\": %s},\n' % (get_policy['Policy']['PolicyName'],parse_dict['PolicyVersion']))