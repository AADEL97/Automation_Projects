###############################################################Importing libraries#####################################################
import urllib.request
import paramiko
import socket, time
from ssh2.session import Session
import re
import numpy as np

###############################################################Run Temprature Detection Command #########################################
remote_conn_pre = paramiko.SSHClient()
remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
remote_conn_pre.connect(hostname='#.#.#.#',username='#####',password='######',port=22)
remote_conn = remote_conn_pre.invoke_shell()
remote_conn.send('ssh Administrator@#.#.#.#\n')
time.sleep(5)
output1 = remote_conn.recv(1000)
remote_conn.send('#######\n')
time.sleep(5)
output2 = remote_conn.recv(1000)
remote_conn.send('ipmcget -t sensor -d list\n')
time.sleep(5)
output3 = remote_conn.recv(1000)
###############################################################Detect Temprature pattern###################################################
final = str(output3)
pattern = "\| Inlet Temp       \| \d{2}.\d{3}"
result = re.findall(pattern,final)
temp = str(result).split('| Inlet Temp       | ')
degree = int(float(temp[1].split("']")[0]))
##############################################################Send Warning SMS############################################################# 
if (degree > 30):
  Number = '201552155564'
  Data = 'Temprature%20at%20Mohandseen%20Mobile%20NOC%20Data%20Center%20:%20{}%20degree%20C'.format(degree)
  url = """http://'#.#.#.#':9501/ozeki?action=sendmessage&username=We-Mobile&password=Mobile@1234&recipient={}&messageData={}""".format(Number,Data)
  urllib.request.urlopen(url)
  time.sleep(10)
###############################################################Raise Warning Alarm##########################################################
def sent_file_alam():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='#.#.#.#',username='####',password='####',port=22)
    sftp_client=ssh.open_sftp()
    sftp_client.put("‪alarm_python.txt".strip("\u202a"),'/home/aadel/Desktop/alarm_python.txt')
    sftp_client.close()
    ssh.close()
    ssh.close()

if (degree > 30):
    alarm_num=np.random.randint(5065146)
    alarm_num=np.random.randint(5065146)
    now = time.localtime()
    time_string = time.strftime("%Y%m%d%H%M%S", now)
    file1 = open("alarm_python.txt","w") 
    L = ["%a\n",
         "-ObjectOfReference=SubNetwork=ONRM_ROOT_MO,SubNetwork=OssTest,ManagedElement=NOCTEST1\n",
         "-AlarmId={}\n".format(alarm_num),
        "-EventTime={}\n".format(time_string),
        "-EventTypeText=COMMUNICATIONS\n",
        "-RecordType=1\n",
        "-PerceivedSeverity=1\n",
        "-ProbableCause=2\n",
        "-AlarmNumber={}\n".format(alarm_num+1),
        "The Temprature at mohandseen Data Center is {} Degree C\n".format(degree),
        "%A"] 
    file1.writelines(L)
    file1.close()

    host = '#.#.#.#'
    user = '####'
    password = '####'
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((host,22))
    session = Session()
    session.handshake(sock)
    session.userauth_password(user,password)
    channel = session.open_session()
    channel.shell() 

    sock2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock2.connect((host,22))
    session2 = Session()
    session2.handshake(sock2)
    session2.userauth_password(user,password)
    channel2 = session2.open_session()

    record = 1
if (record==1):
        sent_file_alam()
        time.sleep(5)
        channel.write('''bash'''+'\n')
        time.sleep(5)
        channel.write('''smtool -coldrestart txf_VS_adapt_1 -reason=other -reasontext="other"'''+'\n')
        time.sleep(5)
        channel.write('''cat /home/aadel/Desktop/alarm_python.txt >> /etc/opt/ericsson/fm/txf/Process/txf_VS_adapt_1/Interface/AlarmReceptionFile1'''+'\n')
        channel2.execute('''cat /home/aadel/Desktop/alarm_python.txt >> /etc/opt/ericsson/fm/txf/Process/txf_VS_adapt_1/Interface/AlarmReceptionFile1''')
        time.sleep(5)
       
