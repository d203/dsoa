from flask import Flask,request,session,g,redirect,url_for,abort,\
    render_template,flash
import os
import json
import redis
import uuid as UUID
from model.Service import Service
from multiprocessing import Process
from flask import send_from_directory
#init param
app=Flask (__name__)
task_channel = 'taskBroadcast'
global r

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

#上传数据包到datacenter
@app.route('/data/package/<filename>', methods=[ 'POST'])
def upload_package_to_datacenter(filename):
    file = request.files['file']
    if file:
        file.save(os.path.join('datacenter/data/package', filename))
        return 'upload done'
    return 'upload fail'


# @app.route('/uploads/<filename>',methods=['GET'])
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)

@app.route('/request',methods=['POST'])
def task_request():
    requestInfo=request.json
    service=Service.objects.filter(name=requestInfo['serviceName'])[-1]
    requestInfo['serviceUUID']=service.uuid
    requestInfo['taskID']=str(UUID.uuid1())
    if requestInfo['data_package']:

    r.publish(task_channel,json.dumps(requestInfo))
    return ''

@app.route('/service',methods=['POST'])
def add_service():
    info=request.json
    info['serviceIP']=request.remote_addr
    print info
    service=Service()
    service.setFromjson(info)
    service.setDebugger(app.logger.debug)
    service.run()
    print service.save()
    return service.get_json()



#main_process
def main_process():

    pass


if __name__=='__main__':
    r=redis.Redis(host='localhost',port=6379,db=0)
    app.debug=True
    p = Process(target = main_process)
    p.start()
    app.run(port=8080)
