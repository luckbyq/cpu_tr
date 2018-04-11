#!/usr/bin/python
# -*- coding: utf-8 -*-

from fabric.colors import *
from fabric.api import *
import re
import host_status

#账号，端口，密码，主机的fabric变量。
env.user='root'
env.port="22"
env.password='123456'
env.roledefs = {
        'javaservers':['192.168.0.222',]
}

@roles('javaservers')
def pid_info():
    print yellow("Testing server now......")
    with settings(warn_only=True):
        try:
            #赋值，ip为当前执行命令的主机的内网ip（仅通用于阿里云经典网络），i为当前cpu最高的一个进程。
            ip = run("ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|grep 10.|tr -d 'addr:'")
            i = run("ps -eo pid,pcpu,rss| tail -n +2|sort -n -k2|tail -n 1")
            JAVA = run ("which jstack")
            JAVABIN = JAVA.replace('jstack','')
            pid,cpu,rss = re.split(' +|\t|\n|', i.strip())
            mem = int(rss) / 1024
            cpu = int(float(cpu))
            pro = run("ps aux|grep %s|grep -v grep|grep -v agent|grep .jar|grep java")
            if len(pro) > 20:
                protype = "jar"
            if protype == 'jar':
                if cpu > 60:
                    host_status.op(ip,'increase',pid,JAVABIN,cpu,'%sMB' % mem)
                else:
                    host_status.op(ip,'reduce',pid,JAVABIN,cpu,'%sMB' % mem)
        except:
            pass