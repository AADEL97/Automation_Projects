#########################################################################Importing libraries#################################################

import paramiko
import socket, time
import datetime
import os
from ssh2.session import Session
from zipfile import ZipFile
import pandas as pd
import numpy as np
import psycopg2
import os
import glob
import sys
import time

##################################################################Define DB connection########################################################

param_dic = {
    "host"      : "localhost",
    "database"  : "postgres",
    "user"      : "postgres",
    "password"  : "postgres"
}

def connect(params_dic):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        
       # print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1) 
    return conn
def single_insert(conn, insert_req):
    """ Execute a single INSERT request """
    cursor = conn.cursor()
    try:
        cursor.execute(insert_req)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    cursor.close()

###############################################################################################################################################
   
old=[]
new=[]
diff=[]
####################################################################List old alarms files#############################################################
remote_conn_pre_1 = paramiko.SSHClient()
remote_conn_pre_1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
remote_conn_pre_1.connect(hostname='#.#.#.#',username='######',password='#######',port=22)
remote_conn_1 = remote_conn_pre_1.invoke_shell()
remote_conn_1.send('su ossuser\n')
time.sleep(5)
remote_conn_1.send('#######\n')
time.sleep(5)
remote_conn_1.send('cd /export/home/sysm/opt/oss/server/var/fileint/fm/{}\n'.format(datetime.datetime.now().strftime("%Y%m%d")))
time.sleep(5)
remote_conn_1.send('ls 1>test19.txt\n')
time.sleep(5)
remote_conn_1.send('cd /home/ossuser\n')
time.sleep(5)
remote_conn_1.send('./test23.sh\n')
time.sleep(5)
time.sleep(5)
o = open(r'/home/ahmed/test19.txt','r')
for line in o:
    old.append(line.strip())
####################################################################List new alarms files#############################################################
time.sleep(1020)
remote_conn_pre_2 = paramiko.SSHClient()
remote_conn_pre_2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
remote_conn_pre_2.connect(hostname='#.#.#.#',username='sopuser',password='Changeme_123',port=22)
remote_conn_2 = remote_conn_pre_2.invoke_shell()
remote_conn_2.send('su ossuser\n')
time.sleep(5)
remote_conn_2.send('######\n')
time.sleep(5)
remote_conn_2.send('cd /export/home/sysm/opt/oss/server/var/fileint/fm/{}\n'.format(datetime.datetime.now().strftime("%Y%m%d")))
time.sleep(5)
remote_conn_2.send('ls 1>test19.txt\n')
time.sleep(5)
remote_conn_2.send('cd /home/ossuser\n')
time.sleep(5)
remote_conn_2.send('./test23.sh\n')
time.sleep(5)
time.sleep(5)
n = open(r'/home/ahmed/test19.txt','r')
for line in n:
    new.append(line.strip())
####################################################################Get new alarms files#############################################################
diff = list(set(old).symmetric_difference(set(new)))
for i in diff:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='#.#.#.#',username='######',password='######',port=22)
    sftp_client=ssh.open_sftp()
    sftp_client.get("/export/home/sysm/opt/oss/server/var/fileint/fm/{}/{}".format(datetime.datetime.now().strftime("%Y%m%d"),i),'/home/ahmed/alarm_tmp/{}'.format(i))
    sftp_client.close()
    ssh.close()
    ssh.close()


os.system("unzip '/home/ahmed/alarm_tmp/*.zip'")

remote_conn_1.close()
remote_conn_2.close()
####################################################################Load Data to data frame#############################################################
files = os.listdir()
first_df = pd.DataFrame()
for file in files:
     if file.endswith('-alarm-log-auto-1.csv'):
        first_df = first_df.append(pd.read_csv(file), ignore_index=True)
file_name = 'first_alarms.csv'
first_df.to_csv(file_name)
second_df=pd.read_csv('first_alarms.csv')
second_df['new_date'] = pd.to_datetime(second_df['OccurrenceTime'],dayfirst=True).dt.strftime('%Y-%m-%d %H:%M:%S ')
second_df.columns = second_df .columns.str.replace(' ','_')
####################################################################Inserting to DB#############################################################
conn = connect(param_dic)
for i in second_df.index:
    Alarm_Source=second_df['Alarm_Source'][i]
    AlarmName=second_df['AlarmName'][i]
    Severity=second_df['Severity'][i]
    new_date=second_df['new_date'][i]
    query = """INSERT INTO public."Alarms_HU"("Alarm_Source", "Alarm_Name", "Severity", "Date") VALUES ('%s','%s','%s','%s');"""%(Alarm_Source,AlarmName,Severity,new_date)
    single_insert(conn, query)
conn.close()

for file in os.listdir(r"/home/ahmed/alarm_tmp"):
    if file.endswith('.csv'):
        os.remove(file)
    elif  file.endswith('.zip'):
        os.remove(file)
print ('____________________________________________________')
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print ('____________________________________________________')
