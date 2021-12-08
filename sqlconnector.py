import sqlite3
from google.cloud import storage 
import pandas as pd
import numpy as np
from datetime import datetime
import mysql.connector
import sys

#### Establish Connetion ####

def connect(dbpass,dbhost,dbname):
    cnx = mysql.connector.connect(user='root', password='2pjHC9svdbauJxFw', host='35.229.85.24',
                                  database='registry')

    #### Connetion Established ####
    print("Connection Established")

    #### Execute query ####

    query1 = ("select ramp_up from package where id = 1")
    #query2 = ("insert into package values (id,\"test_package2\",2.0,2,3,4,5,6,7,8)")
    #cursor.execute(query2)
    cursor.execute(query1)
    #### Create dataframe from resultant table ####
    frame = pd.DataFrame(cursor.fetchall())
    frame.columns = [i[0] for i in cursor.description]

    

    return cnx

if __name__ == "__main__":
    connect(0,0,0)