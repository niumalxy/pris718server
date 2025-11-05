import paramiko

class ssh:
    def __init__(self, host: str, username: str, port: int = 22, password: str = None):
        if not port:
            port = 22
        # 建立连接
        self.trans = paramiko.Transport((host, port))
        self.trans.connect(username=username, password=password)

        # 将sshclient的对象的transport指定为以上的trans
        self.ssh = paramiko.SSHClient()
        self.ssh._transport = self.trans
        
    def __del__(self):
        self.close()
        
    def run_command(self, command: str):
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(command)
        return ssh_stdout.read().decode('utf-8')
    def close(self):
        self.trans.close()
def loginAndCommand(host: str, username: str, command: str, port: int = 22, password: str = None):

    #执行命令
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
    stdout = ssh_stdout.read()
    
    # 关闭连接
    trans.close()
    return stdout

if __name__ == "__main__":
    #print(login_and_command(host="10.10.82.215", username="root", password="Tongtech@123", command="nvidia-smi"))
    conn = ssh(host="10.10.82.215", username="root", password="Tongtech@123")
    print(conn.run_command(command="nvidia-smi --query-gpu=name,memory.used,memory.total --format=csv,noheader,nounits"))
    conn.close()

    