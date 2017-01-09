#服务节点
[TOC]
##程序目录结构
-datacenter 数据中心
-doc        文档
-model      存储的数据模型
-static     网页文件
-test       测试文件
-worker     任务的工作目录


##协议
###任务请求协议
该任务请求使用json的方式传递，主要包含以下字段
requestId 请求id，建议使用uuid
requestName 请求名，目前没啥用处
requestTime 请求时间
paramList 变量名列表
paramValue 请求变量
fileCacheId 需要使用的文件缓存id

##ServiceInformation
s
##servicePeer.py

**服务节点主程序**
##redisco
redisco
##文件分发
暂时使用vsftpd来解决，使用密码ftpd
##任务分发
通过redis的通道广播，广播一条任务请求，之后slaveNode根据广播信息给serverNode发送一条任务请求，从serverNode下载该段数据
希望使用tar打包的形式来加快文件的传输速度，服务器接收到客户端发来的数据包，在服务端解压保存，提供一个唯一的id号来标识。当有任务需求时，服务器自动分包给子节点，提供下载。
----2017 1/7 22:07----
发现之前有点sb了，其实完全可以使用rpc来代替广播通道，这样还可以更好的去发送调用请求，让子节点来相应服务器的请求，就像restful那样。
还有，文件其实没有必要用tar的方式打包，可以试试HDF5？
do it
----2017 1/7 23:02---------
测试发现soap确实还算好用
现在的问题时需要有一个codebuilder来完成构建一个python代码并且执行，来实现动态的加入新的rpc
http://aosabook.org/en/500L/a-template-engine.html 这个开源项目里面提到过给模板引擎写的python代码生成器，借鉴他写一个类似的东西应该可以用了吧。
---2017 1/7 23:28-----
目前看起来codebuilder工作很正常，并且可以通过一个namespace来传递参数给他，打算利用这种方法来执行我们的python代码。
现在惟一的问题就是数据文件了，考虑到数据一般很大，所以肯定不能直接放在
---2017 1/8 10：36----
hdf5可以解决我现在遇到的问题，可以将数据保存为hdf5的格式，然后再通过hdf5压缩，存储，分包，发放。代码想使用hdf5中的数据，只需要在传入给子节点的param_map_list里面，对应的输入‘file.\*’这样的格式就可以了
关于param_map_list我是这样计划的
param_map_list是一个map序列，里面可以选择存储一个map，或者一串map。如果只有一个map时，表示所有的文件都将按照这个参数进行处理，如果是一个list，并且该list与文件长度相同，就按照这个list分别对每个文件进行处理。
----2017 1/8 13:24----
解决了param_map_list（还没写多变量的情况），worker可以工作在进程池里面了，现在的问题就是解决hdf5文件格式
----2017 1/8 17:20----
HDF5被我抛弃了，最后还是使用传统的HTTP下载的方式来解决。
编完了下载与解压的代码，现在可以根据服务器的请求来下载数据包并且执行了，不过还没有写回调函数。
任务分分发的格式
add_worker(worker_name,script) 添加一个worker，以及他的代码
start_worker(worker_name,worker_id,worker_num,param_map_list,file_package) 执行worker ，提供执行的worker id 数量，变量列表和文件包名称
现在开始写返回函数。
---2017 1/9 20:16----
slaveNode返回函数已经可以使用，serverNode发布任务函数也写好了
接下来需要测试模块，然后配置网页
