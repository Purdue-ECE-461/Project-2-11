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

    #### Connection Established ####
    print("Connection Established")

    #### Execute query ####

    

    return cnx

if __name__ == "__main__":
    connect(0,0,0)