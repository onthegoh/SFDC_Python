from simple_salesforce import Salesforce
import requests, pprint, json

sf = Salesforce(instance='na34.salesforce.com',session_id='00D610000007TqI!AQ8AQPo0Ivk7phzkXCozLtdN7VpVozn_NT0omPmwghsRmqeyrbd.2bh5W1CIiCnagNQxrPayol4MXk6jnOTEwoHL.aRnnciR')

#print (json.dumps(sf.Account.metadata(),indent=4))
print('*******************')
res = (json.dumps(sf.search("FIND {Jones}"),indent=4))

for x in res["type"]:
    print rest[0]

'''
for x in sf.Account.metadata()["Attributes"]:
    print x["label"]



print ("Hello World")

res = sf.search("FIND {Jones}")
print (res)

print ("************")

for x in sf.describe()["sobjects"]:
    print x["label"]
'''
