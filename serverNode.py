from flask import Flask,request,session,g,redirect,url_for,abort,\
    render_template,flash,jsonify
import os
import json
import redis
import uuid as UUID
from model.Service import Service
from multiprocessing import Process
from flask import send_from_directory
import model.datacenter as datacenter
from model.user import User
from model.workertask import WorkerTask
import tarfile
import xmlrpclib
#init param
app=Flask (__name__)
task_channel = 'taskBroadcast'
global r

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        print 'a post'
        u=request.form['username']
        p=request.form['password']
        user=User.objects.filter(username=u,password=p)
        print u
        print p
        if len(user)==0:
            return '0'
        else:
            user=user[0]
            session['username']=user.username
            print 'login success'
            return '1'
    else:
        return render_template('login.html')

@app.route('/logout',methods=['GET'])
def logout():
    session['username']=''
    return redirect('/login')

@app.route('/',methods=['GET'])
def index():
    try:
        if session['username']:
            return render_template('AdminLTE-2.3.7/index.html')
    except:
        return redirect('/login')
@app.route('/manage_worker',methods=['GET'])
def start_worker():
    return render_template('AdminLTE-2.3.7/manage_worker.html')

@app.route('/upload_files')
def upload_files():
    return render_template('AdminLTE-2.3.7/upload_files.html')

@app.route('/upload_codes')
def upload_codes():
    return render_template('AdminLTE-2.3.7/upload_codes.html')

@app.route('/status',methods=['GET'])
def status():
    return 'ture'

@app.route('/asyn')
def wait():
    for i in range(1,100000000):
        pass
    return 'finish'

#------------------------------------------------------------------------------
#Author : Meng Qingyu
#Changer : Wang Bingyi
#Data : 170108
#Description : if post filename,then rename the filename ,else reserve it's
#original name
#------------------------------------------------------------------------------

@app.route('/data/package/<filename>', methods=[ 'POST'])
def upload_package_to_datacenter(filename):
    file = request.files['file']
    if file:
        package=datacenter.DataPackage()
        if len(request.form['filename']) > 0:
            package.package_name=request.form['filename']
            file.save(os.path.join('datacenter/data/package', request.form['filename']))
        else:
            file.save(os.path.join('datacenter/data/package', file.filename))
            package.package_name=file.filename
        package.save()
        return 'upload done'
    return 'upload fail'
#------------------------------------------------------------------------------
#Author : Wang Bingyi
#Data : 170108
#Description : Controller ,upload codes
#------------------------------------------------------------------------------

@app.route('/data/service', methods=[ 'POST'])
def upload_package_to_datacenter_code():
    if len(request.form['filename']) > 0:
        file_object = open('datacenter/service/'+request.form['filename'], 'w')
        file_object.write(request.form['codes'])
        file_object.close()
        worker_script=datacenter.WorkerScript()
        worker_script.script_name=request.form['filename']
        worker_script.save()
        return 'Upload code OK!'
    return 'Plead input filename'
#------------------------------------------------------------------------------
#Author : Wang Bingyi
#Data : 170108
#Description : Use redirect method to static files . But now ,we don't want to
# use it ,so you can delete it! :)
#------------------------------------------------------------------------------

@app.route('/data/package/list',methods=['GET'])
def get_package_list():
    l=[]
    packages=datacenter.DataPackage.objects.all()
    for package in packages:
        l.append(package.get_json())
    return jsonify(l)


@app.route('/data/script/list',methods=['GET'])
def get_script_list():
    l=[]
    scripts=datacenter.WorkerScript.objects.all()
    for script in scripts:
        l.append(script.get_json())
    return jsonify(l)





@app.route('/datacenter/<filename>',methods=['GET'])
def get_data_package(filename):
    return send_from_directory('datacenter/data/package/',
                               filename)


@app.route('/request',methods=['POST'])
def task_request():
    requestInfo=request.json
    service=Service.objects.filter(name=requestInfo['serviceName'])[-1]

    requestInfo['serviceUUID']=service.uuid
    requestInfo['taskID']=str(UUID.uuid1())
    if requestInfo['data_package']:
        r.publish(task_channel,json.dumps(requestInfo))
    return ''



@app.route('/data/service',methods=['GET'])
def get_data_service():
    pass

@app.route('/task',methods=['POST'])
def start_task():
    print 'a new task'
    print request
    info=request.json
    print info
    service=dispatch_task(info['worker_name'])
    task_server =  xmlrpclib.ServerProxy("http://127.0.0.1:8089")
    file_object = open('datacenter/service/'+info['script_code'], 'r')
    script=file_object.read()
    file_object.close( )
    task_server.add_worker(info['worker_name'],script)
    uuid=str(UUID.uuid1())
    t=WorkerTask()
    t.task_id=uuid
    t.worker_name=info['worker_name']
    t.script_code=info['script_code']
    t.status='running'
    t.file_package=info['file_package']
    t.save()
    task_server.start_worker(info['worker_name'],uuid,info['worker_num'],[{"":""}],info['file_package'])
    return 'OK'

@app.route('/task/<task_id>/finished',methods=['POST'])
def finish_task(task_id):
    print task_id+' has been finished'
    t=WorkerTask.objects.filter(task_id=task_id)
    t.status='done'
    print t[0].save()
    file = request.files['file']
    print 'try to save file '+file.filename
    if file:
        file.save(os.path.join('datacenter/data/output', file.filename))
        unpack_output_data(file.filename)
        return 'upload done'
    return 'upload fail'


def dispatch_task(worker_name):
    service=Service.objects.all()[0]
    return service

@app.route('/task/list',methods=['GET'])
def get_task_list():
    l=[]
    tasks=WorkerTask.objects.all()
    for task in tasks:
        l.append(task.get_json())
    return jsonify(l)

@app.route("/task/<task_id>",methods=['GET'])
def get_output_page(task_id):
    if not session['username']:
        return redirect('/login')
    else:
        return render_template('task_output_page.html',task_id=task_id)

@app.route('/task/<task_id>/output/list',methods=['GET'])
def get_output_list(task_id):
    l=[]
    for root,dir,files in os.walk('datacenter/data/output/'+task_id):
        for file in files:
            l.append(file)
    return jsonify(l)

@app.route('/task/<task_id>/info')
def get_task_info(task_id):
    task=WorkerTask.objects.filter(task_id=task_id)[0]
    return task.get_json()

@app.route('/task/<task_id>/output/<file_name>',methods=['GET'])
def get_output_file(task_id,file_name):
    return send_from_directory('datacenter/data/output/'+task_id+'/',file_name)

#divided data_package for distribute
def unpack_output_data(package_name):
    #unpack_data
    print package_name
    tar=tarfile.open('datacenter/data/output/'+package_name,"r:gz")
    file_names=tar.getnames()
    for file_name in file_names:
        tar.extract(file_name,'datacenter/data/output/'+package_name[:-7]+'/')
    tar.close()






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
    app.secret_key='dsoa_key'
    p = Process(target = main_process)
    p.start()
    app.run(port=8080)
