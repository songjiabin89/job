#!/usr/bin/env python
#coding:utf-8
'''
Created on 2015年8月12日
@author: 宋家斌
'''
import shutil

def move(filename, sourcepath, destpath):
    src = sourcepath + filename
    dest = destpath + filename
    shutil.move(src, dest)


