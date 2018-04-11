#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os,time,datetime,re,commands,mail,sys


#根据IP地址和PID，来截取项目名。
def process(IP,PID):
    tmpcmd = commands.getoutput('ssh %s ps aux|grep %s|grep -v grep' % (IP,PID))
    cmd = tmpcmd.split('.jar')[0].split('/')[-1]
    return cmd
    pass

#工作模块，先初始化报警附件文件。然后往文本中写入jar进程的占用CPU过高的   线程堆栈  GC内存情况，及heap dump文件。
def problem(IP,PID,CPU,RSS,JAVA):
    commands.getoutput("rm -f /tmp/%s.txt" % IP)
    proname = process(IP,PID)
    user = commands.getoutput("ssh %s ps aux|grep %s|grep -v grep|awk '{print $1}'" % (IP,PID))
    tid16 = commands.getoutput("ssh %s ps -mp %s -o THREAD,tid | tail -n +2 | sort -n -k2 | head -n -1 | tail -n -1|awk '{print $8}'|xargs printf %%x\\n" % (IP,PID))

    commands.getoutput("echo '####################################################################################\n' >> /tmp/%s.txt" % IP)
    commands.getoutput("echo '#########################    Thread stack information    ###########################\n' >> /tmp/%s.txt" % IP)
    commands.getoutput("echo '####################################################################################\n' >> /tmp/%s.txt" % IP)
    commands.getoutput("ssh %s@%s %sjstack %s|grep %s >> /tmp/%s.txt" % (user,IP,JAVA,PID,tid16,IP))

    commands.getoutput("echo '\n\n####################################################################################\n' >> /tmp/%s.txt" % IP)
    commands.getoutput("echo '##############################   Memory status   ###################################\n' >> /tmp/%s.txt" % IP)
    commands.getoutput("echo '####################################################################################\n' >> /tmp/%s.txt" % IP)
    commands.getoutput("ssh %s@%s %sjstat -gcutil %s 2000 10 >> /tmp/%s.txt"% (user,IP,JAVA,PID,IP))

    commands.getoutput("echo '\n\n####################################################################################\n' >> /tmp/%s.txt" % IP)
    commands.getoutput("echo '################################    Heap dump    ###################################\n' >> /tmp/%s.txt" % IP)
    commands.getoutput("echo '####################################################################################\n' >> /tmp/%s.txt" % IP)
    commands.getoutput("ssh %s@%s %sjstack -l %s >> /tmp/%s.txt" % (user,IP,JAVA,PID,IP))

    mail.mail('%s  %s is to high' % (IP,proname) , 'HOST:%s   PROJECT:%s    CPU:%s%%   MEM:%s' % (IP,proname,CPU,RSS) , '/tmp/%s.txt' % IP)

#当已经报警过的进程状态恢复正常时，则发送恢复正常的邮件。
def ok(IP,PID):
    proname = process(IP, PID)
    commands.getoutput("touch /tmp/The_project_is_ok")
    mail.mail('%s  %s is OK!!' % (IP, proname),'HOST:%s   PROJECT:%s ' % (IP, proname), '/tmp/The_project_is_ok')


#测试部分
# IP = sys.argv[1]
# PID = sys.argv[2]
# CPU = sys.argv[3]
# RSS = sys.argv[4]
# JAVA = sys.argv[5]
# problem(IP,PID,CPU,RSS,JAVA)