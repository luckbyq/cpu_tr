#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys,os,chack_pid,mail,commands

file="/tmp/host_status"


#测试输入的语法是否符合。
try:
    who = sys.argv[1]
    do = sys.argv[2]
    pid = sys.argv[3]
    cpu = sys.argv[4]
    mem = sys.argv[5]

except:
    print "please enter python xxxx.py <who> <do>"

#自动初始化新的host。先判断格式化后的hosts文件和状态列表。如果行数不同，则将状态表中没有的主机加入其中，并初始化该行。
def init_statuslist(newhosts):
    os.system("touch %s" % file)
    hosts = int(commands.getoutput("wc -l %s|awk '{print $1}'" % newhosts))
    statuslist = int(commands.getoutput("wc -l %s|awk '{print $1}'" % file))
    if hosts != statuslist:
        s = hosts - statuslist
        print "have %s new server! auto add it......" % s
        for host in open(newhosts,'r'):
            ip = host.split("\t")[0]
            n = 0
            for status in open(file,'r'):
                stat = status.split("_")[0]
                if ip == stat:
                    n += 1
            if n == 0:
                os.system("echo \"%s\" >> %s" % (ip,file))
                reset(ip)

#用来将文本中的所有主机加载到内存中。
def chk():
    l=[]
    f=open(file,'r')
    for i in f.readlines():
        i=i.replace('\n','')
        l.append(i)
        print l
    f.close()

#初始化模块
def reset(i1):
    os.system('sed -i "s/%s.*/%s_0_0_0_0/g" %s' % (i1,i1,file))

#状态码自增长模块
def inc(i1,i2,pid,cpu,mem):
    i2 += 1
    os.system('sed -i "s/%s.*/%s_%s_%s_%s_%s/g" %s' % (i1,i1,i2,pid,cpu,mem,file))
    return i2

#工作模块，带入主机和增加或减少操作。
def op(who,do,pid,JAVA,cpu,mem,protype):
    l=[]
    f=open(file,'r')
    for i in f.readlines():
        #测试i1  i2是否赋值成功
        try:
            i1, i2, PID = i.split('_')[0], int(i.split('_')[1]), i.split('_')[2]
            if who == i1:
                #如果do为增加
                if do == "increase":
                    #如果是同一个进程，则直接累加。
                    if pid == PID:
                        inc(i1, i2, pid, cpu, mem)
                    #如果是不同进程，则重置状态后累加。
                    elif pid != PID:
                        reset(i1)
                        i2 = 0
                        inc(i1, i2, pid, cpu, mem)
                #如果do为减少,并且i2大于5，代表CPU高于警戒值的进程已经恢复，则将对应主机后面的数字变为0，并发送通知进程恢复。
                if (do == "reduce") and (i2 > 5):
                    reset(i1)
                    #发送进程恢复的通知。
                    chack_pid.ok(who,PID)
                #如果do为减少，则将主机后面对应的数字恢复为0.
                elif (do == "reduce") and (5 >i2 > 0):
                    reset(i1)
                else:
                    pass
                #记录某进程CPU高于警戒值超过6次，则产生报警信息。
                if i2 == 6:
                    if protype == "java":
                        chack_pid.problem(who, pid, cpu, mem, JAVA)
                    elif protype == "normal":
                        chack_pid.normalproblem(who,pid,cpu,mem)
        except:
            pass
    f.close()
