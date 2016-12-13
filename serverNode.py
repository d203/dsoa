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
app.config['UPLOAD_FOLDER'] = 'static/data/'
global r

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="/upload" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>',methods=['GET'])
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/request',methods=['POST'])
def taskRequest():
    requestInfo=request.json
    service=Service.objects.filter(name=requestInfo['serviceName'])[-1]
    requestInfo['serviceUUID']=service.uuid
    requestInfo['taskID']=str(UUID.uuid1())
    r.publish(task_channel,json.dumps(requestInfo))
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
