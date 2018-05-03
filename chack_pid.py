#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os,time,datetime,re,commands,mail,sys


#根据IP地址和PID，来截取项目名。
# def process(IP,PID):
#     tmpcmd = commands.getoutput('ssh %s ps aux|grep %s|grep -v grep' % (IP,PID))
#     cmd = tmpcmd.split('.jar')[0].split('/')[-1]
#     return cmd
def process(IP,PID):
    tmpcmd = commands.getoutput("ll /proc/%s/cwd|awk '{print $11}'" % pid )
    if "root" in tmpcmd:
        tmpcmd = commands.getoutput('ssh %s ps aux|grep %s|grep -v grep' % (IP, PID))
        cmd = tmpcmd.split('.jar')[0].split('/')[-1]
    else:
        cmd = tmpcmd
    return cmd

def normalprocess(IP,PID):
    tmpcmd = commands.getoutput('ssh %s ps aux|grep %s|grep -v grep' % (IP, PID))
    cmd = re.split(' +|\t', tmpcmd.strip())
    cmd = cmd[10:]
    cmd = ' '.join(cmd)
    return cmd

#工作模块，先初始化报警附件文件。然后往文本中写入jar进程的占用CPU过高的   线程堆栈  GC内存情况，及heap dump文件。
def problem(IP,PID,CPU,RSS,JAVA):
    commands.getoutput("rm -f /tmp/%s.txt" % IP)
    proname = process(IP,PID)

    #获取进程所属用户
    user = commands.getoutput("ssh %s ps aux|grep %s|grep -v grep|awk '{print $1}'" % (IP,PID))
    if user == "root":
        pass
    else:
        user = commands.getoutput("ssh %s grep %s /etc/passwd" % (pid,user))
        user = user.split(':')[0]

    tid16 = commands.getoutput("ssh %s ps -mp %s -o THREAD,tid | tail -n +2 | sort -n -k2 | head -n -1 | tail -n -1|awk '{print $8}'|xargs printf %%x" % (IP,PID))

    commands.getoutput("echo '####################################################################################\n' >> /tmp/%s.txt" % IP)
    commands.getoutput("echo '#########################    Thread stack information    ###########################\n' >> /tmp/%s.txt" % IP)
    commands.getoutput("echo '####################################################################################\n' >> /tmp/%s.txt" % IP)
    commands.getoutput("ssh %s \"su %s -c '%sjstack %s'|grep %s\" >> /tmp/%s.txt" % (IP,user,JAVA,PID,tid16,IP))

    commands.getoutput("echo '####################################################################################\n' >> /tmp/%s.txt" % IP)
    commands.getoutput("echo '###################################    Jmap    #####################################\n' >> /tmp/%s.txt" % IP)
    commands.getoutput("echo '####################################################################################\n' >> /tmp/%s.txt" % IP)
    commands.getoutput("ssh %s \"su %s -c '%sjmap %s'|head -n20\" >> /tmp/%s.txt" % (IP,user,JAVA,PID,IP))

    commands.getoutput("echo '\n\n####################################################################################\n' >> /tmp/%s.txt" % IP)
    commands.getoutput("echo '##############################   Memory status   ###################################\n' >> /tmp/%s.txt" % IP)
    commands.getoutput("echo '####################################################################################\n' >> /tmp/%s.txt" % IP)
    commands.getoutput("ssh %s \"su %s -c '%sjstat -gcutil %s 2000 10'\" >> /tmp/%s.txt"% (IP,user,JAVA,PID,IP))

    commands.getoutput("echo '\n\n####################################################################################\n' >> /tmp/%s.txt" % IP)
    commands.getoutput("echo '################################    Heap dump    ###################################\n' >> /tmp/%s.txt" % IP)
    commands.getoutput("echo '####################################################################################\n' >> /tmp/%s.txt" % IP)
    commands.getoutput("ssh %s \"su %s -c '%sjstack -l %s'\" >> /tmp/%s.txt" % (IP,user,JAVA,PID,IP))

    mail.mail('%s  %s is to high' % (IP,proname) , 'HOST:%s   PROJECT:%s    CPU:%s%%   MEM:%s  TID:%s \n\n Please see your E-mail \n' % (IP,proname,CPU,RSS,tid16) , '/tmp/%s.txt' % IP)
    mail.postsms('%s  %s is to high,Please see your E-mail' % (IP,proname))
#当已经报警过的进程状态恢复正常时，则发送恢复正常的邮件。
def ok(IP,PID):
    proname = process(IP, PID)
    mail.postsms('%s  %s is OK!!!!' % (IP, proname))

def normalproblem(IP,PID,CPU,RSS):
    commands.getoutput("rm -f /tmp/%s.txt" % IP)
    commands.getoutput("touch /tmp/%s.txt" % IP)
    proname = normalprocess(IP,PID)
    mail.mail('%s  CPU is to high' % IP,'HOST:%s   PROJECT:%s    CPU:%s%%   MEM:%s  TID:%s \n\n Please see your E-mail \n' % (IP, proname, CPU, RSS,tid16),'/tmp/%s.txt' % IP)
    mail.postsms('%s  CPU is to high,Please see your E-mail' % (IP))


#测试部分
if __name__ == "__main__":
    IP = sys.argv[1]
    PID = sys.argv[2]
    CPU = sys.argv[3]
    RSS = sys.argv[4]
    JAVA = sys.argv[5]
    problem(IP, PID, CPU, RSS, JAVA)



