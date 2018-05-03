#!/usr/bin/python
# -*- coding: utf-8 -*-

from fabric.colors import *
from fabric.api import *
import re,host_status,host_to_newhost,os

etchosts = "/etc/hosts"
newhosts = "/tmp/newhosts"

def get_servers(etchosts,newhosts):
    # 每次启动master时，先将hosts文件合并成新的hosts，以供读取成服务器列表。
    host_to_newhost.add(oldfile=etchosts,
                        newfile=newhosts
                        )
    # 通过新的hosts文件，给servers赋值。
    servers = []
    for i in open(newhosts, 'r'):
        i1 = i.split("\t")[0]
        servers.append(i1)
    return servers

    # 账号，端口，密码，主机的fabric变量。

env.user = 'root'
env.port = "22"
#env.password = '123456'
env.roledefs = {
    'javaservers': get_servers(etchosts,newhosts),
}

@task()
@roles('javaservers')
def pid_info():
    print yellow("Testing server now......")
    with settings(warn_only=True):
        try:
            #赋值，ip为当前执行命令的主机的内网ip（仅通用于阿里云经典网络），i为当前cpu最高的一个进程。
            ip = run("ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|grep 10.|tr -d 'addr:'")
            i = run("ps -eo pid,pcpu,rss| tail -n +2|sort -n -k2|tail -n 1")

            pid,cpu,rss = re.split(' +|\t|\n|', i.strip())
            mem = int(rss) / 1024
            cpu = int(float(cpu))
            cpu_processor = run("cat /proc/cpuinfo|grep processor|wc -l")
            cpu = cpu / int(cpu_processor)
            pro = run("ls -l /proc/%s/exe|awk '{print $11}'" % pid)

            #判断项目是否为jar
            if "java" in pro:
                protype = "java"
                JAVA = run("which jstack")
                JAVABIN = JAVA.replace('jstack', '')
            else:
                protype = 'normal'
                JAVABIN = "null"

            #判断进程的动作。传值时带入项目类型。
            if cpu > 65:
                host_status.op(ip,'increase',pid,JAVABIN,cpu,'%sMB' % mem , protype)
            else:
                host_status.op(ip,'reduce',pid,JAVABIN,cpu,'%sMB' % mem , protype)
        except:
            pass