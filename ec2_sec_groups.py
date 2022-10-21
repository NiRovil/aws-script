"""
    Esse script tem como objetivo listar todos os Security Groups, filtrando somente
    os IP Permissions.
"""

from boto3 import Session

ACCESS_KEY = ''
SECRET_KEY = ''

session = Session(aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

client = session.client('ec2', 'us-east-1')
response = client.describe_security_groups()

port = 22

with open('sec_groups.txt', 'w') as file:
    for sec_groups in response['SecurityGroups']:
        for ip_perm in sec_groups['IpPermissions']:
            if 'FromPort' in ip_perm.keys():
                if ip_perm['FromPort'] == port:
                    file.write(f'O grupo: {sec_groups["GroupName"]} está rodando na porta: {str(ip_perm["FromPort"])}, tipo FROM\n')

            if 'ToPort' in ip_perm.keys():
                if ip_perm['ToPort'] == port:
                    file.write(f'O grupo: {sec_groups["GroupName"]} está rodando na porta: {str(ip_perm["ToPort"])}, tipo TO\n')


with open('sec_groups_egress.txt', 'w') as file:
    for sec_groups in response['SecurityGroups']:
        for ip_perm in sec_groups['IpPermissionsEgress']:
            file.write(f'{sec_groups["GroupName"]} - {sec_groups["IpPermissionsEgress"]}\n')
