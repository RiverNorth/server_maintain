import pexpect
from pexpect import spawn

class Sftp(spawn):
    OP_OK = 0
    LOGIN_ERROR = 1
    UPLOAD_ERROR = 2
    BACKUP_ERROR = 3
    NOT_LOGINED = 4
    
    NOTLOGIN_ERRSTR="Login First Please!"
    def __init__(self,timeout=10):
        self.name='<sftp>'
        self.PROMPT="sftp>"
        self.logined=False
        self.err_str=""
        spawn.__init__(self, None, timeout=timeout)
        
    def login(self,server,username,passwd,timeout=30):
        host=username+"@"+server
        cmd="sftp "+host
        spawn._spawn(self, cmd)
        try:
            i=self.expect(["Are you sure you want to continue connecting","Permanently added","password"],5)
            if i==0:
                self.sendline("yes")
                self.expect(["Are you sure you want to continue connecting","Permanently added","password"],5)
            if i==1:
                self.sendline("yes")
                self.expect(["Are you sure you want to continue connecting","Permanently added","password"],5)
            if i==2:
                self.sendline(passwd)
                self.expect(self.PROMPT,5)
        except pexpect.TIMEOUT:
            self.err_str=self.before 
            return Sftp.LOGIN_ERROR
        self.logined=True
        return Sftp.OP_OK
    
    def upload_file(self,remote_path,local_path):
        if self.logined!=True:
            self.err_str=NOTLOGIN_ERRSTR
            return Sftp.NOT_LOGINED
        
        cmd="put "+local_path+" "+remote_path
        try:
            if self.enable_progress():
                self.sendline(cmd)
                self.expect("100%",3)
            else:
                return Sftp.UPLOAD_ERROR
        except pexpect.TIMEOUT:
            return Sftp.UPLOAD_ERROR
        return Sftp.OP_OK
    
    def backup_file(self,remote_path,local_path):
        if self.logined!=True:
            self.err_str=NOTLOGIN_ERRSTR
            return Sftp.NOT_LOGINED
        
        cmd="get "+remote_path+" "+local_path
        try:
            if self.enable_progress():
                self.sendline(cmd)
                self.expect("100%",3)
            else:
                return Sftp.BACKUP_ERROR 
        except pexpect.TIMEOUT:
            return Sftp.BACKUP_ERROR 
        return Sftp.OP_OK     
    
    
    def enable_progress(self):
        try:
            self.sendline("progress")
            i=self.expect(["disable","enable"])
            if i==0:
                self.sendline("progress")
                i=self.expect(["disable","enable"])
            if i==1:
                return True
        except pexpect.TIMEOUT:
            return False  
        return False
        
        
def main():
    client=Sftp()
    if 0==client.login("127.0.0.1","root","kvoing1"):
        if 0!=client.upload_file("/tmp/abc","/home/Joey/install.log"):
            print("fail")
    else:
        print("fail")

if __name__ == '__main__':
    main()
    print("sucess")