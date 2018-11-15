#! /usr/bin/env python
"""
File to export and import an infrastructure
"""
import sys
import requests

if len(sys.argv) > 1:
    inf_id = sys.argv[1]
else:
    print("Required Infrastructure ID as parameter")
    sys.exit(-1)

with open('/usr/local/ec3/auth.dat', 'r') as f:
    auth_data = f.read().replace("\n", "\\n")

headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': auth_data}

print("Getting Infra list locally")
resp = requests.request('GET', 'http://localhost:8800/infrastructures', verify=False, headers=headers)
resp.raise_for_status()
if resp.json()["uri-list"]:
    print("There are infrastructures locally. Do not import.")
    sys.exit(0)

print("Getting Infra Data from %s" % inf_id)
resp = requests.request('GET', inf_id + '/data', verify=False, headers=headers)
resp.raise_for_status()
data = resp.json()['data']

print("Putting Infra Data locally")
resp = requests.request('PUT', 'http://localhost:8800/infrastructures', verify=False, headers=headers, data=data)
resp.raise_for_status()
new_id = resp.text

print("Deleting original Infra")
resp = requests.request('GET', inf_id + '/data?delete=yes', verify=False, headers=headers)

sys.exit(2)
