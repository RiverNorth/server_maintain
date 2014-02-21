from xml.etree import ElementTree
import os
import config
from my_assert import *

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

    #share ip 
    share_ip=server_node.find("share_ip").text
    assert_ip(share_ip,"share_ip")
    server_dic["share_ip"]=share_ip
    
    share_path=server_node.find("share_path").text
    assert_path(share_path,"share_path")
    server_dic["share_path"]=share_path
    
    remote_path=server_node.find("remote_path").text
    assert_path(remote_path,"remote_path")
    server_dic["remote_path"]=remote_path 
    
    #share ip 
    gdb_ip=server_node.find("gdb_ip").text
    assert_ip(gdb_ip,"gdb_ip")
    server_dic["gdb_ip"]=gdb_ip    
    
    gdb_path=server_node.find("gdb_path").text
    assert_path(gdb_path,"gdb_path")
    server_dic["gdb_path"]=gdb_path 
    
    area_id=int(server_node.find("area_id").text)
    server_dic["area_id"]=area_id
    
    pf_type=int(server_node.find("pf_type").text)
    server_dic["pf_type"]=pf_type    
    
    #load gs
    server_dic["gs_name"]=server_node.find("gs/process_name").text
	
    gs_ip=server_node.find("gs/ip_addr").text
    assert_ip(gs_ip,"gs_ip")
    server_dic["gs_ip"]=gs_ip
    
    port=int(server_node.find("gs/telnet_port").text)
    assert_port(port,"gs/telnet_port")
    server_dic["gs_telnet_port"]=port
    
    port=int(server_node.find("gs/listen_port").text)
    assert_port(port,"gs/listen_port")    
    server_dic["gs_listen_port"]=port
    
    telnet_user=server_node.find("gs/telnet_user").text
    server_dic["gs_telnet_user"]=telnet_user
    
    telnet_pass=server_node.find("gs/telnet_pass").text
    server_dic["gs_telnet_pass"]=telnet_pass    
    
	#load ls
    server_dic["ls_name"]=server_node.find("ls/process_name").text

    ls_ip_for_gs=server_node.find("ls/ip_for_gs").text
    assert_ip(ls_ip_for_gs,"ls_ip_for_gs")
    server_dic["ls_ip_for_gs"]=ls_ip_for_gs		

    port=int(server_node.find("ls/port_for_gs").text)
    assert_port(port,"ls/port_for_gs")    
    server_dic["ls_port_for_gs"]=port  
	
    ls_ip_for_client=server_node.find("ls/ip_for_client").text
    assert_ip(ls_ip_for_client,"ls_ip_for_client")
    server_dic["ls_ip_for_client"]=ls_ip_for_client	

    port=int(server_node.find("ls/port_for_client").text)
    assert_port(port,"ls/port_for_client")    
    server_dic["ls_port_for_client"]=port 	
	
    ls_telnet_ip=server_node.find("ls/telnet_ip").text
    assert_ip(ls_telnet_ip,"ls_telnet_ip")
    server_dic["ls_telnet_ip"]=ls_telnet_ip
	
    port=int(server_node.find("ls/telnet_port").text)
    assert_port(port,"ls/telnet_port")
    server_dic["ls_telnet_port"]=port
     
    telnet_user=server_node.find("ls/telnet_user").text
    server_dic["ls_telnet_user"]=telnet_user
    
    telnet_pass=server_node.find("ls/telnet_pass").text
    server_dic["ls_telnet_pass"]=telnet_pass  
    
	#load bs
    server_dic["bs_name"]=server_node.find("bs/process_name").text

    bs_ip=server_node.find("bs/ip_addr").text
    assert_ip(bs_ip,"bs_ip")
    server_dic["bs_ip"]=bs_ip	
  
    bs_telnet_ip=server_node.find("bs/telnet_ip").text
    assert_ip(bs_telnet_ip,"bs_telnet_ip")
    server_dic["bs_telnet_ip"]=bs_telnet_ip
  
    port=int(server_node.find("bs/telnet_port").text)
    assert_port(port,"bs/telnet_port")
    server_dic["bs_telnet_port"]=port
    
    port=int(server_node.find("bs/listen_port").text)
    assert_port(port,"bs/listen_port")    
    server_dic["bs_listen_port"]=port   
    
    telnet_user=server_node.find("bs/telnet_user").text
    server_dic["bs_telnet_user"]=telnet_user
    
    telnet_pass=server_node.find("bs/telnet_pass").text
    server_dic["bs_telnet_pass"]=telnet_pass       

	#load dba
    server_dic["dba_name"]=server_node.find("dba/process_name").text

    dba_ip=server_node.find("dba/ip_addr").text
    assert_ip(dba_ip,"dba_ip")
    server_dic["dba_ip"]=dba_ip	
  
    port=int(server_node.find("dba/telnet_port").text)
    assert_port(port,"dba/telnet_port")
    server_dic["dba_telnet_port"]=port
    
    port=int(server_node.find("dba/listen_port").text)
    assert_port(port,"dba/listen_port")    
    server_dic["dba_listen_port"]=port  
    
    telnet_user=server_node.find("dba/telnet_user").text
    server_dic["dba_telnet_user"]=telnet_user
    
    telnet_pass=server_node.find("dba/telnet_pass").text
    server_dic["dba_telnet_pass"]=telnet_pass     
	
	#load dbu
    server_dic["dbu_name"]=server_node.find("dbu/process_name").text

    dbu_ip=server_node.find("dbu/ip_addr").text
    assert_ip(dbu_ip,"dbu_ip")
    server_dic["dbu_ip"]=dbu_ip	
  
    port=int(server_node.find("dbu/telnet_port").text)
    assert_port(port,"dbu/telnet_port")
    server_dic["dbu_telnet_port"]=port
    
    port=int(server_node.find("dbu/listen_port").text)
    assert_port(port,"dbu/listen_port")    
    server_dic["dbu_listen_port"]=port  
    
    telnet_user=server_node.find("dbu/telnet_user").text
    server_dic["dbu_telnet_user"]=telnet_user
    
    telnet_pass=server_node.find("dbu/telnet_pass").text
    server_dic["dbu_telnet_pass"]=telnet_pass       
	
	#load scs
    server_dic["scs_name"]=server_node.find("scs/process_name").text

    scs_ip=server_node.find("scs/ip_addr").text
    assert_ip(scs_ip,"scs_ip")
    server_dic["scs_ip"]=scs_ip	
  
    port=int(server_node.find("scs/telnet_port").text)
    assert_port(port,"scs/telnet_port")
    server_dic["scs_telnet_port"]=port
    
    port=int(server_node.find("scs/listen_port").text)
    assert_port(port,"scs/listen_port")    
    server_dic["scs_listen_port"]=port 
    
    telnet_user=server_node.find("scs/telnet_user").text
    server_dic["scs_telnet_user"]=telnet_user
    
    telnet_pass=server_node.find("scs/telnet_pass").text
    server_dic["scs_telnet_pass"]=telnet_pass      
	
	#load http
    http_ip=server_node.find("http/ip_addr").text
    assert_ip(http_ip,"http_ip")
    server_dic["http_ip"]=http_ip	
  
    port=int(server_node.find("http/listen_port").text)
    assert_port(port,"http/listen_port")    
    server_dic["http_listen_port"]=port 

    
    return server_dic

