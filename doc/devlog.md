#服务节点
[TOC]
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
通过redis的通道广播，广播一条任务请求，之后slaveNode根据广播信息给serverNode发送一条任务请求，
