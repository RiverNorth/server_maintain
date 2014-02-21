# -*- coding:utf-8 -*-
from xml.etree import ElementTree
import os
import config
import sys
from my_assert import *

def get_remoteconfig():
    config_file=config.REMOTE_CONFIG_FILE
    return read_remote_xml(config_file)

def read_remote_xml(path):
    remote_dics={}
    root = ElementTree.parse(path)
    remote_nodes = root.getiterator("remote_server")
    for node in remote_nodes:
        remote_dic={}
        ip=node.find("ip_addr").text
        assert_ip(ip,"ip_addr")
        remote_dic["ip_addr"]=ip
                              
        tmp_path=node.find("tmp_path").text
        assert_path(tmp_path,"tmp_path")
        remote_dic["tmp_path"]=tmp_path
        
        backup_des_path=node.find("backup_des_path").text
        assert_path(backup_des_path,"backup_des_path")
        remote_dic["backup_des_path"]=backup_des_path        
        
        port=int(node.find("ssh_port").text)
        assert_port(port,"ssh_port")
        remote_dic["ssh_port"]=port
        
        user=node.find("ssh_user").text
        remote_dic["ssh_user"]=user 
        
        password=node.find("ssh_password").text
        remote_dic["ssh_password"]=password        
        
        
        port=int(node.find("sftp_port").text)
        assert_port(port,"sftp_port")
        remote_dic["sftp_port"]=port
        
        user=node.find("sftp_user").text
        remote_dic["sftp_user"]=user 
        
        password=node.find("sftp_password").text
        remote_dic["sftp_password"]=password 
        
        if remote_dics.has_key(remote_dic["ip_addr"]):
            print "this remote server ip "+remote_dic["ip_addr"]+" configed twice"
            sys.exit(-1)
        remote_dics[remote_dic["ip_addr"]]=remote_dic
    return remote_dics

