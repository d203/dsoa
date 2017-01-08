from flask import Flask,request,session,g,redirect,url_for,abort,\
    render_template,flash
import os
import json
import redis
import uuid as UUID
from model.Service import Service
from multiprocessing import Process
from flask import send_from_directory
import tarfile

#init param
app=Flask (__name__)
task_channel = 'taskBroadcast'
global r

@app.route('/',methods=['GET'])
def index():
    return render_template('AdminLTE-2.3.7/index.html')

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
        if len(request.form['filename']) > 0:
            file.save(os.path.join('datacenter/data/package', request.form['filename']))
        file.save(os.path.join('datacenter/data/package', file.filename))
        return 'upload done'
    return 'upload fail'
#------------------------------------------------------------------------------
#Author : Wang Bingyi
#Data : 170108
#Description : Controller ,upload codes
#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
#Author : Wang Bingyi
#Data : 170108
#Description : Use redirect method to static files . But now ,we don't want to
# use it ,so you can delete it! :)
#------------------------------------------------------------------------------



@app.route('/bootstrap/<s_path>')
def static_path_bootstrap(s_path):
    return redirect("/static/bootstrap/"+s_path)

@app.route('/img/<s_path>')
def static_path_img(s_path):
    return redirect("/static/img/"+s_path)

@app.route('/build/<s_path>')
def static_path_build(s_path):
    return redirect("/static/build/"+s_path)

@app.route('/dist/img/<s_path>')
def static_path_dist(s_path):
    return redirect("/static/dist/img/"+s_path)

@app.route('/documentation/<s_path>')
def static_path_documentation(s_path):
    return redirect("/static/documentation/"+s_path)

@app.route('/pages/<s_path>')
def static_path_pages(s_path):
    return redirect("/static/pages/"+s_path)

@app.route('/plugins/<s_path>')
def static_path_plugins(s_path):
    return redirect("/static/plugins/"+s_path)

#---------------------------------End------------------------------------------

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

#divided data_package for distribute
def unpack_data(package_name):
    #unpack_data
    if os.path.exists('datacenter/data/package/'+package_name)==False:
        os.mkdir('datacenter/data/package/'+package_name)
    tar=tarfile.open('datacenter/data/package/'+package_name+'.tar.gz',"r:gz")
    file_names=tar.getnames()
    for file_name in file_names:
        tar.extract(file_name,'datacenter/data/package/'+package_name+'/')
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

    p = Process(target = main_process)
    p.start()
    app.run(port=8080)
