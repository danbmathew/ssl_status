#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ssl
import socket
import datetime
import requests
import argparse

def certificate_details(host):
    context = ssl.create_default_context()
    connection = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname = host)
    connection.connect((host, 443))
    certificate_details = connection.getpeercert()
    connection.close()

    return certificate_details

def get_expiry_date(host):
    ssl_details = certificate_details(host)
    expiry_date = datetime.datetime.strptime(ssl_details['notAfter'], '%b %d %H:%M:%S %Y %Z')

    return expiry_date



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    arg = parser.parse_args()
    expiry_date = get_expiry_date(arg.host)
    remaining_days_to_expire = (expiry_date - datetime.datetime.now()).days
    return 5

main()
