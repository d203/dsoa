import requests
import tools
import requests
import json
from multiprocessing import Process,Pool
from model.Service import Service
import redis
import logging
import os
import tarfile
from contextlib import closing
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SocketServer import ThreadingMixIn
import sys



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

ip="http://127.0.0.1:8080/"
headers={'content-type':'application/json'}
global service
task_channel='taskBroadcast'
host='localhost'
jsonDict={}
worker_list={}

#
class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):pass

#add worker to run script
def add_worker(worker_name,script):
    print 'try to find '+worker_name
    if worker_name in worker_list:
        print "worker has already in the worker_list try to use it."
    else:
        print "try to add worker: "+worker_name
        worker=CodeBuilder()
        worker.set_code(script)
        worker_list[worker_name]=worker

        return "new worker has been added"

    return "finished"

#start worker with paramMap
def start_worker(worker_name,worker_id,worker_num,param_map_list,file_package):
    logging.debug(worker_name+" with id "+worker_id)
    if len(param_map_list)==1:
        p_worker_thread=Process(target=worker_thread,args=(worker_name,worker_id,worker_num,param_map_list,file_package))
        p_worker_thread.start()
        print "thread start"
    print 'param_map_list error'

def worker_thread(worker_name,worker_id,worker_num,param_map_list,file_package):
    logging.debug("now comes to worker_thread")
    pool=Pool(processes=8)
    namespace=param_map_list[0]
    worker=worker_list[worker_name]
    package_path="worker/data/"+file_package
    input_data="worker/data/"+worker_id+"/"
    output_data="worker/outdata/"+worker_id+"/"
    if not os.path.exists(package_path):
        download_package('http://127.0.0.1:8080/datacenter/',file_package)
    unpack_data(file_package,worker_id)
    os.mkdir(output_data)
    #now apply worker from file_package
    path_ls=os.listdir(input_data)
    for i in xrange(worker_num):
        pool.apply_async(do_worker(worker,worker_id,namespace,input_data+path_ls[i],output_data+path_ls[i]))
        print "Worker number: "+str(i)+"has been started"

    pack_data(worker_id)
    file_to_upload = {'file':open('worker/outdata/package/'+worker_id+'.tar.gz','r')}
    requests.post('http://127.0.0.1:8080/task/'+worker_id+'/finished',files=file_to_upload)
    pool.close()
    pool.join()



def do_worker(worker,worker_id,namespace,input_file_path,output_file_path):
    print 'do_worker now running'
    namespace['input_file_path']=input_file_path
    namespace['output_file_path']=output_file_path
    worker.run_with(namespace)
    return namespace

def download_package(url,package_name):
    print 'start donwload'
    response=requests.get(url+package_name, stream=True)
    chunk_size = 1024
    size=0;
    content_size = int(response.headers['content-length'])
    with open('worker/data/'+package_name, "wb") as file:
       for data in response.iter_content(chunk_size=chunk_size):
           file.write(data)
           size+=len(data)
           sys.stdout.write('donwloading --'+' '* 10 + '\r')
           sys.stdout.flush()
           sys.stdout.write('donwloading --'+'#'* (size*10/content_size) + '\r')
           sys.stdout.flush()
    response.close()

def unpack_data(package_name,worker_id):
    #unpack_data
    if os.path.exists('worker/data/'+package_name)==False:
        os.mkdir('worker/data/'+worker_id)
    tar=tarfile.open('worker/data/'+package_name,"r:gz")
    file_names=tar.getnames()
    for file_name in file_names:
        tar.extract(file_name,'worker/data/'+worker_id+'/')
    tar.close()

def pack_data(worker_id):
    t = tarfile.open('worker/outdata/package/'+worker_id+'.tar.gz', "w:gz")
    for root, dir, files in os.walk('worker/outdata/'+worker_id):
        print root, dir, files
        for file in files:
            fullpath = os.path.join(root, file)
            t.add(fullpath,arcname=file)

    t.close()



#CodeBuilder to run a python code
class CodeBuilder(object):
    def __init__(self,indent=0):
        self.code=[]
        self.indent_level=indent
    def add_line(self,line):
        self.code.extend([" " * self.indent_level, line, "\n"])
    INDENT_STEP = 4      # PEP8 says so!
    global_namespace={}
    def indent(self):
        """Increase the current indent for following lines."""
        self.indent_level += self.INDENT_STEP

    def dedent(self):
        """Decrease the current indent for following lines."""
        self.indent_level -= self.INDENT_STEP
    def add_section(self):
        section=CodeBuilder(self.indent_level)
        self.code.append(section)
        return section
    def set_code(self,code):
        self.code=code
    def set_namespace(self,namespace):
        self.global_namespace=namespace
    def __str__(self):
        return "".join(str(c) for c in self.code)
    def run(self):
        """Execute the code, and return a dict of globals it defines."""
        # A check that the caller really finished all the blocks they started.
        assert self.indent_level == 0
        # Get the Python source as a single string.
        python_source = str(self)
        # Execute the source, defining globals, and return them.
        global_namespace=self.global_namespace
        exec(python_source, global_namespace)
        return global_namespace
    def run_with(self,namespace):
        python_source=str(self)
        exec(python_source,namespace)
        return namespace



#init service, post information to serverNode
def init(serviceName,load=0,calcAbility=0):
    jsonDict['serviceName']=serviceName
    jsonDict['load']=0
    jsonDict['calcAbility']=0
    r=requests.post(ip+'service',data=json.dumps(jsonDict),headers=headers)
    info=r.json()
    global service
    service=Service.objects.filter(uuid=info['serviceUUID'])[0]
    print info
    logging.debug('Service Start')




# listen channel
def task_waiting():
    for item in msg.listen():
        if item['type']=='message':
            print item['data']
            jsonDict=json.loads(item['data'])
            print jsonDict['serviceUUID']
            uuid=jsonDict['taskID']
            if uuid==service.uuid:
                logging.debug('Task running')
                if jsonDict['dataPackage']!='':
                    logging.debug('Going to dowonload: '+jsonDict['dataPackage'])
                    os.mkdir('worker/data/'+uuid)
                    file=jsonDict['dataPackage']
                    r=requests.get(ip+'uploads/'+file)
                    with open("worker/data/"+uuid+"/"+file, "wb") as code:
                        code.write(r.content)
                    logging.debug('Dowonload finished')
                    if file.split('.')[-1]=='gz':
                        try:
                            tar=tarfile.open('worker/data/'+uuid+"/"+file,"r:gz")
                            file_names = tar.getnames()
                            for file_name in file_names:
                                tar.extract(file_name, 'worker/data/'+uuid+"/")
                            tar.close()
                        except Exception, e:
                            raise Exception, e



def main_process():
    r=redis.Redis(host=host,port=6379,db=0)
    global msg
    msg=r.pubsub()
    msg.subscribe(task_channel)
    server=ThreadXMLRPCServer(("0.0.0.0",8089),allow_none=True)
    server.register_function(add_worker)
    server.register_function(start_worker)
    print "Service start to istening on port 8089"
    server.serve_forever()
    p_task_waiting=Process(target=task_waiting)
    p_task_waiting.start()
    p_task_waiting.join()


if __name__=='__main__':
    set_debug()
    init('testName')
    p = Process(target = main_process)
    p.start()
    p.join()
