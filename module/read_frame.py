# -*- coding:utf-8 -*-
from config import *
from sftp import *
from ssh import *
import os

def make_dirpath(path):
	if not path.endswith("/"):
		path=path+"/"
	return path

def upload_config_file(server_config,remote_config):
	path_dic_str="gdm_path"
	#1.prepare server config file in tmp dir
	prepare_config_file(server_config)
	#2.init sftp client
	client=Sftp(remote_config["ip_addr"],remote_config["sftp_user"],remote_config["sftp_password"])
	if Sftp.OP_OK!=client.login():
	    return "upload config file error:Sftp user/password error"
    
        ssh_client=Ssh(remote_config["ip_addr"],remote_config["ssh_user"],remote_config["ssh_password"])
	if Ssh.OP_OK!=ssh_client.login():
	    return "upload config file error:ssh user/password error"
	
	#3.read upload path
	remote_path=server_config[path_dic_str]
	cwd_path=os.getcwd() 
	#handle path that need link with another
	if not remote_path.endswith("/"):
	    remote_path=remote_path+"/"
	if not cwd_path.endswith("/"):
	    cwd_path=cwd_path+"/"   
	    
	#4.upload file
	up_load_bash_ini_dic=up_load_bash_ini_remote_dic
	for local_path in up_load_bash_ini_dic.keys():
	    remote_remote_path=remote_path+up_load_bash_ini_dic[local_path]
	    local_path=cwd_path+local_path.split("/",1)[1]
	    print("upload config from [%s] to [%s]"%(local_path,remote_remote_path))
	    if Sftp.OP_OK!=client.upload_files(remote_remote_path,local_path,False,True):
			return client.error_str
		
	#5.upload common_config file
	local_path = make_dirpath(server_config["common_config"]) +"common_config.lua"
	remote_remote_path=remote_path+RMT_COMMON_CONFIG_FILE
	if Sftp.OP_OK!=client.upload_files(remote_remote_path,local_path,False,True):
		return client.error_str	
	
	remote_remote_path =remote_path + RMT_SCS_CONFIG_DIR
	#5.upload scs_config file
	cmd="rm -r "+remote_remote_path
	print("exec cmd [%s]"%cmd)
	result=ssh_client.exec_command(cmd)
	if result[0]!=True:
		print("rm config dir error:%s" % result[2])
		return False
	
	cmd="mkdir "+remote_remote_path
	print("exec cmd [%s]"%cmd)
	result=ssh_client.exec_command(cmd)
	if result[0]!=True:
		print("mkdir config dir error:%s" % result[2])
		return False	
	
	remote_remote_path = make_dirpath(remote_remote_path)
	local_base_dir = make_dirpath(server_config["common_config"]) + "config/"
	for file_name in os.listdir(local_base_dir):
		local_path=local_base_dir + file_name
		print("upload config dir from [%s] to [%s]"%(local_path,remote_remote_path + file_name))
		client.sftp_client.put(local_path,remote_remote_path + file_name)
	return True


def prepare_config_file(server_config):
	read_bs_bash(server_config)
	read_bs_ini(server_config)
	read_gs_bash(server_config)
	read_gs_ini(server_config)
	read_ls_bash(server_config)
	read_ls_ini(server_config)
	read_dba_bash(server_config)
	read_dba_ini(server_config)
	read_dbu_bash(server_config)
	read_dbu_ini(server_config)		
	read_scs_bash(server_config)
	read_scs_ini(server_config)

def read_gs_bash(server_config):
    a=server_config
    f=open(GS_BASH_FILE,"r")
    string=f.read()
    f.close()
    
    f=open(TMP_GS_BASH_FILE,"w")
    f.write(string%(a["gs_name"],a["gs_name"],a["gs_name"],a["gs_name"]))
    f.close()    

def read_gs_ini(server_config):
    a=server_config
    f=open(GS_INI_FILE,"r")
    string=f.read()
    f.close()
    
    f=open(TMP_GS_INI_FILE,"w")
    f.write(string%(a["scs_listen_port"]))
    f.close()      

def read_dba_bash(server_config):
    a=server_config
    f=open(DBA_BASH_FILE,"r")
    string=f.read()
    f.close()
    
    f=open(TMP_DBA_BASH_FILE,"w")
    f.write(string%(a["dba_name"],a["dba_name"],a["dba_name"],a["dba_name"]))
    f.close()     

def read_dba_ini(server_config):
    a=server_config
    f=open(DBA_INI_FILE,"r")
    string=f.read()
    f.close()
    
    f=open(TMP_DBA_INI_FILE,"w")
    f.write(string%(a["scs_listen_port"]))
    f.close()  

def read_dbu_bash(server_config):
    a=server_config
    f=open(DBU_BASH_FILE,"r")
    string=f.read()
    f.close()
    
    f=open(TMP_DBU_BASH_FILE,"w")
    f.write(string%(a["dbu_name"],a["dbu_name"],a["dbu_name"],a["dbu_name"]))
    f.close()     
	
def read_dbu_ini(server_config):
    a=server_config
    f=open(DBU_INI_FILE,"r")
    string=f.read()
    f.close()
    
    f=open(TMP_DBU_INI_FILE,"w")
    f.write(string%(a["scs_listen_port"]))
    f.close()  

def read_bs_bash(server_config):
    a=server_config
    f=open(BS_BASH_FILE,"r")
    string=f.read()
    f.close()
    
    f=open(TMP_BS_BASH_FILE,"w")
    f.write(string%(a["bs_name"],a["bs_name"],a["bs_name"],a["bs_name"]))
    f.close()

def read_bs_ini(server_config):
    a=server_config
    f=open(BS_INI_FILE,"r")
    string=f.read()
    f.close()
    
    f=open(TMP_BS_INI_FILE,"w")
    f.write( string%(a["scs_listen_port"]))
    f.close()      

def read_ls_bash(server_config):
    a=server_config
    f=open(LS_BASH_FILE,"r")
    string=f.read()
    f.close()
    
    f=open(TMP_LS_BASH_FILE,"w")
    f.write( string%(a["ls_name"],a["ls_name"],a["ls_name"],a["ls_name"]))
    f.close()      

def read_ls_ini(server_config):
    a=server_config
    f=open(LS_INI_FILE,"r")
    string=f.read()
    f.close()
    
    f=open(TMP_LS_INI_FILE,"w")
    f.write( string%(a["scs_listen_port"]))
    f.close()      

def read_scs_bash(server_config):
    a=server_config
    f=open(SCS_BASH_FILE,"r")
    string=f.read()
    f.close()
    
    f=open(TMP_SCS_BASH_FILE,"w")
    f.write(string%(a["scs_name"],a["scs_name"],a["scs_name"],a["scs_name"]))
    f.close()     

def read_scs_ini(server_config):
    a=server_config
    f=open(SCS_INI_FILE,"r")
    string=f.read()
    f.close()
    
    f=open(TMP_SCS_INI_FILE,"w")
    f.write(string%(a["scs_listen_port"]))
    f.close()     

    
