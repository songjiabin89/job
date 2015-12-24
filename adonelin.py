#!/usr/bin/env python
#coding:utf-8
'''
Created on 2015年8月5日
@author: 宋家斌
'''

import MySQLdb, mail, os, time
from filemove import filemove
if __name__ == '__main__':
    dbusr = 'selectapk'
    dbhost = '114.255.157.17'
    dbpasswd = 'selectapk'
    dbport = 7710
    dbdatabae = 'adpushadmin'
    #上面是连接数据库信息。
    
    file_path = 'F:\\project\\job\\'  #指定各个文件路径,windows系统格式。
    apk_source_path = 'F:\\1111\\'
    apk_dest_path= 'F:\\2222\\'
    #file_path = './'  #指定各个文件路径,linux系统格式。
    if os.path.exists(file_path + 'sendinfo.txt'):
        os.remove(file_path + 'sendinfo.txt')
    else:
        pass
    #上面是判断上次发送的邮件内容是否存在，如果存在则删sendinfo.txt文件。
    
    
    local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) #获取系统时间，用于日志记录。
    info = '投放中'  #比对内容。
    apkinfo = 'info'
    test_file = file(file_path + 'testlist.txt')  
    del_log_file = open(file_path + 'delinfo.log','a+')
    del_log_file.write('************' + local_time + '*********\n') 
    wait_log_file = open(file_path + 'waitinfo.log','a+')
    wait_log_file.write('************' + local_time + '*********\n')
    #以上是对文件进行操作，并写入相应时间。
    while True:
        check = 0 #数据改变校验值。
        apk_list = test_file.readline().strip() #读取APK列表并去掉空格。
        if len(apk_list) == 0:break   #判断如果读取的内容是空的则退出循环。
        SQL = "SELECT a.adid '广告ID',a.app_name '广告名称',CASE a.push_status WHEN 3 THEN '投放中' WHEN 2 THEN '暂停' ELSE '下线' END '推送状态',CASE a.spot_status WHEN 3 THEN '投放中' WHEN 2 THEN '暂停' ELSE '下线' END '插屏状态',CASE a.wallstatus WHEN 3 THEN '投放中' WHEN 2 THEN '暂停' ELSE '下线' END '墙状态',CASE a.bindstatus WHEN 3 THEN '投放中' WHEN 2 THEN '暂停' ELSE '下线' END '捆绑状态',a.app_url '链接地址'FROM adpushadmin.ad a WHERE a.app_url IN ('/upload/%s')" %apk_list
        #上面是定义SQL查寻语句。
        conn=MySQLdb.connect(host=dbhost,user=dbusr,passwd=dbpasswd,db=dbdatabae,port=dbport,charset='utf8')
        #上面是连接数据库。
        cur = conn.cursor() #cursor用来执行命令的方法
        cur.execute(SQL)  #执行之前定义的SQL语句。
        numrows = int(cur.rowcount) #取之前定义语句执行后返回的行数值，并将值转成整型。
        #print numrows
        if numrows == 0:
            del_log_file.write(apk_list + '\n')
            if os.path.exists(apk_source_path + apk_list):
                ffilemove.filemove.move(apk_list,apk_source_path, apk_dest_path)
            else:
                pass
        #以上语句是判断如果取的值为0，说明这个APK包在数据库中没有记录也就是下线广告，同时将这个APK名写到delinfo.log文件内，并将APK包移走。
        else:
            for i in range(numrows):
                row = cur.fetchone()
                adid = int(row[0])
                adname = row[1].encode("utf-8")
                push = row[2].encode("utf-8")
                spot = row[3].encode("utf-8")
                wall = row[4].encode("utf-8")
                bund = row[5].encode("utf-8")
                apk = row[6].encode("utf-8")
                #print "广告ID:%s,广告名称:%s,推送状态:%s,插屏状态:%s,墙状态:%s,捆绑状态:%s,APK包名:%s" %(adid,adname,push,spot,wall,bund,apk)
                #以上语句是判断如果取值不为0，则将每个语句遍历一次，将每个字段内容取出，并将long字型转成int字型，将字符编码车成utf-8。
                if push == info or spot == info or wall == info or bund == info:
                    check =+ 1
                #将取出的值一一与info变量比对，其中有一个值与变量相等，就将check变量由0改成1，即使有多行数据只要有一行数据与info相等就会加1,方便以下代码判断。
            print check
            if check == 0:
                del_log_file.write(apk_list + '\n')
                if os.path.exists(apk_source_path + apk_list):
                    ffilemove.filemove.move(apk_list,apk_source_path, apk_dest_path)
                else:
                    pass
                    
                #以上判断check变量如果是0，说明判断的广告没有在投放，则将APK包移走，并将包名写到delinfo.log文件内做记录。
            elif check >= 1:
                select_info = "广告ID:%s,广告名称:%s,推送状态:%s,插屏状态:%s,墙状态:%s,捆绑状态:%s,APK包名:%s" %(adid,adname,push,spot,wall,bund,apk)
                change_info = '%s<br />' %select_info
                info_file = open(file_path + 'sendinfo.txt','a+')
                info_file.write(change_info + '\n')
                info_file.close()
                wait_log_file.write(apk_list + '\n')
                #以上是如果check变量由0变成1说明比对信息中有True，则装此广告所以信息取出，输入sendinfo.txt文件内，此文件为邮件发送内容。    
    conn.close()
    wait_log_file.close()
    del_log_file.close()
    #以上是关闭各文件。
    
    note = '注:此脚本正在测试当中，如发现问题及时反馈，谢谢。<br />' 
    
    if os.path.exists(file_path + 'sendinfo.txt'):
        send_file = file(file_path + 'sendinfo.txt')
        send_file_info = send_file.read()
        send_info = '<html><body> %s\n%s </body></html>' %(send_file_info,note)
        mail.sm('345278300@qq.com','病毒包处理信息',send_info)
    else:
        send_info = '没有需要处理的病毒包，谢谢。此脚本正在测试当中，如发现问题及时反馈谢谢。'
        #mail.sm('2675991587@qq.com','病毒包处理信息',send_info)
        #mail.sm('2697279171@qq.com','病毒包处理信息',send_info)
        mail.sm('345278300@qq.com','病毒包处理信息',send_info)
    #以上是判断问sendinfo.txt是不是存在，如果存在则将文件内容发送出去。
  









