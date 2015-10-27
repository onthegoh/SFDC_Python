#!/usr/bin/python

#required libraries to install
#pip install requests
import requests, json, getpass, pprint, re

'''
Logging in using Connected Apps and then getting a SessionID and accessToken
Once we get the confimation back we need to store this in a cookie for future use
'''

def main():
    #username = raw_input('Enter login: ')
    #password = getpass.getpass(prompt='Enter password: ')

    username = 'USERNAME'
    password = 'PASSWORD'
    sf_url = "https://login.salesforce.com/services/oauth2/token"
    consumer_key = 'YOUR CONSUMER KEY FROM CONNECTED APP'
    consumer_secret ='YOUR CONSUMER SECRET FROM CONNECTED APP'

    payload = {
        'grant_type': 'password',
        'client_id': consumer_key,
        'client_secret': consumer_secret,
        'username': username,
        'password': password
    }

    r = requests.post(url=sf_url,
        headers={"Content-Type":"application/x-www-form-urlencoded"},
        data=payload)

    req = r.json()
    #print req
    accessToken = req['access_token']
    instanceURL = req['instance_url']
    #issuedAt = req['issued_at']
    headers={'Authorization': "Bearer " + accessToken}
#    print "Total number of custom objects: " + str(sobjectList(instanceURL,headers))
#    print limits(instanceURL,headers)
    Fields('Account',instanceURL,headers)
    Fields('Contact',instanceURL,headers)
    Fields('Opportunity',instanceURL,headers)
    Fields('Lead',instanceURL,headers)
    Fields('Campaign',instanceURL,headers)
    Fields('Case',instanceURL,headers)
    workflows(instanceURL,headers)
    limits(instanceURL,headers)



def sobjectList(instanceURL, headers):
    URL = instanceURL + "/services/data/v35.0/sobjects"
    describe = requests.get(URL,headers=headers)
    s = describe.json()
    cnt = 0 #count of custom objects
    notcnt = 0
    for i in s['sobjects']:
        if i['custom'] and re.match('.*__c\Z',i['name']):
            print i['name']
            cnt += 1
        else:
            #print i['name']
            notcnt +=1
        #print i['custom']
    #print 'Standard Objects: ' + str(notcnt)
    return cnt

def Fields(sobject,instanceURL, headers):
    URL = instanceURL + "/services/data/v35.0/sobjects/" + sobject + "/describe"
    describe = requests.get(URL,headers=headers)
    s = describe.json()
    cnt = 0 #count of fields
    rtypecnt = 0 #count record types
    lcnt = 0 #layout count
    for i in s['fields']:
        if i['custom'] and re.match('.*__c\Z',i['name']):
            #print i['name']
            cnt += 1
    for j in s['recordTypeInfos']:
        rtypecnt += 1
    layoutsURL = instanceURL + "/services/data/v35.0/sobjects/" + sobject + "/describe/layouts"
    describe = requests.get(layoutsURL,headers=headers)
    l = describe.json()
    for k in l['recordTypeMappings']:
        lcnt += 1
    print sobject + '\n\tfields: %s layouts: %s recordTypes: %s ' % (cnt, lcnt, rtypecnt)


def limits(instanceURL, headers):
    URL = instanceURL + "/services/data/v35.0/limits/"
    describe = requests.get(URL,headers=headers)
    s = describe.json()
    print "==========\nOrg Limits\n=========="
    for i in s:
        #print s[i]['Max']
        print i + "\n\t Max: %s Remaining: %s " % (str(s[i]['Max']), str(s[i]['Remaining']))
    #pprint.pprint(s,indent=4)

def workflows(instanceURL,headers):
    URL = instanceURL + "/services/data/v35.0/process/rules"
    describe = requests.get(URL,headers=headers)
    s = describe.json()
    print "===========\nWorkflows\n==========="
    for i in s['rules']:
        wfcnt = 0 #workflow counter
        print i + " workflows: "
        for j in s['rules'][i]:
            wfcnt +=1
        print wfcnt


if __name__ == '__main__':
    main()
