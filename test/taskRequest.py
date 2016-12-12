import requests
import json
ip="http://127.0.0.1:8080/request"
headers={'content-type':'application/json'}
data={}
    'serviceName':'testName',
    'from':'this will be an uuid',
    'param':'a,b,c,d'

    }
print requests.post(ip,data=json.dumps(data),headers=headers)
