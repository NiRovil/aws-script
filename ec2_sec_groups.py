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

client = session.client('ec2', 'us-east-1')
response = client.describe_security_groups()

insecure_from_ports = []
insecure_to_ports = []
insecure_egress_ports = []

def message(title, text):
    message = DiscordWebhook(url=URL_BOT, content=f'{title}: {text}')
    return message

# Listando os ingress
for port in PORTS:
    for sec_groups in response['SecurityGroups']:
        for ip_perm in sec_groups['IpPermissions']:
            if 'FromPort' in ip_perm.keys() and ip_perm['FromPort'] == port:
                insecure_from_ports.append(sec_groups['GroupName'])

            if 'ToPort' in ip_perm.keys() and ip_perm['ToPort'] == port:
                insecure_to_ports.append(sec_groups['GroupName'])

# Listando os egress
for port in PORTS:
    for sec_groups in response['SecurityGroups']:
        for ip_perm in sec_groups['IpPermissionsEgress']:
            if 'FromPort' in ip_perm.keys() and ip_perm['FromPort'] == port:
                insecure_egress_ports.append(sec_groups['GroupName'])
            
            if 'ToPort' in ip_perm.keys() and ip_perm['ToPort'] == port:
                insecure_egress_ports.append(sec_groups['GroupName'])

# Definindo as mensagens a serem enviadas via discord webhook
if insecure_from_ports or insecure_to_ports:
    message('Portas ingress FROM verificadas', f'{[port for port in PORTS]} / GroupNames identificados: {[gname for gname in insecure_from_ports]}').execute()
    message('Portas ingress TO verificadas', f'{[port for port in PORTS]} / GroupNames identificados: {[gname for gname in insecure_to_ports]}').execute()
    
else:
    message('Portas ingress verificadas', f'{[port for port in PORTS]} / Nenhuma porta insegura identificada' ).execute()

if insecure_egress_ports:
    message('Portas egress FROM/TO verificadas', f'{[port for port in PORTS]} / GroupNames identificados {[gname for gname in insecure_egress_ports]}').execute()

else:
    message('Portas egress verificadas', f'{[port for port in PORTS]} / Nenhuma porta insegura identificada').execute()