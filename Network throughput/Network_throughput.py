#############################################################Importing Libraries########################################################################
 
import pandas as pd
import os
import psycopg2

#############################################################Load data & extract new added sites #######################################################

df1 = pd.read_csv("//home//ahmed//network_throughput//oldsite//throughput.csv")
df2 = pd.read_csv("//home//ahmed//network_throughput//newsite//throughput.csv")
df_all = df1.merge(df2.drop_duplicates(), on=['Date','Hour','Min','Downlink Throughput -Gbps','Uplink Throughput -Gbps'], 
                   how='right', indicator=True)

final_df = df_all[df_all['_merge']=='right_only']
final_df.drop(['_merge'], axis=1,inplace=True)

#############################################################Define DB connection##########################################################################

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
        
        print('Connecting to the PostgreSQL database...')
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
###############################################################Inserting to DB############################################################################

conn = connect(param_dic)
for i in final_df.index:
    Date=final_df['Date'][i]
    Hour=final_df['Hour'][i]
    Min=final_df['Min'][i]
    Downlink_Throughput_Gbps=final_df['Downlink Throughput -Gbps'][i]
    Uplink_Throughput_Gbps=final_df['Uplink Throughput -Gbps'][i]
    #query = """INSERT INTO public."CMM_hw_inventory_huawei"("NEName", "Board_Name", "Board_Type","Slot_No") VALUES ('%s','%s','%s','%s');""" % (NEName, Board_Name, Board_Type,Slot_No)
    query = """INSERT INTO public."Network_throughput"("Date", "Hour", "Min", "Downlink Throughput -Gbps", "Uplink Throughput -Gbps") VALUES ('%s','%s','%s','%s','%s');"""%(Date,Hour,Min,Downlink_Throughput_Gbps,Uplink_Throughput_Gbps)
    single_insert(conn, query)
conn.close()