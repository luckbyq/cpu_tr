#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys,os,re,time,datetime,commands,host_status

#用来备份当前的hosts文件。
# nowday = datetime.datetime.now().strftime('%Y-%m-%d')
# nowTime = datetime.datetime.now().strftime('%H:%M:%S')
# os.system('mkdir -p /backup/hosts/%s' % nowday)
# os.system('cp /etc/hosts /backup/hosts/%s/hosts_%s' % (nowday,nowTime))

#清空列表中的空字符模块。
def sp(l):
    if '' in l:
        for i in range(l.count('')):
            l.remove('')

#主工作模块。
def add(oldfile,newfile):
    print "Being merged......"
    #睡眠1秒，保证hosts文件备份不会被覆盖。
    time.sleep(1)
    #初始化新的hosts文件
    tmpfile = "/tmp/oldhosts"
    os.system("cp %s %s" % (oldfile,tmpfile))
    os.system("sed -i '/^ *$/d' %s" % tmpfile)
    os.system("touch %s" % newfile)
    # chack_newfile_bit = int(commands.getoutput("ls -l %s |awk '{print $5}'" % newfile))
    # if chack_newfile_bit == 0:
    #     print "newfile"
    #     os.system("echo '127.0.0.1\tlocalhost' > %s" % newfile)
    #遍历老文件，查看新文件。如果新文件不存在则写入，如果存在则追加。
    for i in open(tmpfile,'r').readlines():
        if ("127.0.0.1" in i) or ("10.47.48.37" in i):
            pass
        else:
            l = []
            l = re.split(' +|\t|\n|', i.strip())
            sp(l)
            ip = l[0]
            new = open(newfile, 'a+')
            #设置新行写入开关，默认为开。进入检察重复行后，如果循环遍历无重复行，则开关为开。
            write = 0
            #载入新的文件，开始查看重复行
            for I in new.readlines():
                #如果IP地址有相同，将新行写入开关关闭。
                if ip in I:
                    write += 1
                    #初始化新文件的行信息。
                    L = []
                    L = re.split(' +|\t|\n|', I.strip())
                    #切除原始文件的IP重复行的IP部分。
                    l.remove(ip)
                    #根据新行切除IP后剩余的值的个数做遍历循环。
                    for key in range(len(l)):
                        #格式化新文件的行数据。
                        sp(L)
                        #如果原始的行中的值已经存在于新的行中的值，则忽略。否则将原始的这个值添加到新的list中末尾。
                        if l[key] in L:
                            pass
                        else:
                            L.append(l[key])
                    #已经遍历完毕，将内存中的新行list转换成str
                    L = '\t'.join(L)
                    #将内存中新的行，替换掉新文件中的同一行。
                    os.system("sed -i 's/%s.*/%s/g' %s" % (ip, L, newfile))
            #如果没有IP地址相同，此时的开关应是默认的开启状态。那么就将原始文件中的这一行数据写入新文件。
            if write == 0:
                new = open(newfile, 'a+')
                new.writelines('\t'.join(l)+'\n')
                new.close()
    print "Merged success!!"
    host_status.init_statuslist(newhosts=newfile)

if __name__ == "__main__":
    import host_status
    # 判断传值是否存在。
    try:
        oldfile = sys.argv[1]
        newfile = sys.argv[2]
    except:
        print "cmd is   python  xxxx.py <oldfile path> <newfile path>"
        exit(1)
    add(oldfile, newfile)
    host_status.init_statuslist(newhosts=newfile)