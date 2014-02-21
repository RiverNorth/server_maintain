# -*- coding:GBK -*-
import time
import sys
import module.read_server as read_server
import module.read_remote as read_remote
#import module.menu.item as item
#import module.menu.menu as menu
from module.sftp import *
from module.ssh import *
from module.telnet import *
from module.read_frame import *
import module.read_frame
import re

reload(sys)
sys.setdefaultencoding('GBK')

def make_dirpath(path):
	if not path.endswith("/"):
		path=path+"/"
	return path

def init_gdb_gs_sshclient(area_ids):
	#1.sort upload area in remote_ip
	bp_area_gdbdic=sort_area_in_remoteip(area_ids,True)
	bp_area_gssdic=sort_area_in_remoteip(area_ids,False)
	#2.init ssh client for all ip
	ssh_dic={}
	temp_list=[]
	temp_list.extend(bp_area_gdbdic.keys())
	temp_list.extend(bp_area_gssdic.keys())
	for ip_addr in temp_list:
		#if ssh for this ip_addr exsits then skip
		if ssh_dic.has_key(ip_addr):
			continue
		remote_config=remote_configs[ip_addr]
		ssh_client=Ssh(remote_config["ip_addr"],remote_config["ssh_user"],remote_config["ssh_password"])
		if Ssh.OP_OK!=ssh_client.login():
			print("error on ip[%s] login ssh:%s"%(ip_addr,ssh_client.error_str))
			return False
		ssh_dic[ip_addr]=ssh_client
	return ssh_dic


def read_server_configs():
	config=read_server.get_serconfig()
	if type(config)==type(""):
		print("error:load server config file")
		print config
		sys.exit(-1)
	return config

def convert_server_configs():
	temp_configs_dic={}
	for server_config in server_configs:
		temp_configs_dic[server_config["area_id"]]=server_config
	return temp_configs_dic

def get_server_nick_id():
	temp_nick_dic={}
	for area_id in area_configs.keys():
		server_configs=area_configs[area_id]
		assert not temp_nick_dic.has_key(server_configs["server_name"])
		temp_nick_dic[server_configs["server_name"]]=area_id
	return temp_nick_dic

#GS remote config
remote_configs=read_remote.get_remoteconfig()
server_configs=read_server_configs()
area_configs=convert_server_configs()
nick_id_dic=get_server_nick_id()




def upload_file(ip_str,local_file,force=False):
	remote_config=remote_configs[ip_str]
	sftp_client=Sftp(remote_config["ip_addr"],remote_config["sftp_user"],remote_config["sftp_password"])
	if Sftp.OP_OK!=sftp_client.login():
		print("uploads file error:%s" % sftp_client.error_str)
		return	False
	#get upload file path
	remote_path=remote_config["tmp_path"]
	if not remote_path.endswith("/"):
		remote_path=remote_path+"/"
	file_name=parse_path(local_file)[1]
	remote_file=remote_path+file_name

	if Sftp.OP_OK!=sftp_client.upload_files(remote_file,local_file,False,force):
		print("uploads file error:%s" % sftp_client.error_str)
		return False
	sftp_client.logout()
	return remote_file

def upload_and_unpack(ip_str,local_file,des_dirs):
	if not local_file.endswith("zip"):
		print("uploads file error:need local file to be zip file")
		return False
	
	#before upload delete all files
	remote_config=remote_configs[ip_str]
	ssh_client=Ssh(remote_config["ip_addr"],remote_config["ssh_user"],remote_config["ssh_password"])
	if Ssh.OP_OK!=ssh_client.login():
		print("ssh login error:%s" % ssh_client.error_str)
		return False
	
	remote_path=remote_config["tmp_path"]
	if not remote_path.endswith("/"):
		remote_path=remote_path+"/"
		
	del_cmd="cd %s;rm -r ./*"%(remote_path)
	print("exec cmd %s"%del_cmd)
	result=ssh_client.exec_command(del_cmd)
	if result[0]!=True:
		print("rm old file error:%s" % result[2])
		return False
				
	remote_file=upload_file(ip_str,local_file,True)
	if not remote_file:
		return False

	for des_dir in des_dirs:
		#befor delete it backup it
		backup_dir=make_dirpath(remote_config["backup_des_path"])
		dir_suffix = des_dir.split("/")[-2]+time.strftime("%m%d_%H%M%S")
		mkdir_cmd="mkdir -p %s" % (backup_dir +dir_suffix)
		ssh_client.exec_command(mkdir_cmd)
		backup_cmd="cd %s;cp -r ./* %s" % (des_dir,backup_dir + dir_suffix)
		print("exec cmd %s"%(backup_cmd))
		result=ssh_client.exec_command(backup_cmd)
		if result[0]!=True:
			print("backup file error:%s" % result[2])
			return False
		
		#before upload delete it
		del_cmd="cd %s;rm -r ./*"%(des_dir)
		print("exec cmd %s"%(del_cmd))
		result=ssh_client.exec_command(del_cmd)
		if result[0]!=True:
			print("rm file error:%s" % result[2])
			return False	
		#upload and unpack
		if Ssh.OP_OK!=ssh_client.unpack_remote_file(remote_file,des_dir):
			print("extract file error:%s" % ssh_client.error_str)
			return False
	return True

def upload_files(ip_str,local_file,des_files):
	remote_file=upload_file(ip_str,local_file)
	remote_config=remote_configs[ip_str]

	ssh_client=Ssh(remote_config["ip_addr"],remote_config["ssh_user"],remote_config["ssh_password"])
	if Ssh.OP_OK!=ssh_client.login():
			print("copy file error:%s" % ssh_client.error_str)
			return False
	for des_file in des_files:
		cmd="cp "+remote_file+" "+des_file
		result=ssh_client.exec_command(cmd)
		if result[0]!=True:
			print("copy file error:%s" % result[2])
			return False
	print("complete upload files")

def upload_config_file(area_id):
	server_config=False
	for i in server_configs:
		if i["area_id"]==area_id:
			server_config=i
			break
	dic_str="gdm_ip"
	remote_config=remote_configs[server_config[dic_str]]
	result=module.read_frame.upload_config_file(server_config,remote_config)
	if result==True:
		return True
	else:
		return False

def sort_area_in_remoteip(area_ids,isGDB,isGDM=False):
	upload_area_dic={}
	for area_id in area_ids:
		server_config=area_configs[area_id]
		dic_str="gss_ip"
		if isGDB:
			dic_str="gdb_ip"
		if isGDM:
			dic_str="gdm_ip"
		if not upload_area_dic.has_key(server_config[dic_str]):
			upload_area_dic[server_config[dic_str]]=[]
		upload_area_dic[server_config[dic_str]].append(server_config)
	return upload_area_dic

def get_upload_remotedir(ip_addr,upload_area_dic,isGDB):
	path_dic_str="gss_path"
	if isGDB:
		path_dic_str="gdb_path"
	remote_dirs=[]
	for server_config in upload_area_dic[ip_addr]:
		remote_dirs.append(server_config[path_dic_str])
	assert(len(remote_dirs)>0)
	return remote_dirs

def change_exec_name(server_config,ssh_client,name_pair):
	path_dic_str="gdm_path"
	remote_gs=make_dirpath(server_config[path_dic_str])+name_pair[1]
	new_remote_path=parse_path(remote_gs)[0]
	new_remote_gs=new_remote_path+server_config[name_pair[0]]
	cmd="mv %s %s"%(remote_gs,new_remote_gs)
	print("exec cmd[%s] "%cmd)
	result=ssh_client.exec_command(cmd)
	if result[0]!=True:
		print("exec failed:%s"%result[2])
		return False
	print("exec cmd[%s] complete!"%cmd)
	return True

def change_all_name(server_config,ssh_client):
	name_list=all_name_list
	for name_pair in name_list:
		result=change_exec_name(server_config,ssh_client,name_pair)
		if not result:
			return False
	return True


def change_all_area_name(area_ids):
	upload_area_dic=sort_area_in_remoteip(area_ids,False,True)
	for ip_addr in upload_area_dic.keys():
		#1.init ssh client
		remote_config=remote_configs[ip_addr]
		ssh_client=Ssh(remote_config["ip_addr"],remote_config["ssh_user"],remote_config["ssh_password"])
		if Ssh.OP_OK!=ssh_client.login():
			print("ssh login failed:%s"%ssh_client.error_str)
			return False
		#2.change area exec name
		for server_config in upload_area_dic[ip_addr]:
			print("begin change area [%d] exec name" % server_config["area_id"])
			if not change_all_name(server_config,ssh_client):
				print("!!!!!!!!!!failed change exec name")
				return False
	return True


def shangchuanfenqu(src_file,area_ids):
	ip_dic_str="gdm_ip"
	path_dic_str="gdm_path"
	upload_area_dic={}
	print("begin upload fenqu -----------------------------")
	#1.sort upload area in remote_ip
	for area_id in area_ids:
		server_config=area_configs[area_id]
		if not upload_area_dic.has_key(server_config[ip_dic_str]):
			upload_area_dic[server_config[ip_dic_str]]=[]
		upload_area_dic[server_config[ip_dic_str]].append(server_config)

	for ip_addr in upload_area_dic.keys():
		#2.get share dirs and remote dirs for upload
		remote_dirs=[]
		for server_config in upload_area_dic[ip_addr]:
			remote_dirs.append(server_config[path_dic_str])
		assert(len(remote_dirs)>0)

		#3. upload zip file and unpack it to share path
		print("begin upload and unpack file %s to %s" % (src_file,ip_addr))
		if not upload_and_unpack(ip_addr,src_file,remote_dirs):
			return False
		print("complete upload and unpack file %s to %s" % (src_file,ip_addr))


		#4. copy config file from temp path to  remotepath
		for server_config in upload_area_dic[ip_addr]:
			print("begin upload area[%d] config file to remote path" % server_config["area_id"])
			result=upload_config_file(server_config["area_id"])
			if result!=True:
				print("upload config file error:%s" % result)
				return False
			else:
				print("complete upload area[%d] config file to remote path" % server_config["area_id"])

	#6. change file name in remote path
	print("begin change process name")
	if not change_all_area_name(area_ids):
		print("failed begin change process name")
		return False
	print("end change process name")

	print("complete upload fenqu -----------------------------")
	return True

#won't override remote file
def piliangshangchuan(src_file,area_ids,relative_path,isGDB):
	#upload path must ends with / not begin with /
	if relative_path.startswith("/"):
		print("relative_path must be a relative_path not begin with '/' ")
		return False
	if not relative_path.endswith("/"):
		relative_path=relative_path+"/"
	print("upload files begin----------------------------------")
	#1.sort upload area in remote_ip
	upload_area_dic=sort_area_in_remoteip(area_ids,isGDB)
	for ip_addr in upload_area_dic.keys():
		#2 get remote dirs for upload
		remote_dirs=get_upload_remotedir(ip_addr,upload_area_dic,isGDB)
		# init sftp client
		remote_config=remote_configs[ip_addr]
		sftp_client=Sftp(remote_config["ip_addr"],remote_config["sftp_user"],remote_config["sftp_password"])
		if Sftp.OP_OK !=sftp_client.login():
			print("upload file error:sftp login failed %s" % sftp_client.error_str)
			return False
		#3 upload file to remote dirs
		for dir_path in remote_dirs:
			if not dir_path.endswith("/"):
				dir_path=dir_path+"/"
			upload_path=dir_path+relative_path
			print("upload file [%s] to [%s] in ip[%s]"%(src_file,upload_path,ip_addr))
			if Sftp.OP_OK != sftp_client.upload_files(upload_path,src_file,True):
				print("upload failed:%s" % sftp_client.error_str)
				return False
			else:
				print("complete")
		sftp_client.logout()
	print("upload files complete----------------------------------")
	return True

def backup_dir(ip_addrs,isGDB):
	print("begin backup files ----------------------------------")
	for ip_addr in ip_addrs:
		#1 get remote config
		remote_config=False
		if not remote_configs.has_key(ip_addr):
			print("cant find %s remote_config"%ip_addr)
			continue
		remote_config=remote_configs[ip_addr]
		#2 init ssh client
		ssh_client=Ssh(remote_config["ip_addr"],remote_config["ssh_user"],remote_config["ssh_password"])
		if Ssh.OP_OK!=ssh_client.login():
			print("Ssh login failed:%s" % ssh_client.error_str)
			return False

		#3 exec command and backup dir
		cmd="cd %s;tar -cjf %s/%s%s *"%(remote_config["backup_src_path"],\
		                                         remote_config["backup_des_path"],\
		                                         time.strftime("%m%d_%H%M%S"),\
		                                         ".tar.bz2")

		print("exec command %s "%cmd)
		result=ssh_client.exec_command(cmd,120)
		if True!=result[0]:
			print("exec %s failed:%s"%(cmd,result[2]))
			return False
	print("complete backup files ----------------------------------")
	return True

def backup_areas(area_ids,data_str):
	ssh_list=init_gdb_gs_sshclient(area_ids)
	if ssh_list==False:
		return False
	for area_id in area_ids:
		print("----begin backup area[%d]----"%area_id)
		server_config=area_configs[area_id]
		gdb_ip=server_config["gdb_ip"]
		gss_ip=server_config["gss_ip"]
		gdb_client=ssh_list[gdb_ip]
		gss_client=ssh_list[gss_ip]
		gdb_dir=make_dirpath(server_config["gdb_path"])
		gss_dir=make_dirpath(server_config["gss_path"])
		print("backup gdb dir in [%s]"%gdb_ip)
		#1.mkdir GDB backup dir
		gdb_backup_path=gdb_dir+"GDB_"+data_str+"_bak"
		cmd="mkdir %s"%(gdb_backup_path)
		print("exec [%s]"%cmd)
		result=gdb_client.exec_command(cmd)
		if result[0]!=True:
			print("exec [%s] failed:%s"%(cmd,result[2]))
			return False
		for copy_dir_name in GDB_copy_path_list:
			#1 del old dir
			cp_cmd="cd %s;cp -rf %s %s"%(gdb_dir,copy_dir_name,gdb_backup_path)
			print("exec [%s]"%cp_cmd)
			result=gdb_client.exec_command(cp_cmd)
			if result[0]!=True:
				print("exec [%s] failed:%s"%(cp_cmd,result[2]))
				return False

		print("backup gss dir in [%s]"%gss_ip)
		#1.mkdir GSS backup dir
		gss_backup_path=gss_dir+"GS_"+data_str+"_bak"
		cmd="mkdir %s"%(gss_backup_path)
		print("exec [%s]"%cmd)
		result=gss_client.exec_command(cmd)
		if result[0]!=True:
			print("exec [%s] failed:%s"%(cmd,result[2]))
			return False
		for copy_dir_name in GSS_copy_path_list:
			#1 del old dir
			cp_cmd="cd %s;cp -rf %s %s"%(gss_dir,copy_dir_name,gss_backup_path)
			print("exec [%s]"%cp_cmd)
			result=gss_client.exec_command(cp_cmd)
			if result[0]!=True:
				print("exec [%s] failed:%s"%(cp_cmd,result[2]))
				return False
	#5 close ssh server:
	for ip in ssh_list.keys():
		ssh_list[ip].logout()
	return True

"""
def backup_areas(area_ids,data_str):
	#1.sort upload area in remote_ip
	bp_area_gdbdic=sort_area_in_remoteip(area_ids,True)
	bp_area_gssdic=sort_area_in_remoteip(area_ids,False)
	#2.init ssh client for all ip
	ssh_dic={}
	temp_list=[]
	temp_list.extend(bp_area_gdbdic.keys())
	temp_list.extend(bp_area_gssdic.keys())
	for ip_addr in temp_list:
		#if ssh for this ip_addr exsits then skip
		if ssh_dic.has_key(ip_addr):
			continue
		remote_config=remote_configs[ip_addr]
		ssh_client=Ssh(remote_config["ip_addr"],remote_config["ssh_user"],remote_config["ssh_password"])
		if Ssh.OP_OK!=ssh_client.login():
			print("error on ip[%s] login ssh:%s"%(ip_addr,ssh_client.error_str))
			return False
		ssh_dic[ip_addr]=ssh_client
	#3.backup gdb dir
	for ip_addr in bp_area_gdbdic.keys():
		ssh_client=ssh_dic[ip_addr]
		gd_remote_config=remote_configs[ip_addr]
		gdb_remote_dirs=get_upload_remotedir(ip_addr,bp_area_gdbdic,True)
		for remote_dir in gdb_remote_dirs:
			remote_dir=make_dirpath(remote_dir)
			backup_file=make_dirpath(gd_remote_config["backup_des_path"])+"GDB_"+remote_dir.rsplit("/")[2]+"_"+data_str+".tar"
			cmd="cd %s;tar -cvf %s *"%(remote_dir,backup_file)
			print("exec [%s]"%cmd)
			result=ssh_client.exec_command(cmd)
			if result[0]!=True:
				print("exec [%s] failed:%s"%(cmd,result[2]))
				return False
	#4.backup gss dir
	for ip_addr in bp_area_gssdic.keys():
		ssh_client=ssh_dic[ip_addr]
		gs_remote_config=remote_configs[ip_addr]
		gss_remote_dirs=get_upload_remotedir(ip_addr,bp_area_gdbdic,True)
		for remote_dir in gss_remote_dirs:
			remote_dir=make_dirpath(remote_dir)
			backup_file=make_dirpath(gd_remote_config["backup_des_path"])+"GSS_"+remote_dir.rsplit("/")[2]+"_"+data_str+".tar"
			cmd="cd %s;tar -cvf %s *"%(remote_dir,backup_file)
			print("exec [%s]"%cmd)
			result=ssh_client.exec_command(cmd)
			if result[0]!=True:
				print("exec [%s] failed:%s"%(cmd,result[2]))
				False
	#5 close ssh server:
	for ip in ssh_dic.keys():
		ssh_dic[ip].logout()
	return True
"""

def shutdown_server(area_ids):
	for area_id in area_ids:
		print("-------begin shutdown on area [%d]---------"%area_id)
		result_str="CLOSED "
		print("shutdown area[%d] gs ----------------------------------"%area_id)
		exec_command_on_GS(area_id,shutdown_gs_cmds)
		if check_gs_listen_port(area_id):
			result_str="STILL OPEN!!!!!!!"
		print("gs prot %s"%result_str)

		print("shutdown area[%d] bs----------------------------------"%area_id)
		exec_command_on_BS(area_id,shutdown_bs_cmds)
		if check_bs_listen_port(area_id):
			result_str="STILL OPEN!!!!!!!"
		print("bs prot %s"%result_str)

		print("shutdown area[%d] ls----------------------------------"%area_id)
		exec_command_on_LS(area_id,shutdown_ls_cmds)
		if check_ls_listen_port(area_id):
			result_str="STILL OPEN!!!!!!!"
		print("ls prot %s"%result_str)

		print("shutdown area[%d] dba----------------------------------"%area_id)
		exec_command_on_DBA(area_id,shutdown_dba_cmds)
		if check_dba_listen_port(area_id):
			result_str="STILL OPEN!!!!!!!"
		print("dba prot %s"%result_str)

		print("shutdown area[%d] scs----------------------------------"%area_id)
		exec_command_on_SCS(area_id,shutdown_scs_cmds)
		if check_scs_listen_port(area_id):
			result_str="STILL OPEN!!!!!!!"
		print("scs prot %s"%result_str)
		if result_str=="STILL OPEN!!!!!!!":
			print("!!!!!!Failed shutdown on area [%d]!!!!!!"%area_id)
			return False
	return True


def gengxinfenqu(area_ids):
	ssh_list=init_gdb_gs_sshclient(area_ids)
	if ssh_list==False:
		return False
	for area_id in area_ids:
		print("----begin update area[%d]----"%area_id)
		server_config=area_configs[area_id]
		gdb_ip=server_config["gdb_ip"]
		gss_ip=server_config["gss_ip"]
		gdb_client=ssh_list[gdb_ip]
		gss_client=ssh_list[gss_ip]
		gdb_dir=make_dirpath(server_config["gdb_path"])
		gss_dir=make_dirpath(server_config["gss_path"])
		gdm_path=make_dirpath(server_config["gdm_path"])
		print("update gdb in [%s]"%gdb_ip)
		for copy_dir_name in GDB_copy_path_list:
			#1 del old dir
			del_cmd="cd %s;rm -r %s"%(gdb_dir,copy_dir_name)
			print("exec [%s]"%del_cmd)
			gdb_client.exec_command(del_cmd)
			#2 mk base path dir
			gdb_client.exec_command("mkdir %s"%(gdb_dir))
			#3 copy dir
			copy_path=gdm_path+copy_dir_name
			cmd="cd %s;cp %s ./ -r"%(gdb_dir,copy_path)
			print("exec [%s]"%cmd)
			result=gdb_client.exec_command(cmd)
			if result[0]!=True:
				print("exec [%s] failed:%s"%(cmd,result[2]))
				return False
		print("update gss in [%s]"%gss_ip)
		for copy_dir_name in GSS_copy_path_list:
			del_cmd="cd %s;rm -r %s"%(gss_dir,copy_dir_name)
			print("exec [%s]"%del_cmd)
			gss_client.exec_command(del_cmd)
			copy_path=gdm_path+copy_dir_name
			cmd="cd %s;cp %s ./ -r"%(gss_dir,copy_path)
			print("exec [%s]"%cmd)
			gss_client.exec_command("mkdir %s"%(gss_dir))
			result=gss_client.exec_command(cmd)
			if result[0]!=True:
				print("exec [%s] failed:%s"%(cmd,result[2]))
				return False
	#5 close ssh server:
	for ip in ssh_list.keys():
		ssh_list[ip].logout()
	return True


def startup_server(area_ids,isGDB):
	gdb_str="GDB"
	if not isGDB:
		gdb_str="GS"
	upload_area_dic=sort_area_in_remoteip(area_ids,isGDB)
	for ip_addr in upload_area_dic.keys():
		#1.init ssh client
		remote_config=remote_configs[ip_addr]
		ssh_client=Ssh(remote_config["ip_addr"],remote_config["ssh_user"],remote_config["ssh_password"])
		if Ssh.OP_OK!=ssh_client.login():
			print("ssh login failed:%s"%ssh_client.error_str)
			return False
		#2.exec server
		for server_config in upload_area_dic[ip_addr]:
			name_list=GSS_name_list
			if isGDB:
				name_list=GDB_name_list
			for name_pair in name_list:
				print("begin startup area[%d] on %s-----------------------------"%(server_config["area_id"],gdb_str))
				result=run_server_exec(server_config,ssh_client,name_pair,isGDB)
				if not result:
					return False
	return True

def startup_server1(area_ids,isGDB):
	gdb_str="GDB"
	if not isGDB:
		gdb_str="GS"
	upload_area_dic=sort_area_in_remoteip(area_ids,isGDB)
	fail_list=[]
	for ip_addr in upload_area_dic.keys():
		#1.init ssh client
		remote_config=remote_configs[ip_addr]
		ssh_client=Ssh(remote_config["ip_addr"],remote_config["ssh_user"],remote_config["ssh_password"])
		print("ip_addr %s"%remote_config["ip_addr"])
		if Ssh.OP_OK!=ssh_client.login():
			print("ssh login failed:%s"%ssh_client.error_str)
			return False
		#2.exec server
		for server_config in upload_area_dic[ip_addr]:
			print("begin startup area[%d] on %s-----------------------------"%(server_config["area_id"],gdb_str))
			repeat_cmd=False
			name_list=GSS_name_list
			if isGDB:
				name_list=GDB_name_list
			last_check=False
			for name_pair in name_list:
				if name_pair[0]=="dbu_name":
					continue
				result=run_server_exec(server_config,ssh_client,name_pair,isGDB,False)
				if not result:
					return False
				else:
					repeat_cmd=result
				if repeat_cmd:				
					check=[ssh_client,repeat_cmd,server_config["server_name"]]
				        if name_pair[0]=="gs_name":
					    last_check=check
					    continue					
					success_regex=check_list[name_pair[0]]
					if not success_regex:
					    continue					
					flag=True
					count=0
					while(True):
					    if count==15:
						fail_list.append(check)
						print("!!!!!Startup Failed:area[%s]!!!!!!!!"%check[2])
						flag=False
						break
					    count=count+1
					    print("exec %s"%check[1])
					    result=check[0].exec_command(check[1])
					    if result[0]!=True:
						print("!!!!!Startup Failed:area[%s]!!!!!!!!"%check[2])
						fail_list.append(check)
						flag=False
						break
					    a=success_regex.match(result[1])
					    if a:
						break
					    else:
						time.sleep(3)
						continue
					if not flag:
						break
			flag=True
			count=0
			while(last_check):
				if count==15:
					fail_list.append(last_check)
					flag=False
					print("!!!!!Startup Failed:area[%s]!!!!!!!!"%check[2])
				count=count+1
				print("exec %s"%last_check[1])
				result=last_check[0].exec_command(last_check[1])
				if result[0]!=True:
				    print("!!!!!Startup Failed:area[%s]!!!!!!!!"%last_check[2])
				    fail_list.append(last_check)
				    flag=False
				    break
				success_regex=check_list["gs_name"]
				a=success_regex.match(result[1])
				if a:
				    break
				else:
				    time.sleep(3)
				    continue
        #3.print error
	if len(fail_list)!=0:
		for fail_case in fail_list:
				print("area[%s] exec '%s' failed"%(fail_case[2],fail_case[1]))
				return False
	return True

def get_logined_telnet_client(area_id, service_name):
	server_config=area_configs[area_id]
	t = False
	if service_name == "GS":
		t = Telnet(server_config["gs_ip"],server_config["gs_telnet_port"],\
		           server_config["gs_telnet_user"],server_config["gs_telnet_pass"],gs_dic,3)
	elif service_name == "BS":
		t = Telnet(server_config["bs_telnet_ip"],server_config["bs_telnet_port"],\
		           server_config["bs_telnet_user"],server_config["bs_telnet_pass"],bs_dic,3)		
	elif service_name == "DBA":
		t = Telnet(server_config["dba_ip"],server_config["dba_telnet_port"],\
		           server_config["dba_telnet_user"],server_config["dba_telnet_pass"],dba_dic,3)		
	elif service_name == "LS":
		t = Telnet(server_config["ls_telnet_ip"],server_config["ls_telnet_port"],\
		           server_config["ls_telnet_user"],server_config["ls_telnet_pass"],ls_dic,3)	
	elif service_name == "SCS":
		t=Telnet(server_config["scs_ip"],server_config["scs_telnet_port"],\
			 server_config["scs_telnet_user"],server_config["scs_telnet_pass"],scs_dic,3)		
	else:
		return false
	result = t.login()
	if result != Telnet.OP_OK:
		print("telnet %s error:%s" %(service_name, t.error_str))
		return False
	else:
		return t

def shutdown_service(area_id, service_name, command_pairs):
	#1 init telnet client and init control step class
	telnet_client = get_logined_telnet_client(area_id, service_name)
	if not telnet_client:
		return False
	print("开始关闭[%s]"%(service_name))
	for command_pair in command_pairs:
		result = exec_commands_on_telnet1(telnet_client, command_pair)
		if result[0] != True or result[1].find(command_pair[1]) == -1:
			flag = False
			if command_pair[0] == "cmd.shutdown()" and result[1] == "socket port has been closed":
				print("\n在[%d]区[%s]关闭完成!\n"%(area_id, service_name))
				return True
			#如果等于printuser则需要再多判断几次 如果
			elif command_pair[0] == shutdown_gs_pairs[1][0]:
				count = 1
				while count < 6:
					result = exec_commands_on_telnet1(telnet_client, shutdown_gs_pairs[0])
					result = exec_commands_on_telnet1(telnet_client, shutdown_gs_pairs[1])
					if result[1].find(command_pair[1]) != -1 :
						print(result[1])
						time.sleep(2)
						flag = True
						break
			if not flag:		
				print("\n在[%d]区[%s]执行命令[%s]时失败!\n"%(area_id, service_name, command_pair[0]))
				print(result[1])
				return False
		else:
			print(result[1])

		

"""def startup_service(area_ids,services):
	#1.init all ssh client
	ssh_clients={}
	upload_area_dic_GDB=sort_area_in_remoteip(area_ids,True)
	upload_area_dic_GS =sort_area_in_remoteip(area_ids,False)
	for ip_addr in upload_area_dic_GDB.keys():
		remote_config=remote_configs[ip_addr]
		ssh_client=Ssh(remote_config["ip_addr"],remote_config["ssh_user"],remote_config["ssh_password"])
		if Ssh.OP_OK!=ssh_client.login():
			print("ssh login failed:%s"%ssh_client.error_str)
			continue
		ssh_clients[ip_addr]=ssh_client
	for ip_addr in upload_area_dic_GS.keys():
		if ssh_clients.has_key(ip_addr):
			continue
		remote_config=remote_configs[ip_addr]
		ssh_client=Ssh(remote_config["ip_addr"],remote_config["ssh_user"],remote_config["ssh_password"])
		if Ssh.OP_OK!=ssh_client.login():
			print("ssh login failed:%s"%ssh_client.error_str)
			continue
		ssh_clients[ip_addr]=ssh_client
	#2.init all ssh client
	for area_id in area_ids:
		server_config = area_configs[area_id]
		if gdb
"""		
			
	
			
			
	

def gengxinshujuku(area_ids):
	gdb_str="GDB"
	upload_area_dic=sort_area_in_remoteip(area_ids,True)
	failed_list=[]
	for ip_addr in upload_area_dic.keys():
		check_list=[]
		#1.init ssh client
		remote_config=remote_configs[ip_addr]
		ssh_client=Ssh(remote_config["ip_addr"],remote_config["ssh_user"],remote_config["ssh_password"])
		if Ssh.OP_OK!=ssh_client.login():
			print("ssh login failed:%s"%ssh_client.error_str)
			return False
		#2.exec server
		for server_config in upload_area_dic[ip_addr]:
			name_list=updateDB_name_list
			for name_pair in name_list:
				print("begin gengxinshujuku on area[%d]-----------------------------"%server_config["area_id"])
				result=run_server_exec(server_config,ssh_client,name_pair,True,False)
				if not result:
					failed_list.append(server_config["server_name"])
				elif name_pair[0]=="dbu_name":
					check_list.append([ssh_client,result,server_config["area_id"]])
		for check in check_list:
			area_id=check[2]
			flag=True
			#shutdown DBU and SCS
			while(True):
				result=check[0].exec_command(check[1])
				if result[0]!=True:
				    print("!!!!!tail log Failed:area[%s]!!!!!!!!"%check[2])
				    failed_list.append(check)
				    flag=False
				    break
			        print("-----------dbu log--------------")
				print(result[1])
				print("-----------dbu log--------------")
				w_o_s=raw_input("wait dbu finish or shutdown dbu or tag it failed? w/s/f\n").lower()
				if w_o_s=="w":
					continue
				elif w_o_s=="s":
					break
				elif w_o_s=="f":
					failed_list.append(check)
					flag=False
					break
			if not flag:
				continue
			result_str=False
			print("shutdown area[%d] DBU-------------------"%area_id)
			tmp_shutdown_cmd=copy.copy(shutdown_dbu_cmds)
			if check_dbu_listen_port(area_id):
				exec_command_on_DBU(area_id,tmp_shutdown_cmd)
				if check_dbu_listen_port(area_id):
					result_str="STILL OPEN!!!!!!!"
			else:
				result_str="CLOSED"
			print("DBU PORT %s"%result_str)

			print("shutdown area[%d] scs-------------------"%area_id)
			if check_scs_listen_port(area_id):
				exec_command_on_SCS(area_id,shutdown_scs_cmds)
				if check_scs_listen_port(area_id):
					result_str="STILL OPEN!!!!!!!"
			else:
				result_str="CLOSED"

			print("SCS PORT %s"%result_str)
			if result_str=="STILL OPEN!!!!!!!":
				failed_list.append(check)
				print("!!!!!!Failed shutdown SCS and DBU on area [%d]!!!!!!"%area_id)
	if len(failed_list)!=0:
		print("\n\n\n")
		for check in failed_list:
			print("!!!!!!!!!!!FAILED UPDATE DBU on area[%d]!!!!!!!!!!!!!!!!"%(check[2]))
		return False
	return True

def rejiazai(area_ids,cmd):
	flag=True
	for area_id in area_ids:
		print("-------begin reload file on area [%d]---------"%area_id)
		if not exec_command_on_GS(area_id,[cmd],True):
			print("!!!!!!!failed reload on area [%d] cmd[%s]!!!!!!!"%(area_id,cmd))
			flag=False
	return flag

def run_server_exec(server_config,ssh_client,name_pair,isGDB,need_sure=True):
	path_dic_str="gss_path"
	if isGDB:
		path_dic_str="gdb_path"
	remote_gs=make_dirpath(server_config[path_dic_str])+name_pair[1]
	new_remote_path=parse_path(remote_gs)[0]
	new_remote_exe=new_remote_path+server_config[name_pair[0]]
	new_remote_bash=new_remote_path+run_bash_dic[name_pair[0]].rsplit("/")[1]
	new_remote_dir,relative_exe=new_remote_bash.rsplit("/",1)
	new_log_gs=new_remote_path+log_list[name_pair[0]]
	chmod_cmd="chmod 770 %s"%(new_remote_exe)
	chmod_bash_cmd="chmod 770 %s"%(new_remote_bash)
	run_cmd="cd %s;./%s"%(new_remote_dir,relative_exe)
	repeat_command="tail %s -n 500"%(new_log_gs)
	#1.chmod 770
	result=ssh_client.exec_command(chmod_cmd)
	if result[0]!=True:
		print("exec failed:%s"%result[2])
		return False
	result=ssh_client.exec_command(chmod_bash_cmd)
	if result[0]!=True:
		print("exec failed:%s"%result[2])
		return False
	#2.exec process
	if need_sure:
		while True:
			y_or_n =raw_input("exec command [%s] continue or stop? y/n\n"%(run_cmd)).lower()
			if y_or_n=="y":
				break
			elif y_or_n=="n":
				return True
	result=ssh_client.exec_command(run_cmd)
	print("exec [%s]"%run_cmd)
	if result[0]!=True:
		print("exec failed:%s"%result[2])
		return False
	#3.tail -f log check whether need continue
	if need_sure:
		while True:
			result=ssh_client.exec_command(repeat_command)
			if result[0]!=True:
				print("exec failed:%s"%result[2])
				return False
			print("--------logdiplay--------\n")
			print(result[1])
			print("--------logdiplay--------\n")

			y_or_n =raw_input("go to open next process or wait ? y/n/w\n").lower()
			if y_or_n=="y":
				return True
			elif y_or_n=="n":
				return False
		print("exec cmd[%s] complete!",cmd)
	else:
		return repeat_command






#---------------------------------------------------------------------------------------
test_dic={
    Telnet.LOGIN_PROMT:"Login:",
    Telnet.LOGIN_PROMT_A:"Password:",
    Telnet.COMMAN_PROMT:"GS>"
}

UNKONW_STEP=-1
ERROR_STEP=0
GOTO_NEXT_STEP=1
QUIT_STEP=2
REPEAT_STEP=3


class ControlStepTelnet():
	def __init__(self,telnet_client):
		if telnet_client.logined==False:
			raise Exception("telnet not logined")
		self.telnet_client=telnet_client

	#show result and ask for whether continue
	def show_and_continue(self,show_string):
		print("---------------------------------------")
		print(show_string)
		print("---------------------------------------")
		while(True):
			y_o_n=raw_input("continue or quir or repeat y/n/r\n").lower()
			if y_o_n=="y":
				return GOTO_NEXT_STEP
			elif y_o_n=="n":
				return QUIT_STEP
			elif y_o_n=="r":
				return REPEAT_STEP

	def be_sure_exec_cmd(self,cmd):
		while True:
			y_o_n=raw_input("!!!!!!!!Are you sure want to exec [%s] y/n!!!!!!!!!!\n" % cmd).lower()
			if y_o_n == "y":
				return True
			elif y_o_n == "n":
				return False

	#control comman exec step
	def control_step(self,cmd,expect_list,needlog=False):
		if expect_list==False:
			expect_list=[self.telnet_client.expect_dic[Telnet.COMMAN_PROMT]]
		while True:
			#1 exec command and get output
			#1.2 exec cmd
			result=self.telnet_client.exec_command(cmd,expect_list,5)
			if result[0]!=0:
				print("exec [%s] error:%s"%(cmd,result[1]))
				return ERROR_STEP
			if needlog :
				print("------------log--------------------\n")
				print("%s"%(result[1]))
				print("------------log--------------------\n")
			#1.3 ask for whether go to next step
			will = self.show_and_continue(result[1])
			if will==GOTO_NEXT_STEP:
				return GOTO_NEXT_STEP
			elif will==QUIT_STEP:
				return QUIT_STEP
			elif will==REPEAT_STEP:
				continue
			else:
				return UNKONW_STEP

	def control_exec_commands(self,commands,needlog=False):
		for cmd in commands:
			#exec commands
			print("exec [%s]"%cmd)
			#ask whether goon
			will=self.control_step(cmd,False)
			if will==QUIT_STEP:
				continue
			elif will==ERROR_STEP:
				return False
			elif will==UNKONW_STEP:
				print("exec [%s] unknown error"%cmd)
				return False
		return True

	def shutdown_telnet(self):
		self.telnet_client.logout()



def exec_commands_on_telnet(logined_telnet_client,cmds,needlog=False):
	#1 init ControlStep
	con_step=ControlStepTelnet(logined_telnet_client)
	#2 control exec command chain
	result=con_step.control_exec_commands(cmds,needlog)
	#3 shutdown telnet port
	con_step.shutdown_telnet()
	return result

def exec_commands_on_telnet1(logined_telnet_client,cmd_pairs):
	expect_list=[logined_telnet_client.expect_dic[Telnet.COMMAN_PROMT]]
	result=logined_telnet_client.exec_command(cmd_pairs[0],expect_list,8)
	if result[0] == -1:
		return [False,result[1]]
	else:
		return [True,result[1]]



def exec_command_on_GS(area_id,cmds,needlog=False):
	#1 get server config by area_id
	server_config=area_configs[area_id]
	#2 init telnet client and init control step class
	t=Telnet(server_config["gs_ip"],server_config["gs_telnet_port"],\
	         server_config["gs_telnet_user"],server_config["gs_telnet_pass"],gs_dic,3)
	result=t.login()
	if result!=Telnet.OP_OK:
		print("telnet gs error:%s" % t.error_str)
		return False
	result=exec_commands_on_telnet(t,cmds,needlog)
	return result


def exec_command_on_BS(area_id,cmds):
	#1 get server config by area_id
	server_config=area_configs[area_id]
	#2 init telnet client and init control step class
	t=Telnet(server_config["bs_telnet_ip"],server_config["bs_telnet_port"],\
	         server_config["bs_telnet_user"],server_config["bs_telnet_pass"],bs_dic,3)
	result=t.login()
	if result!=Telnet.OP_OK:
		print("telnet bs error:%s" % t.error_str)
		return False
	result=exec_commands_on_telnet(t,cmds)
	return result

def exec_command_on_LS(area_id,cmds):
	#1 get server config by area_id
	server_config=area_configs[area_id]
	#2 init telnet client and init control step class
	t=Telnet(server_config["ls_telnet_ip"],server_config["ls_telnet_port"],\
	         server_config["ls_telnet_user"],server_config["ls_telnet_pass"],ls_dic,3)
	result=t.login()
	if result!=Telnet.OP_OK:
		print("telnet ls error:%s" % t.error_str)
		return False
	result=exec_commands_on_telnet(t,cmds)
	return result


def exec_command_on_DBA(area_id,cmds):
	#1 get server config by area_id
	server_config=area_configs[area_id]
	#2 init telnet client and init control step class
	t=Telnet(server_config["dba_ip"],server_config["dba_telnet_port"],\
	         server_config["dba_telnet_user"],server_config["dba_telnet_pass"],dba_dic,3)
	result=t.login()
	if result!=Telnet.OP_OK:
		print("telnet dba error:%s" % t.error_str)
		return False
	result=exec_commands_on_telnet(t,cmds)
	return result

def exec_command_on_SCS(area_id,cmds):
	#1 get server config by area_id
	server_config=area_configs[area_id]
	#2 init telnet client and init control step class
	t=Telnet(server_config["scs_ip"],server_config["scs_telnet_port"],\
	         server_config["scs_telnet_user"],server_config["scs_telnet_pass"],scs_dic,3)
	result=t.login()
	if result!=Telnet.OP_OK:
		print("telnet scs error:%s" % t.error_str)
		return False
	result=exec_commands_on_telnet(t,cmds)
	return result


def exec_command_on_DBU(area_id,cmds):
	#1 get server config by area_id
	server_config=area_configs[area_id]
	#2 init telnet client and init control step class
	t=Telnet(server_config["dbu_ip"],server_config["dbu_telnet_port"],\
	         server_config["dbu_telnet_user"],server_config["dbu_telnet_pass"],dbu_dic,3)
	result=t.login()
	if result!=Telnet.OP_OK:
		print("telnet dbu error:%s" % t.error_str)
		return False
	result=exec_commands_on_telnet(t,cmds)
	t.logout()
	return result

def check_gs_listen_port(area_id):
	#1 get server config by area_id
	server_config=area_configs[area_id]
	#2 init telnet client and init control step class
	t=Telnet(server_config["gs_ip"],server_config["gs_listen_port"],\
	         server_config["gs_telnet_user"],server_config["gs_telnet_pass"],test_dic,3)
	result=t.login()
	t.logout()
	if result!=Telnet.PORT_CLOSED_ERROR:
		return True
	else:
		return False

def check_ls_listen_port(area_id):
	#1 get server config by area_id
	server_config=area_configs[area_id]
	#2 init telnet client and init control step class
	t=Telnet(server_config["ls_ip_for_client"],server_config["ls_port_for_client"],\
	         server_config["gs_telnet_user"],server_config["gs_telnet_pass"],test_dic,3)
	result=t.login()
	t.logout()
	if result!=Telnet.PORT_CLOSED_ERROR:
		return True
	else:
		return False

def check_bs_listen_port(area_id):
	#1 get server config by area_id
	server_config=area_configs[area_id]
	#2 init telnet client and init control step class
	t=Telnet(server_config["bs_ip"],server_config["bs_listen_port"],\
	         server_config["gs_telnet_user"],server_config["gs_telnet_pass"],test_dic,3)
	result=t.login()
	t.logout()
	if result!=Telnet.PORT_CLOSED_ERROR:
		return True
	else:
		return False

def check_dba_listen_port(area_id):
	#1 get server config by area_id
	server_config=area_configs[area_id]
	#2 init telnet client and init control step class
	t=Telnet(server_config["dba_ip"],server_config["dba_listen_port"],\
	         server_config["gs_telnet_user"],server_config["gs_telnet_pass"],test_dic,3)
	result=t.login()
	t.logout()
	if result!=Telnet.PORT_CLOSED_ERROR:
		return True
	else:
		return False

def check_dbu_listen_port(area_id):
	#1 get server config by area_id
	server_config=area_configs[area_id]
	#2 init telnet client and init control step class
	t=Telnet(server_config["dbu_ip"],server_config["dbu_telnet_port"],\
	         server_config["gs_telnet_user"],server_config["gs_telnet_pass"],test_dic,3)
	result=t.login()
	t.logout()
	if result!=Telnet.PORT_CLOSED_ERROR:
		return True
	else:
		return False

def check_scs_listen_port(area_id):
	#1 get server config by area_id
	server_config=area_configs[area_id]
	#2 init telnet client and init control step class
	t=Telnet(server_config["scs_ip"],server_config["scs_listen_port"],\
	         server_config["gs_telnet_user"],server_config["gs_telnet_pass"],test_dic,3)
	result=t.login()
	t.logout()
	if result!=Telnet.PORT_CLOSED_ERROR:
		return True
	else:
		return False






# this case include override dir, overide file,True,false
def testcase1():
	shangchuanfenqu("/tmp/testbin/GDB.tar",[1,2],True)

# this case include override dir, overide file
def testcase2():
	piliangshangchuan("/tmp/abc.log",[1,2],"GS/",False)

# this case include override
def testcase3():
	backup_dir(["127.0.0.1"],True)

def testcase4():
	exec_command_on_GS(1,["cmd.clearuser()","cmd.printuser()"])

def testcase5():
	result=check_gs_listen_port(1)
	print result
def testcase6():
	result=shutdown_server([1])

def testcase7():
	startup_server([1,2],True)
	startup_server([1,2],False)
def testcase8():
	backup_areas([1,2],time.strftime("%m%d_%H%M%S"))

def main():
	testcase8()

if __name__ == '__main__':
	main()