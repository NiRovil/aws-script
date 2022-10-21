"""
    Esse script tem como objetivo listar todos os Security Groups, filtrando somente
    os IP Permissions.
"""
from discord_webhook import DiscordWebhook
from boto3 import Session

ACCESS_KEY = ''
SECRET_KEY = ''
URL_BOT = ''
PORTS = []

session = Session(aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
webhook = DiscordWebhook(url=URL_BOT, content=f'Portas verificadas: {[port for port in PORTS]}')

client = session.client('ec2', 'us-east-1')
response = client.describe_security_groups()

with open('sec_groups.txt', 'w') as file:
    for port in PORTS:
        for sec_groups in response['SecurityGroups']:
            for ip_perm in sec_groups['IpPermissions']:
                if 'FromPort' in ip_perm.keys():
                    if ip_perm['FromPort'] == port:
                        file.write(f'{sec_groups["GroupName"]}\n')


                # Caso haja a necessidade de listar as portas TO:

                #if 'ToPort' in ip_perm.keys():
                    #if ip_perm['ToPort'] == port:
                        #file.write(f'{sec_groups["GroupName"]}\n')

# Caso haja a necessidade de listar a portas EGRESS

#with open('sec_groups_egress.txt', 'w') as file:
    #for sec_groups in response['SecurityGroups']:
        #for ip_perm in sec_groups['IpPermissionsEgress']:
            #file.write(f'{sec_groups["GroupName"]} - {sec_groups["IpPermissionsEgress"]}\n')

with open('sec_groups.txt', 'rb') as f:
    webhook.add_file(file=f.read(), filename='sec_groups.txt')

#with open('sec_groups_egress.txt', 'rb') as f:
    #webhook.add_file(file=f.read(), filename='sec_groups_egress.txt')

webhook.execute()