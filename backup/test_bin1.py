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


#GS remote config 
remote_configs=read_remote.get_remoteconfig()
server_configs=read_server_configs()
area_configs=convert_server_configs()



def make_dirpath(path):
	if not path.endswith("/"):
		path=path+"/"
	return path

def upload_file(ip_str,local_file):
	remote_config=remote_configs[ip_str]
	sftp_client=Sftp(remote_config["ip_addr"],remote_config["sftp_user"],remote_config["sftp_password"])
	if Sftp.OP_OK!=sftp_client.login():
		print("uploads file error:%s" % sftp_client.error_str)
		return	
	#get upload file path
	remote_path=remote_config["tmp_path"]
	if not remote_path.endswith("/"):
		remote_path=remote_path+"/"
	file_name=parse_path(local_file)[1]
	remote_file=remote_path+file_name
	
	if Sftp.OP_OK!=sftp_client.upload_files(remote_file,local_file,False):
		print("uploads file error:%s" % sftp_client.error_str)	
		return 
	sftp_client.logout()	
	return remote_file
	
def upload_and_unpack(ip_str,local_file,des_dirs):
	if not local_file.endswith("tar"):
		print("uploads file error:need local file to be tar file")
		return False	
	remote_file=upload_file(ip_str,local_file)
	remote_config=remote_configs[ip_str]
	
	ssh_client=Ssh(remote_config["ip_addr"],remote_config["ssh_user"],remote_config["ssh_password"])
	if Ssh.OP_OK!=ssh_client.login():
		print("extract file error:%s" % ssh_client.error_str)
		return False
	for des_dir in des_dirs:
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
			return 
	for des_file in des_files:
		cmd="cp "+remote_file+" "+des_file
		result=ssh_client.exec_command(cmd)
		if result[0]!=True:
			print("copy file error:%s" % ssh_client.error_str)
			return 
	print("complete upload files")
	
def upload_config_file(area_id):
	server_config=False
	for i in server_configs:
		if i["area_id"]==area_id:
			server_config=i
			break
	remote_config=remote_config=remote_configs[server_config["share_ip"]]
	module.read_frame.upload_config_file(server_config,remote_config)
	
def sort_area_in_remoteip(area_ids):
	upload_area_dic={}
	for area_id in area_ids:
		server_config=area_configs[area_id]
		if not upload_area_dic.has_key(server_config["share_ip"]):
			upload_area_dic[server_config["share_ip"]]=[]
		upload_area_dic[server_config["share_ip"]].append(server_config)
	return upload_area_dic

def get_upload_remotedir(ip_addr,upload_area_dic):
	remote_dirs=[]
	for server_config in upload_area_dic[ip_addr]:
		remote_dirs.append(server_config["remote_path"])
	assert(len(remote_dirs)>0)
	return remote_dirs

def change_exec_name(server_config,ssh_client,name_pair):
	for server_config in upload_area_dic[ip_addr]:
		remote_gs=make_dirpath(server_config["remote_path"])+name_pair[1]
		new_remote_path=parse_path(remote_gs)[0]
		new_remote_gs=new_remote_path+server_config[name_pair[0]]
		cmd="mv {0} {1}".format(remote_gs,new_remote_gs)
		print("exec cmd[%s] ",cmd)
		result=ssh_client.exec_command(cmd)
		if result[0]!=True:
			print("exec failed:%s"%result[2])
			return False
		print("exec cmd[%s] complete!",cmd)

def change_all_name(server_config,ssh_client):
	for name_pair in name_list:
		result=change_exec_name(server_config,ssh_client,name_pair)
		if not result:
			return False
	return True

def start_up_allprocess(server_config,ssh_client):
	for name_pair in name_list:
		result=

def change_all_area_name(area_ids):
	print("begin change exec name -----------------------------")
	upload_area_dic=sort_area_in_remoteip(area_ids)
	for ip_addr in upload_area_dic:
		#1.init ssh client 
		remote_config=remote_configs[ip_addr]
		ssh_client=Ssh(remote_config["ip_addr"],remote_config["ssh_user"],remote_config["ssh_password"])
		if Ssh.OP_OK!=ssh_client.login():
			print("ssh login failed:%s"%ssh_client.error_str)
			return False
		#2.change area exec name
		for area_id in upload_area_dic[ip_addr]:
			print("begin change area [%d] exec name"%area_id)
			server_config=area_configs[area_id]
			if not change_all_name(server_config,ssh_client):
				print("!!!!!!!!!!failed change exec name")
		
		
def shangchuanfenqu(src_file,area_ids):
	upload_area_dic={}
	print("begin upload fenqu -----------------------------")
	#1.sort upload area in remote_share_ip
	for area_id in area_ids:
		server_config=area_configs[area_id]
		if not upload_area_dic.has_key(server_config["share_ip"]):
			upload_area_dic[server_config["share_ip"]]=[]
		upload_area_dic[server_config["share_ip"]].append(server_config)

	for ip_addr in upload_area_dic.keys():
		#2.get share dirs and remote dirs for upload
		remote_dirs=[]
		copy_dir_pairs=[]
		for server_config in upload_area_dic[ip_addr]:
			remote_dirs.append(server_config["share_path"])
			copy_dir_pairs.append((server_config["share_path"],server_config["remote_path"]))
		assert(len(remote_dirs)>0)
	
		#3. upload tar file and unpack it to share path
		print("begin upload and unpack file %s to %s" % (src_file,ip_addr))
		if not upload_and_unpack(ip_addr,src_file,remote_dirs):
			return False
		print("complete upload and unpack file %s to %s" % (src_file,ip_addr))
	
		#4. copy file from share_path to remote_path
		remote_config=remote_configs[ip_addr]
		print("begin copy file on %s to online dir" % ip_addr)
		ssh_client=Ssh(remote_config["ip_addr"],remote_config["ssh_user"],remote_config["ssh_password"])
		if Ssh.OP_OK!=ssh_client.login():
			print("ssh login failed:%s"%ssh_client.error_str)
			return False
		if not ssh_client.multi_copy(copy_dir_pairs,True):
			print("copy file failed:%s"%ssh_client.error_str)
			return False
		print("complete copy file on %s to online dir" % ip_addr)
		
		#5. copy config file from temp path to sharepath and remotepath
		for server_config in upload_area_dic[ip_addr]:
			print("begin upload area[%d] config file to share path and remote path" % server_config["area_id"])
			result=upload_config_file(server_config["area_id"])
			if result:
				print("upload config file error:%s" % result)
				return False
			else:
				print("complete upload area[%d] config file to share path and remote path" % server_config["area_id"])
	
	#6. change file name in remote path
	print("begin change process name")
	if not change_all_area_name(area_ids):
		print("failed begin change process name")
		return False
	print("end change process name")
		
	print("complete upload fenqu -----------------------------")	
	return True	
			
def piliangshangchuan(src_file,area_ids,relative_path,isGDB):
	#upload path must ends with / not begin with /
	if relative_path.startswith("/"):
		print("relative_path must be a relative_path not begin with '/' ")
		return False
	if not relative_path.endswith("/"):
		relative_path=relative_path+"/"	
	print("upload files begin----------------------------------")
	#1.sort upload area in remote_share_ip
	upload_area_dic=sort_area_in_remoteip(area_ids)	
	for ip_addr in upload_area_dic.keys():
		#2 get remote dirs for upload
		remote_dirs=get_upload_remotedir(ip_addr,upload_area_dic)
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
	print("upload files complete----------------------------------")
	return True
			
def backup_dir(ip_addrs):
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
		cmd="cd {0};tar -cjf {1}/{2}{3} *".format(remote_config["backup_src_path"],\
		                                         remote_config["backup_des_path"],\
		                                         time.strftime("%m%d%H%M%S"),\
		                                         ".tar.bz2")
		
		print("exec command %s "%cmd)
		result=ssh_client.exec_command(cmd,120)
		if True!=result[0]:
			print("exec %s failed:%s"%(cmd,result[2]))
			return False
	print("complete backup files ----------------------------------")
	return True

def shutdown_server(area_ids):
	for area_id in area_ids:
		print("shutdown area[%d] gs ----------------------------------"%area_id)
		exec_command_on_GS(area_id,shutdown_gs_cmds)
		print("shutdown area[%d] bs----------------------------------"%area_id)
		exec_command_on_BS(area_id,shutdown_bs_cmds)
		print("shutdown area[%d] ls----------------------------------"%area_id)
		exec_command_on_LS(area_id,shutdown_ls_cmds)
		print("shutdown area[%d] dba----------------------------------"%area_id)
		exec_command_on_DBA(area_id,shutdown_dba_cmds)
		print("shutdown area[%d] scs----------------------------------"%area_id)
		exec_command_on_SCS(area_id,shutdown_scs_cmds)
		
def startup_server(area_ids):
	print("begin change exec name -----------------------------")
	upload_area_dic=sort_area_in_remoteip(area_ids)
	for ip_addr in sort_area_in_remoteip.keys():
		#1.init ssh client
		remote_config=remote_configs[ip_addr]
		ssh_client=Ssh(remote_config["ip_addr"],remote_config["ssh_user"],remote_config["ssh_password"])
		if Ssh.OP_OK!=ssh_client.login():
			print("ssh login failed:%s"%ssh_client.error_str)
			return False
		#2.change area exec name
		for area_id in upload_area_dic[ip_addr]:
			print("begin change area [%d] exec name"%area_id)
			server_config=area_configs[area_id]
			if not change_all_name(server_config,ssh_client):
				print("!!!!!!!!!!failed change exec name")


		
		

		
		
	

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
		print(show_string.decode("GB18030"))
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
	def control_step(self,cmd,expect_list):		
		if expect_list==False:
			expect_list=self.telnet_client.expect_dic[Telnet.COMMAN_PROMT]
		while True:
			#1 exec command and get output
			#1.1 be sure want to  exec command
			c_will=be_sure_exec_cmd(cmd)
			if not c_will:
				return QUIT_STEP
			#1.2 exec cmd
			result=self.telnet_client.exec_command(cmd,expect_list,5)
			if result[0]!=0:
				print("exec [%s] error:%s"%(cmd,result[1]))
				return ERROR_STEP
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
		
	def control_exec_commands(self,commands):
		for cmd in commands:
			#exec commands 
			print("exec [%s]"%cmd)
			#ask whether goon
			will=self.control_step(cmd,False)	
			if will==QUIT_STEP:
				return True
			elif will==ERROR_STEP:
				return False
			elif will==UNKONW_STEP:
				print("exec [%s] unknown error"%cmd)
				return False
	
	def shutdown_telnet(self):
		self.telnet_client.logout()
			
			

def exec_commands_on_telnet(logined_telnet_client,cmds):
	#1 init ControlStep
	con_step=ControlStepTelnet(logined_telnet_client)
	#2 control exec command chain
	result=con_step.control_exec_commands(cmds)
	#3 shutdown telnet port
	con_step.shutdown_telnet()
	return result



def exec_command_on_GS(area_id,cmds):
	#1 get server config by area_id
	server_config=area_configs[area_id]
	#2 init telnet client and init control step class
	t=Telnet(server_config["gs_ip"],server_config["gs_telnet_port"],\
	         server_config["gs_telnet_user"],server_config["gs_telnet_pass"],gs_dic,3)
	result=t.login()
	if result!=Telnet.OP_OK:
		print("telnet gs error:%s" % t.error_str)
		return False
	result=exec_commands_on_telnet(t,cmds)
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
	




def start_up_area(area_ids):
	pass
	
def run_server():
	pass
		


	
	
# this case include override dir, overide file		
def testcase1():
	shangchuanfenqu("/tmp/testtar/1.tar",[1])
	
# this case include override dir, overide file		
def testcase2():
	piliangshangchuan("/tmp/abc.log",[1,2],"1dir/3dir")

# this case include override	
def testcase3():
	backup_dir(["127.0.0.1"])
	
#
def testcase4():
	exec_command_on_GS(1,["cmd.clearuser()","cmd.printuser()"])

def testcase5(): 
	result=check_gs_listen_port(1)
	print result
def testcase6():
	result=shutdown_server([1])
def main():
	testcase6()
	#for i in server_configs:
		#string=read_common_config(i)
		#f=open("abc.test","w")
		#f.write(string)
		#f.close()

	#des_dirs=[]
	#for i in range(1,6):
		#des_dirs.append("/tmp/a"+str(i)+"/"+"456.log")
	#upload_files("127.0.0.1","/tmp/456/456.log",des_dirs)

	#des_dirs=[]
	#for i in range(1,6):
		#des_dirs.append("/tmp/aa"+str(i))
	#upload_and_unpack("127.0.0.1","/tmp/456/123456.tar",des_dirs)	
if __name__ == '__main__':
	main()	