import requests
import tools
import requests
import json
from multiprocessing import Process
from model.Service import Service
import redis
import logging

#init param
def set_debug():
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='slaveNode.log',
                    filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

ip="http://127.0.0.1:8080/service"
headers={'content-type':'application/json'}
global service
task_channel='taskBroadcast'
host='localhost'
jsonDict={}

def init(serviceName,load=0,calcAbility=0):
    jsonDict['serviceName']=serviceName
    jsonDict['load']=0
    jsonDict['calcAbility']=0
    r=requests.post(ip,data=json.dumps(jsonDict),headers=headers)
    info=r.json()
    service=Service.objects.filter(uuid=info['serviceUUID'])[0]
    print info
    logging.debug('Service Start')



def task_waiting():
    for item in msg.listen():
        if item['type']=='message':
            print item['data']
            jsonDict=json.loads(item['data'],encoding='unicode')
            print jsonDict['serviceUUID']
            if jsonDict['serviceUUID']==service.uuid:
                print jsonDict


def main_process():
    r=redis.Redis(host=host,port=6379,db=0)
    global msg
    msg=r.pubsub()
    msg.subscribe(task_channel)
    p_task_waiting=Process(target=task_waiting)
    p_task_waiting.start()
    p_task_waiting.join()

if __name__=='__main__':
    set_debug()
    init('testName')
    p = Process(target = main_process)
    p.start()
    p.join()
