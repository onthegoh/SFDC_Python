#!/usr/bin/python
# Import assocated libraries
import requests, json, getpass, pprint

username = raw_input('Enter login: ')
password = getpass.getpass(prompt='Enter password: ')
#username = USERNAME
#password = PASSWORD
sf_url = "https://login.salesforce.com/services/oauth2/token"
consumer_key = YOUR KEY FROM CONNECTED APP
consumer_secret = YOUR SECRET FROM CONNECTED APP

payload = {
    'grant_type': 'password',
    'client_id': consumer_key,
    'client_secret': consumer_secret,
    'username': username,
    'password': password
}

r = requests.post("https://login.salesforce.com/services/oauth2/token",
    headers={"Content-Type":"application/x-www-form-urlencoded"},
    data=payload)

req = r.json()
accessToken = req['access_token']
instanceURL = req['instance_url']
issuedAt = req['issued_at']

print req

print accessToken
print instanceURL
print issuedAt

def sobjectList(accessToken,instanceURL):
    headers={'Authorization': "Bearer " + accessToken}
    URL = instanceURL + "/services/data/v35.0/sobjects"
    describe = requests.get(URL,headers=headers)
    s = describe.json()
    #print sobj[0]
    #pprint.pprint(sobj['sobjects'],indent=4)
    #print s['sobjects']['name']

    for i in s['sobjects']:
        print i['name']
        print i['custom']

        print '=================='





sobjectList(accessToken,instanceURL)
