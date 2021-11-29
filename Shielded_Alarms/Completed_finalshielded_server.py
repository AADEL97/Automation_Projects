#######################################################################Importing Libraries###########################################################

from datetime import datetime , timedelta
import os
import numpy as np
import pandas as pd
import datetime
import paramiko
import socket, time
from ssh2.session import Session
import time
import re
import urllib.request

#########################################################################Regex pattern ############################################################

os.rename(r'MmlTaskResult',r'MmlTaskResult.txt')
data = []
site_name_data = []
alarms=[]
alarms_intro = []

with open("MmlTaskResult.txt",'r',errors="ignore") as f:
    file = f.read()
    for match1 in re.findall('\+\+\+.+\n.+\n.+\n.+\n\n.+\n\n---\s\s\s\sEND',file):
        data.append(match1)
        
for i in range(len(data)):
    site_name=re.findall('\+\+\+\s\s\s\s.*\s\s',data[i])
    site_name_data.append(str(site_name).split(" ")[4])
    for match2 in re.findall('RETCODE.+\n\n.+\n\n---\s\s\s\sEND',data[i]):
        alarms_intro.append(match2)

for z in range(len(alarms_intro)):
    alarms.append(str(alarms_intro[z]).replace("RETCODE = 0  Operation succeeded.\n\n","").replace("\n\n---    END",""))

########################################################################Load data to data frame####################################################

df = pd.DataFrame(list(zip(site_name_data, alarms)),columns =['Site Name', 'Alarms',])
alarm_site=[]
alarm_alarm=[]
sep = ' , '
full_alarm = []
for g in range(df.shape[0]):
    if (df.iloc[g,1]!="No record exists"):
        alarm_site.append(df.iloc[g,0])
        alarm_alarm.append(df.iloc[g,1])
for i in range(len(alarm_site)):
    site=alarm_site[i]
    ala=alarm_alarm[i]
    conc=str(site)+" has Shielded alarm : "+str(ala)
    full_alarm.append(conc)
message=(sep.join(full_alarm))
##########################################################################Remote file transfer & raise alarm on system####################################
def sent_file_alam():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='#.#.#.#',username='####',password='####',port=22)
    sftp_client=ssh.open_sftp()
    sftp_client.put("‪alarm_python.txt".strip("\u202a"),'/home/aadel/Desktop/alarm_python.txt')
    sftp_client.close()
    ssh.close()
    ssh.close()

if (message!=""):
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
        "{}\n".format(message),
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
        time.sleep(5)
        channel.close()
    ######################################################################Send detected alarms by SMS##################################################

    phones=['015xxxxxxxx','015xxxxxxx']
    for a in range(len(phones)):
        Number = phones[a]
        Data = '{}'.format(message.replace(" ","%20"))
        url = """http://'#.#.#.#':9501/ozeki?action=sendmessage&username=We-Mobile&password=Mobile@1234&recipient={}&messageData={}""".format(Number,Data)
        urllib.request.urlopen(url)