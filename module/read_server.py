# -*- coding:utf-8 -*-
from xml.etree import ElementTree
import os
import config
from my_assert import *
import re

def make_dirpath(path):
	if not path.endswith("/"):
		path=path+"/"
	return path

gs_ip=re.compile(u'\s*?gs_ip\s*?=\s*"(.*?)"')
gs_telnet_port=re.compile(u'\s*?gs_telnet_port\s*?=\s*(\d*)')
gs_listen_port=re.compile(u'\s*?gs_listen_port\s*?=\s*(\d*)')
ls_ip_for_gs=re.compile(u'\s*?ls_ip_for_gs\s*?=\s*"(.*?)"')
ls_port_for_gs=re.compile(u'\s*?ls_port_for_gs\s*?=\s*(\d*)')
ls_ip_for_client=re.compile(u'\s*?ls_ip_for_client\s*?=\s*"(.*?)"')
ls_port_for_client=re.compile(u'\s*?ls_port_for_client\s*?=\s*(\d*)')
ls_telnet_ip=re.compile(u'\s*?ls_ip_for_telnet\s*?=\s*"(.*?)"')
ls_telnet_port=re.compile(u'\s*?ls_port_for_telnet\s*?=\s*(\d*)')
bs_ip=re.compile(u'\s*?bs_ip\s*?=\s*"(.*?)"')
bs_telnet_ip=re.compile(u'\s*?bs_telnet_ip\s*?=\s*"(.*?)"')
bs_telnet_port=re.compile(u'\s*?bs_telnet_port\s*?=\s*(\d*)')
bs_listen_port=re.compile(u'\s*?bs_listen_port\s*?=\s*(\d*)')
dba_ip=re.compile(u'\s*?dba_ip\s*?=\s*"(.*?)"')
dba_telnet_port=re.compile(u'\s*?dba_telnet_port\s*?=\s*(\d*)')
dba_listen_port=re.compile(u'\s*?dba_listen_port\s*?=\s*(\d*)')
dbu_ip=re.compile(u'\s*?dbu_ip\s*?=\s*"(.*?)"')
dbu_telnet_port=re.compile(u'\s*?dbu_telnet_port\s*?=\s*(\d*)')
dbu_listen_port=re.compile(u'\s*?dbu_listen_port\s*?=\s*(\d*)')
scs_ip=re.compile(u'\s*?scs_ip\s*?=\s*"(.*?)"')
scs_telnet_port=re.compile(u'\s*?scs_telnet_port\s*?=\s*(\d*)')
scs_listen_port=re.compile(u'\s*?scs_listen_port\s*?=\s*(\d*)')

area_id=re.compile(u'\s*?current_area_id\s*?=\s*(\d*)')

common_configip_dic={gs_ip:"gs_ip",\
                   ls_ip_for_gs:"ls_ip_for_gs",\
                   ls_ip_for_client:"ls_ip_for_client",\
                   ls_telnet_ip:"ls_telnet_ip",\
                   bs_ip:"bs_ip",\
                   bs_telnet_ip:"bs_telnet_ip",\
                   dba_ip:"dba_ip",\
                   dbu_ip:"dbu_ip",\
                   scs_ip:"scs_ip"                  
}

common_configport_dic={gs_telnet_port:"gs_telnet_port",\
                       gs_listen_port:"gs_listen_port",\
                       ls_port_for_gs:"ls_port_for_gs",\
                       ls_port_for_client:"ls_port_for_client",\
					   ls_telnet_port:"ls_telnet_port",\
                       bs_telnet_port:"bs_telnet_port",\
                       bs_listen_port:"bs_listen_port",\
                       dba_telnet_port:"dba_telnet_port",\
                       dba_listen_port:"dba_listen_port",\
                       dbu_telnet_port:"dbu_telnet_port",\
                       dbu_listen_port:"dbu_listen_port",\
                       scs_telnet_port:"scs_telnet_port",\
                       scs_listen_port:"scs_listen_port"                                                           
}

def get_serconfig():
    config_dic={}
    config_dic_list=[]
    config_path=config.SERVER_CONFIG_PATH
    paths=os.listdir(config_path)
    for i in paths:
        path=config_path+"/"+i
        if os.path.isfile(path) and path.endswith(".xml"):
            dic=read_server_xml(path)
            if config_dic.has_key(dic["area_id"]):
                return "area_id "+ str(dic["area_id"])+" has given to more than one area"
            config_dic[dic["area_id"]]=1
            config_dic_list.append(dic)
    return sorted(config_dic_list,key=lambda config:config["area_id"])

def cmp(a,b):
    if a["area_id"]>b["area_id"]:
        return 1
    elif a["area_id"]==b["area_id"]:
        return 0
    else:
        return -1

def read_server_xml(ser_xml_path):
    server_dic={}
    root = ElementTree.parse(ser_xml_path)
    server_node = root.getiterator("server")[0]
    server_dic["server_name"]=server_node.attrib["name"]

    #gss ip 
    gss_ip=server_node.find("gss_ip").text
    assert_ip(gss_ip,"gss_ip")
    server_dic["gss_ip"]=gss_ip 
    
    gss_path=server_node.find("gss_path").text
    assert_path(gss_path,"gss_path")
    server_dic["gss_path"]=gss_path 
    #gdb ip 
    gdb_ip=server_node.find("gdb_ip").text
    assert_ip(gdb_ip,"gdb_ip")
    server_dic["gdb_ip"]=gdb_ip    
    
    gdb_path=server_node.find("gdb_path").text
    assert_path(gdb_path,"gdb_path")
    server_dic["gdb_path"]=gdb_path 
    
    #gdm ip
    gdm_ip=server_node.find("gdm_ip").text
    assert_ip(gdm_ip,"gdm_ip")
    server_dic["gdm_ip"]=gdm_ip    
    
    gdm_path=server_node.find("gdm_path").text
    assert_path(gdm_path,"gdm_path")
    server_dic["gdm_path"]=gdm_path     
    #load gs
    server_dic["gs_name"]=server_node.find("gs/process_name").text
    telnet_user=server_node.find("gs/telnet_user").text
    server_dic["gs_telnet_user"]=telnet_user
    telnet_pass=server_node.find("gs/telnet_pass").text
    server_dic["gs_telnet_pass"]=telnet_pass       
    #load ls
    server_dic["ls_name"]=server_node.find("ls/process_name").text
    telnet_user=server_node.find("ls/telnet_user").text
    server_dic["ls_telnet_user"]=telnet_user
    telnet_pass=server_node.find("ls/telnet_pass").text
    server_dic["ls_telnet_pass"]=telnet_pass     
    #load bs
    server_dic["bs_name"]=server_node.find("bs/process_name").text
    telnet_user=server_node.find("bs/telnet_user").text
    server_dic["bs_telnet_user"]=telnet_user
    telnet_pass=server_node.find("bs/telnet_pass").text
    server_dic["bs_telnet_pass"]=telnet_pass
    #load dba
    server_dic["dba_name"]=server_node.find("dba/process_name").text
    telnet_user=server_node.find("dba/telnet_user").text
    server_dic["dba_telnet_user"]=telnet_user
    telnet_pass=server_node.find("dba/telnet_pass").text
    server_dic["dba_telnet_pass"]=telnet_pass    
    #load dbu
    server_dic["dbu_name"]=server_node.find("dbu/process_name").text
    telnet_user=server_node.find("dbu/telnet_user").text
    server_dic["dbu_telnet_user"]=telnet_user
    telnet_pass=server_node.find("dbu/telnet_pass").text
    server_dic["dbu_telnet_pass"]=telnet_pass
    #load scs
    server_dic["scs_name"]=server_node.find("scs/process_name").text
    telnet_user=server_node.find("scs/telnet_user").text
    server_dic["scs_telnet_user"]=telnet_user
    telnet_pass=server_node.find("scs/telnet_pass").text
    server_dic["scs_telnet_pass"]=telnet_pass
    #common_config path
    common_config_path=server_node.find("common_config").text.strip()
    if common_config_path.startswith("/"):
	assert(False)
    common_config_path=make_dirpath(common_config_path)
    server_dic["common_config"]=common_config_path

    #----------------------------------------
    common_file=open(common_config_path+"common_config.lua","r")
    str_list=common_file.readlines()
    common_file.close()
    used_regex={}
    for line in str_list:
	if parse_param(server_dic,common_configip_dic,assert_ip,line,used_regex):
	    continue
	if parse_param(server_dic,common_configport_dic,assert_str_port,line,used_regex):    
	    continue
	result=area_id.match(line)
	if result:
	    assert(result.group(1).isdigit())
	    server_dic["area_id"]=int(result.group(1))
	
    return server_dic

def parse_param(server_dic,common_config_dic,assert_func,line,used_regex):
    for regex in  common_config_dic.keys():
	if used_regex.has_key(regex):
	    continue
	result=regex.match(line)
	if result:
	    assert_func(result.group(1),common_config_dic[regex])
	    server_dic[common_config_dic[regex]]=result.group(1)
	    used_regex[regex]=1
	    return True
    return False
