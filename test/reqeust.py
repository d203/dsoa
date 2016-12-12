import requests
import json
ip="http://127.0.0.1:8080/addService"
headers={'content-type':'application/json'}
data={
    'serviceName':'edge',
    'serviceIP':'127.0.0.1',
    'load':2
    }
requests.post(ip,data=json.dumps(data),headers=headers)
