# -*- coding:utf-8 -*-
import telnetlib
import socket
import copy
import time
import select

WAIT_TO_WRITE = 1
WAIT_TO_READ = 2

class Telnet():    
    
    CONNECT_ERRSTR= "cant link to host:%s"
    LOGIN_ERRSTR="Telnet username or passwd error"
    NOTLOGIN_ERRSTR="Login First Please!"
    RELOGIN_ERRSTR="already logined"
    
    FILE_EXISTS_ERRSTR="%s file already exsits"
    FILE_NOT_EXISTS_ERRSTR="%s file not exsits"
    PACK_PATH_ERROR="%s path contains %s,this will make operation never stop"
    
    OP_OK = 0
    LOGIN_ERROR = 1
    REMOTE_UNPACK_ERROR = 2
    REMOTE_PACK_ERROR = 3
    NOT_LOGINED = 4
    PORT_CLOSED_ERROR=5
    
    LOGIN_PROMT="LOGIN_PROMT"
    LOGIN_PROMT_A="PASSWD_PROMT"
    COMMAN_PROMT="COMMAND_PROMT"
    UNKNOW_PROMT="UNKNOWN_PROMT"
    
    def __init__(self,hostname,port,username,passwd,expect_dic,timeout):
	self.hostname=hostname
	self.port=port
	self.username=username
	self.passwd=passwd
	self.expect_dic=False
	if not self.extract_expect_para(expect_dic):
	    raise Exception("expect dic not correct")
	self.timeout=timeout
	
	self.error_str=""
	self.logined=False
	self.tel_client=telnetlib.Telnet()
    
    def extract_expect_para(self,expect_dic):
	if not expect_dic.has_key(Telnet.LOGIN_PROMT) or \
	   not expect_dic.has_key(Telnet.LOGIN_PROMT_A) or \
	   not expect_dic.has_key(Telnet.COMMAN_PROMT):
	    return False
	else:
	    self.expect_dic=copy.copy(expect_dic)
	    if not expect_dic.has_key(Telnet.UNKNOW_PROMT):
		self.expect_dic[Telnet.UNKNOW_PROMT] = "..."
	    return True
	

    def do_and_wait(self, command, expect, sock, wait_sec):
	found = False
	buff = ""
	status = WAIT_TO_WRITE
	while(not found):
	    rlist = []
	    wlist = []
	    xlist = []   
	    if status == WAIT_TO_WRITE:
		wlist = [sock]
	    elif status == WAIT_TO_READ:
		rlist = [sock]
	    timeout = True
	    triple = select.select(rlist, wlist, xlist, wait_sec)
	    if status == WAIT_TO_WRITE:
		for t_sock in triple[1]:
		    sock.send(command)
		    status = WAIT_TO_READ
		    timeout = False
		    continue
	    elif status == WAIT_TO_READ:
		for t_sock in triple[0]:
		    buff = buff + t_sock.recv(10000)
		if buff.find(expect) != -1:
		    found = True
		timeout = False

	    if timeout :
		return False
	return True, buff
	
    
    def login(self):
	try:
	    if self.logined:
		self.error_str=Telnet.RELOGIN_ERRSTR
		return Telnet.LOGIN_ERROR
	    if self.tel_client.sock!=0:
		self.tel_client.close()
	    self.tel_client.open(self.hostname,self.port)
	except socket.error,error:
	    self.error_str=error.message
	    return self.PORT_CLOSED_ERROR
	try:
	    sock = self.tel_client.get_socket()
	    sock.setblocking(False)
	    found = False
	    buff = ""
	    while(not found):
		rlist = [sock]
		wlist = []
		xlist = []   
		timeout = True
		triple = select.select(rlist, wlist, xlist, 3)
		for t_sock in triple[0]:
		    buff = buff + t_sock.recv(10000)
		    if buff.find("Login:") != -1:
			found = True
		    timeout = False
		if timeout :
		    return Telnet.LOGIN_ERROR
		
	    result_set = self.do_and_wait(self.username+"\r\n", "Password", sock, 3)
	    if not result_set[0]:
		print("telnet faild:%s"%result_set[1])
		return Telnet.LOGIN_ERROR 
	    result_set = self.do_and_wait(self.passwd+"\r\n", self.expect_dic[Telnet.COMMAN_PROMT], sock, 3)
	    if not result_set[0]:
		print("telnet faild:%s"%result_set[1])
		return Telnet.LOGIN_ERROR 	    
	    
	    self.logined=True
	    return Telnet.OP_OK	  
	
	    ##special case need do this
	    #self.tel_client.write(self.username+"\r\n")  
	    #time.sleep(1)
	    #result=self.exec_code(self.passwd,[ self.expect_dic[Telnet.COMMAN_PROMT] ],self.timeout)
	    #if result[0]==-1:
		#self.error_str=Telnet.LOGIN_ERRSTR
		#return Telnet.LOGIN_ERROR
	    #result=self.exec_code("",[ self.expect_dic[Telnet.COMMAN_PROMT] ],self.timeout)
	    #if result[0]==-1:
		#self.error_str=Telnet.LOGIN_ERRSTR
		#return Telnet.LOGIN_ERROR	    
	    #self.logined=True
	    #return Telnet.OP_OK
	except Exception,error:
	    self.logined=False
	    self.error_str=error.message
	    return Telnet.LOGIN_ERROR
    
    def logout(self):
	if not self.logined:
	    return Telnet.OP_OK
	self.tel_client.close()
	self.logined=False
	return Telnet.OP_OK
    
    def exec_command(self,command,expect_list,timeout):
	if not self.logined:
	    raise Exception("Try to exec comman but,telnet not logined")
	result_list=self.exec_code(command,expect_list,timeout)
	return result_list
    
    def wait_and_recv(self, sock, timeout, expect_list):
	retry_sec = 0
	buff =""
	found = False
	while(retry_sec <= timeout):
	    buff = buff + sock.read(1000)
	    if buff.find(expect_list[0])==-1:
		time.sleep(1)
		retry_sec = retry_sec + 1
	    else:
		found = True
		break
	return (found, buff)
    
    def exec_code(self,command,expect_list,timeout):
	if self.tel_client.sock==0:
	    raise Exception("Try to exec comman but,socket not open")
	command=command+"\r\n"
	try:	    
	    sock = self.tel_client.get_socket()
	    result_set = self.do_and_wait(command, expect_list[0], sock, timeout)

	    if result_set[1].find(Telnet.COMMAN_PROMT) == -1:
		 sock.send("\r\n\r\n")
	    if not result_set[0]:
		return (-1, result_set[1])
	    else:
		return (0, result_set[1])
	except socket.error,e:
	    return (-1,"socket port has been closed")
	except EOFError,e:
	    return (-1,"remote server shutdowned port")
	

test_dic={
    Telnet.LOGIN_PROMT:"Login:",
    Telnet.LOGIN_PROMT_A:"Password:",
    Telnet.COMMAN_PROMT:"GS>"
}

test_dic1={
    Telnet.LOGIN_PROMT_A:"Password:",
    Telnet.COMMAN_PROMT:"GS>"
}

#normal login case
def testcase1():
    t=Telnet("192.168.2.101",9920,"root","root",test_dic,3)
    result=t.login()
    assert(result==Telnet.OP_OK)
    result=t.logout()
    assert(result==Telnet.OP_OK)
    print("error_str %s"%t.error_str)
    
#user or password error case    
def testcase2():
    t=Telnet("192.168.2.101",9920,"root1","root",test_dic,3)
    result=t.login()
    assert(result==Telnet.LOGIN_ERROR)
    print("error_str %s"%t.error_str)

#socket error case   
def testcase3():
    t=Telnet("192.168.2.102",9920,"root1","root",test_dic,3)
    result=t.login()
    assert(result==Telnet.LOGIN_ERROR)
    print("error_str %s"%t.error_str)
    
#wrong case test_dic    
def testcase4():
    t=Telnet("192.168.2.101",9920,"root1","root",test_dic1,3)

#wrong case test unlogined cant exec command   
def testcase5():
    t=Telnet("192.168.2.101",9920,"root","root",test_dic,3)
    result=t.login()
    assert(result==Telnet.OP_OK)
    result=t.logout()
    assert(result==Telnet.OP_OK)
    result=t.exec_command("cmd.p_i(6)",["GS>"],4)
    assert(result[0]==1)
    print("result:%s"%result[1])
    print("error_str %s"%error_str)
    
#right case test  exec command   
def testcase6():
    t=Telnet("192.168.2.101",9920,"root","root",test_dic,3)
    result=t.login()
    assert(result==Telnet.OP_OK)
    result=t.exec_command("cmd.p_i(6)",["GS>"],4)
    assert(result[0]==0)
    print("result:%s"%result[1].decode("gb18030"))
    result=t.exec_command("cmd.p_i(6)",["GS>"],4)
    assert(result[0]==0)
    print("result:%s"%result[1].decode("gb18030")) 


def main():
	testcase6()
	
if __name__ == '__main__':
	main()	