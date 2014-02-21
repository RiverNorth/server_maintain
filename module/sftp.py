# -*- coding:utf-8 -*-
import paramiko 
import os
SFTP_PORT=22

def parse_path(path):
	result_list=path.rsplit("/",1)
	result_list[0]=result_list[0]+"/"
	return result_list


class Sftp():
	OP_OK = 0
	LOGIN_ERROR = 1
	UPLOAD_ERROR = 2
	BACKUP_ERROR = 3
	NOT_LOGINED = 4

	FILE_EXISTS=11
	FILE_NOT_EXISTS=12
	DIR_NOT_EXISTS=13
	
	LOGIN_ERRSTR="SFTP username or passwd error"
	NOTLOGIN_ERRSTR="Login First Please!"
	FILE_EXISTS_ERRSTR="%s file already exsits"
	FILE_NOT_EXISTS_ERRSTR="%s file not exsits"

	def __init__(self,hostname,username,passwd):
		self.hostname=hostname
		self.username=username
		self.passwd=passwd
		self.error_str=""
		self.logined=False
		self.sftp_client=False

	def login(self):
		try:
			t = paramiko.Transport((self.hostname, SFTP_PORT))
			t.connect(username=self.username, password=self.passwd)
			self.sftp_client=paramiko.SFTPClient.from_transport(t)
		except Exception,e:
			self.error_str=Sftp.LOGIN_ERRSTR
			try:
				t.close()
				return Sftp.LOGIN_ERROR
			except:
				return Sftp.LOGIN_ERROR
		self.logined=True
		return Sftp.OP_OK
	
	def logout(self):
		if not self.logined:
			return
		self.sftp_client.close()
		
	#local_path must be a file path!
	def upload_files(self,remote_path,local_path,is_remote_dir,isforce=False):
		if self.logined == False:
			self.error_str=Sftp.NOTLOGIN_ERRSTR
			return Sftp.UPLOAD_ERROR
		if not os.path.exists(local_path):
			self.error_str=Sftp.FILE_NOT_EXISTS_ERRSTR%(local_path)
			return Sftp.UPLOAD_ERROR
		
		# if remote_path is a dir path parse file name to ends of remote_path
		if is_remote_dir:
			if not remote_path.endswith("/"):
				remote_path=remote_path+"/"
			remote_path=remote_path+parse_path(local_path)[1]
		
		rt= self.remote_file_exists(remote_path)
		if not isforce and rt==Sftp.FILE_EXISTS:
			self.error_str=Sftp.FILE_EXISTS_ERRSTR
			return Sftp.UPLOAD_ERROR
		elif rt==Sftp.DIR_NOT_EXISTS:	
			try:
				self.sftp_client.mkdir(parse_path(remote_path)[0])
			except Exception,e:
				self.error_str==e.strerror
				return Sftp.UPLOAD_ERROR

		try:
			self.sftp_client.put(local_path,remote_path)
		except Exception,e:
			self.error_str=e.strerror
			return self.UPLOAD_ERROR
		return self.OP_OK


	
	def backup_files(self,remote_path,local_path):
		if not self.logined:
			self.error_str=Sftp.NOTLOGIN_ERRSTR
			return Sftp.BACKUP_ERROR

		if Sftp.FILE_EXISTS==self.remote_file_exists(remote_path):
			self.error_str=Sftp.FILE_EXISTS_ERRSTR%(remote_path)
			return Sftp.BACKUP_ERROR

		rt=self.local_file_exists(local_path)
		if Sftp.FILE_EXISTS==rt:
			self.error_str=Sftp.FILE_EXISTS_ERRSTR%(local_path)
			return Sftp.BACKUP_ERROR
		elif Sftp.DIR_NOT_EXISTS==rt:
			cmd="mkdir -p "+parse_path(local_path)[0]
			try:
				os.system(cmd)
			except Exception,e:
				self.error_str="failed make local dir"
				return Sftp.BACKUP_ERROR

		try:
			self.sftp_client.get(remote_path,local_path)
		except Exception,e:
			self.error_str=e.strerror
			return Sftp.BACKUP_ERROR
		return Sftp.OP_OK




	def local_file_exists(self,local_path):
		result_list=parse_path(local_path)
		file_path=result_list[0]
		file_name=result_list[1]
		if not os.path.exists(file_path):
			return Sftp.DIR_NOT_EXISTS
		if os.path.exists(local_path):
			return Sftp.FILE_EXISTS
		else:
			return Sftp.FILE_NOT_EXISTS


	def remote_file_exists(self,remote_path):
		result_list=parse_path(remote_path)
		file_path=result_list[0]
		file_name=result_list[1]
		try:
			file_names=self.sftp_client.listdir(file_path)
			for name in file_names:
				if name==file_name:
					return Sftp.FILE_EXISTS
			return Sftp.FILE_NOT_EXISTS
		except IOError,e:
			return Sftp.DIR_NOT_EXISTS

#success upload case		
def testcase1():
	client=Sftp("127.0.0.1","root","kvoing")
	assert(Sftp.OP_OK==client.login())
	assert(Sftp.OP_OK==client.upload_files("/tmp/abc/def/install.log","/home/Joey/install.log"))

#remote dir not exists successs case		
def testcase2():
	client=Sftp("127.0.0.1","Joey","kvoing")
	assert(Sftp.OP_OK==client.login())
	assert(Sftp.UPLOAD_ERROR==client.upload_files("/tmp/abc/def/install1.log","/home/Joey/install.log"))
	print("testcase2:error:%s"%(client.error_str))

#permission denied to mkdir case
def testcase3():
	client=Sftp("127.0.0.1","Joey","kvoing")
	assert(Sftp.OP_OK==client.login())
	assert(Sftp.UPLOAD_ERROR==client.upload_files("/tmp/abc/def/install1.log","/home/Joey/install1.log"))
	print("testcase3:error:%s"%(client.error_str))

#user or passwd login error case
def testcase4():
	client=Sftp("127.0.0.1","Joey1","kvoing")
	assert(Sftp.LOGIN_ERROR==client.login())
	print("testcase4:error:%s"%(client.error_str))

#backup success backup case
def testcase5():
	client=Sftp("127.0.0.1","root","kvoing")
	assert(Sftp.OP_OK==client.login())
	assert(Sftp.OP_OK==client.backup_files("/tmp/install32.log","/home/Joey/install321.log"))
	print("testcase5:error:%s"%(client.error_str))	
	
#permission denied for write case
def testcase6():
	client=Sftp("127.0.0.1","Joey","kvoing")
	assert(Sftp.OP_OK==client.login())
	assert(Sftp.BACKUP_ERROR==client.backup_files("/tmp/testdir/install.log","/home/Joey/Desktop/testdir/install321.log"))
	print("testcase5:error:%s"%(client.error_str))

#local dir not exists success backup case	
def testcase7():
	client=Sftp("127.0.0.1","Joey","kvoing")
	assert(Sftp.OP_OK==client.login())
	assert(Sftp.OP_OK==client.backup_files("/tmp/install.log","/home/Joey/Desktop/testdir1/install321.log"))
	print("testcase5:error:%s"%(client.error_str))
	
