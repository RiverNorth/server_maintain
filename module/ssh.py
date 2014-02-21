# -*- coding:utf-8 -*-
import paramiko 
import socket
import os

def parse_path(path):
	result_list=path.rsplit("/",1)
	result_list[0]=result_list[0]+"/"
	return result_list

class Ssh():
    CONNECT_ERRSTR= "cant link to host:%s"
    LOGIN_ERRSTR="SSH username or passwd error"
    NOTLOGIN_ERRSTR="Login First Please!"
    
    FILE_EXISTS_ERRSTR="%s file already exsits"
    FILE_NOT_EXISTS_ERRSTR="%s file not exsits"
    PACK_PATH_ERROR="%s path contains %s,this will make operation never stop"
    
    
    OP_OK = 0
    LOGIN_ERROR = 1
    REMOTE_UNPACK_ERROR = 2
    REMOTE_PACK_ERROR = 3
    NOT_LOGINED = 4    
    
    FILE_EXISTS=11
    FILE_NOT_EXISTS=12
    DIR_NOT_EXISTS=13
    
    def __init__(self,hostname,username,passwd):
	self.hostname=hostname
	self.username=username
	self.passwd=passwd
	self.error_str=""
	self.logined=False
	self.ssh_client=False
	
    def login(self):
	self.ssh_client=paramiko.SSHClient()
	self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
	    self.ssh_client.connect(hostname=self.hostname,username=self.username,password=self.passwd)
	except socket.error,error:
	    self.error_str=Ssh.CONNECT_ERRSTR%(self.hostname)
	    return Ssh.LOGIN_ERROR
	except paramiko.AuthenticationException,error:
	    self.error_str=Ssh.LOGIN_ERRSTR
	    return Ssh.LOGIN_ERROR
	self.logined=True
	return Ssh.OP_OK

    def logout(self):
	    self.ssh_client.close()
    
    def unpack_remote_file(self,r_src_file,r_des_path):
	if not self.logined:
		self.error_str=Ssh.NOTLOGIN_ERRSTR
		return Ssh.REMOTE_UNPACK_ERROR
	#judge whether unpack file exsits
	rt=self.remote_file_exists(r_src_file,False)
	if rt!=Ssh.FILE_EXISTS:
		self.error_str=Ssh.FILE_NOT_EXISTS_ERRSTR%("remote file:"+r_src_file)
		return Ssh.REMOTE_UNPACK_ERROR
	
	#judge whether unpack despath exsits 
	rt=self.remote_file_exists(r_des_path,True)
	#if not exsits make the dir recursively
	if rt==Ssh.DIR_NOT_EXISTS:
		cmd="mkdir -p "+r_des_path
		result=self.exec_command(cmd)
		if not result[0]:
			return Ssh.REMOTE_UNPACK_ERROR	
		
	#unpack file
	cmd="cd "+r_des_path+";"
	cmd=cmd+"unzip "+r_src_file
	result=self.exec_command(cmd)
	if result[0]:
		return Ssh.OP_OK
	else:
		return Ssh.REMOTE_UNPACK_ERROR
	
	
    def pack_remote_dir(self,r_src_path,r_des_file):
	if not self.logined:
		self.error_str=Ssh.NOTLOGIN_ERRSTR
		return Ssh.REMOTE_PACK_ERROR
	
	#judge whether pack path exsits
	rt=self.remote_file_exists(r_src_path,True)
	if rt!=Ssh.FILE_EXISTS:
		self.error_str=Ssh.FILE_NOT_EXISTS_ERRSTR%("remote path:"+r_src_path)
		return Ssh.REMOTE_UNPACK_ERROR
	
	#judge whether unpack despath exsits 
	rt=self.remote_file_exists(r_des_file,False)
	#if not exsits make the dir recursively
	if rt==Ssh.FILE_EXISTS:
		self.error_str=Ssh.FILE_EXISTS_ERRSTR%("remote file:"+r_des_file)
		return Ssh.REMOTE_UNPACK_ERROR
	elif rt==Ssh.DIR_NOT_EXISTS:
		r_des_dir=parse_path(r_des_file)[0]
		cmd="mkdir -p "+r_des_dir
		result=self.exec_command(cmd)
		if not result[0]:
			return Ssh.REMOTE_PACK_ERROR
	cmd="cd "+r_src_path+";"
	cmd=cmd+"tar -cvf "+r_des_file+" *"
	if r_des_file.startswith(r_src_path):
		self.error_str=Ssh.PACK_PATH_ERROR%(r_des_file,r_src_path)
		return Ssh.REMOTE_PACK_ERROR
	
	result=self.exec_command(cmd)
	if not result[0]:
		return Ssh.REMOTE_PACK_ERROR
	else:
		return Ssh.OP_OK
	    
	    
	    
    def exec_command(self,cmd,timeout=5):
	if not self.logined:
		self.error_str=Ssh.NOTLOGIN_ERRSTR
		return False
	if not cmd.endswith(";"):
		cmd=cmd+(";")
	cmd=cmd+"echo $?"
	stdin,stdou,stderr=self.ssh_client.exec_command(cmd)
	error_str=stderr.read()
	result_str=stdou.read()
	result=result_str.endswith("0\n")
	if not result:
		self.error_str=error_str
		return (False,result_str,error_str)
	else:
		output_str=result_str.rsplit("0\n",1)[0]
		return (True,output_str,error_str)

	    
    def remote_file_exists(self,remote_path,is_dir):
	path_name=remote_path
	if not is_dir:
		result_list=parse_path(remote_path)
		path_name=result_list[0]
	stdin,stdout,stderr=self.ssh_client.exec_command("ls "+path_name)
	error_str=stderr.read()
	#if ls dir error if isfile then dir not exists
	if error_str!="":
		return Ssh.DIR_NOT_EXISTS
	#if is dir we can sure dir not exists
	if is_dir:
		return Ssh.FILE_EXISTS
	
	stdin,stdout,stderr=self.ssh_client.exec_command("ls "+remote_path)
	error_str=stderr.read()
	#if dir exits we judge whether file exists
	if error_str!="":
		return Ssh.FILE_NOT_EXISTS
	
	return Ssh.FILE_EXISTS

    def multi_copy(self,path_pairs,force):
	for path_pair in path_pairs:
		local_path=path_pair[0]
		remote_path=path_pair[1]
		#judge wether remote_path exists
		result=self.remote_file_exists(remote_path,True)
		if result==Ssh.FILE_EXISTS:
			cmd="cd "+remote_path+";rm * -rf"
			if self.exec_command(cmd)[0]!=True:
				return False
		elif result==Ssh.DIR_NOT_EXISTS:
			cmd="mkdir -p "+remote_path
			if self.exec_command(cmd)[0]!=True:
				return False		
		
		cmd="cd %s ;cp -r "%(local_path)
		if force:
			cmd=cmd+"-f "
		cmd=cmd+"./* "+remote_path
		if self.exec_command(cmd)[0]!=True:
			return False
	return True	

#this case success pack remote dir
def testcase1():
	ssh_client=Ssh("127.0.0.1","root","kvoing")
	ssh_client.login()
	result=ssh_client.pack_remote_dir("/home/mrw/testdir","/home/mrw/123456.tar")
	print("testcase1:error:%s"%(ssh_client.error_str))
	assert(Ssh.OP_OK==result)
	
#this case will make des dir cause it doesn't appears	
def testcase2():
	ssh_client=Ssh("127.0.0.1","root","kvoing")
	ssh_client.login()
	assert(Ssh.OP_OK==ssh_client.pack_remote_dir("/home/mrw/testdir","/home/mrw/test1dir/123456.tar"))
	print("testcase1:error:%s"%(ssh_client.error_str))
#this case will failed cause id did't login
def testcase3():
	ssh_client=Ssh("127.0.0.1","root","kvoing")
	assert(Ssh.REMOTE_PACK_ERROR==ssh_client.pack_remote_dir("/home/Joey/testdir","/home/Joey/test1dir/123456.tar"))
	print("testcase1:error:%s"%(ssh_client.error_str))

#this case will failed cause passwd wasn't correct
def testcase4():
	ssh_client=Ssh("127.0.0.1","root1","kvoing")
	assert(Ssh.LOGIN_ERROR==ssh_client.login())
	print("testcase1:error:%s"%(ssh_client.error_str))

#this case will failed permission denied
def testcase5():
	ssh_client=Ssh("127.0.0.1","mrw","kvoing")
	ssh_client.login()
	result=ssh_client.pack_remote_dir("/home/mrw/testdir","/home/mrw/test1dir/123456.tar")
	print("testcase1:error:%s"%(ssh_client.error_str))
	assert(Ssh.REMOTE_PACK_ERROR==result)


#this case need force overide file and dirctory ,and auto mkdir dir
def testcase6():
	ssh_client=Ssh("127.0.0.1","root","kvoing")
	ssh_client.login()
	result=ssh_client.multi_copy([("/tmp/dir1","/tmp/dir2"),("/tmp/dir3","/tmp/dir4/dir5")],True)
	print("error:",ssh_client.error_str)

def main():
	testcase6()
	
if __name__ == '__main__':
	main()	