"""
    Esse script tem como objetivo obter todos os usuários que não fizeram uso do
    acesso IAM nos ultimos 55 dias.
"""

import json
from boto3 import Session
from datetime import datetime

ACCESS_KEY = ''
SECRET_KEY = ''

session = Session(aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

client = session.client('iam')
users = client.list_users()

parse = json.dumps(users, indent=4, sort_keys=True, default=str)
response = json.loads(parse)
parse_dict = dict(response)

flagged_users = []

for item in parse_dict['Users']:
    flagged_user = {}
    for key in item:
        if key == 'PasswordLastUsed':
            last_used = item['PasswordLastUsed'][:19]
            last_used_date = datetime.strptime(last_used, '%Y-%m-%d %H:%M:%S')
            last_activity = datetime.now(last_used_date.tzinfo) - last_used_date

            if last_activity.days >= 55:
                flagged_user['username'] = item['UserName']
                flagged_user['last_activity'] = last_activity.days

                flagged_users.append(flagged_user)
            else:
                continue

with open('lista_usuarios.xls', 'w') as file:
    for user in flagged_users:
        file.writelines("Usuario: %s\n" % user['username'])
        file.writelines("Dias sem uso: %s\n" % user['last_activity'])