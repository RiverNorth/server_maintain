# -*- coding:utf-8 -*-
import socket
def assert_path(path,error_str):
    assert valid_path(path)
        
def valid_path(path):
    if not path.startswith("/"):
        return False
    return True
    
def assert_port(port,error_str):
    assert port >0 and port <65535

def assert_str_port(port,error_str):
    assert int(port)

def assert_ip(ip_str,error_str):
    assert valid_ip(ip_str) or valid_domain(ip_str)

def valid_domain(ip_str):
    try:
        socket.getaddrinfo(ip_str, None)
        return True
    except Exception,e:
        print e.message
        return False


def valid_ip(ip_str):
    ip_list=ip_str.split(".")
    if len(ip_list)!=4:
        return False
    #check each split value
    for i in ip_list:
        num=int(i)
        if num<0 or num>=255:
            return False
    #last split value must not be zero
    if int(ip_list[3])==0:
        return False
    return True
