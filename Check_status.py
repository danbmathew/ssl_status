import ssl
import socket
import datetime
import requests

def certificate_details(host):
    connection = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname = host)
    connection.connect((host, 443))
    certificate_details = connection.getpeercert()
    connection.close()

    return certificate_details

def get_expiry_date(host):
    ssl_details = certificate_details(host)
    expiry_date = datetime.datetime.strptime(ssl_details['notAfter'], '%b %d %H:%M:%S %Y %Z')

    return expiry_date

#Creating an SSL Context
context = ssl.create_default_context()

hosts = open('hostnames.txt')
slack_webhook = 'https://hooks.slack.com/services/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'


for each in hosts:
    host = each.rstrip()
    expiry_date = get_expiry_date(host)
    remaining_days_to_expire = (expiry_date - datetime.datetime.now()).days
    message = '* Domain : {} \n * Warning : The SSL certificate for {} will expire in {} days.'.format(host, host, remaining_days_to_expire)
    requests.post(slack_webhook, json={'text': message})
