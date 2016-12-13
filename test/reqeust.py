import requests
import json
ip="http://127.0.0.1:8080/request"
headers={'content-type':'application/json'}
data={
    'serviceName':'testName',
    'dataPackage':'1.jpg',
    'calcAbility':0,
    'load':2
    }
print requests.post(ip,data=json.dumps(data),headers=headers)
