from flask import Flask,request,session,g,redirect,url_for,abort,\
    render_template,flash
import os
import json
import redis
from model.Service import Service
from multiprocessing import Process
#init param
app=Flask (__name__)
task_channel = 'taskBroadcast'
global r
@app.route('/request',methods=['POST'])
def taskRequest():
    requestInfo=request.json
    service=Service.objects.filter(name=requestInfo['serviceName'])[0]
    requestInfo['serviceUUID']=service.uuid
    r.publish(task_channel,requestInfo)
    return ''

@app.route('/service',methods=['POST'])
def addService():
    info=request.json
    info['serviceIP']=request.remote_addr
    print info
    service=Service()
    service.setFromjson(info)
    service.setDebugger(app.logger.debug)
    service.run()
    print service.save()
    return service.get_json()

@app.route('/')
def show_list():
    entries=db.get_entries()
    for e in entries:
        print 'title is:' +e.title+' text is:' +e.row+'/n'

#main_process
def main_process():

    pass


if __name__=='__main__':
    r=redis.Redis(host='localhost',port=6379,db=0)
    app.debug=True
    p = Process(target = main_process)
    p.start()
    app.run(port=8080)
