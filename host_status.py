#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys,os,chack_pid

file="/tmp/host_status"

#测试输入的语法是否符合。
try:
    who = sys.argv[1]
    do = sys.argv[2]
    pid = sys.argv[3]
    cpu = sys.argv[4]
    rss = sys.argv[5]

except:
    print "please enter python xxxx.py <who> <do>"

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
    os.system('sed -i "s/%s.*/%s_0_0_0_0" %s' % (i1,i1,file))

#状态码自增长模块
def inc(i1,i2,pid,cpu,rss):
    i2 += 1
    os.system('sed -i "s/%s.*/%s_%s_%s_%s_%s" %s' % (i1,i1,i2,pid,cpu,rss,file))

#工作模块，带入主机和增加或减少操作。
def op(who,do,pid,JAVA,cpu,mem):
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
                        inc(i1, i2, pid, cpu, rss)
                    #如果是不同进程，则重置状态后累加。
                    elif pid != PID:
                        reset(i1)
                        inc(i1, i2, pid, cpu, rss)
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
                if i3 == 6:
                    chack_pid.problem(who,pid,cpu,mem,JAVA)
        except:
            pass
    f.close()
