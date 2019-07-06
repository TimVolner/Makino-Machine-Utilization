import sqlite3
import os
import pandas as pd

def build_util_table():
    
    # Set path names
    path = os.getcwd() + '\\DATA\\' 
    db_path = path + 'util.db'
    log_path = path + 'ERROR_LOG'
    
    # Create and connect to sqlite database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Create needed tables, MACH_UTIL and LIVE_UTIL
    try:
        
        c.execute('''CREATE TABLE MACH_UTIL(
        [DATE] TEXT PRIMARY KEY,
        [HOURS] float, 
        [TARGET_HOURS] float,
        [CUMUL_HOURS] float)'''
                  )

        c.execute('''CREATE TABLE LIVE_UTIL(
        [DATE] TEXT PRIMARY KEY,
        [HOURS] float, 
        [TARGET_HOURS] float,
        [CUMUL_HOURS] float)'''
                  )     
        
    except Exception as e:
        
        with open(log_path, 'a') as f:
            
            text = str(pd.to_datetime('today')) + ' - UTIL_2.py - '  + ' - build_util_table - ' + ' - ERROR:::: ' + str(e) + '\n'
            f.write(text)
    
    # Close sqlite database connection
    conn.commit()
    conn.close()

def save_day_util(data):
    
   # Set path names
    path = os.getcwd() + '\\DATA\\' 
    db_path = path + 'util.db'
    log_path = path + 'ERROR_LOG'
    
    # Create and connect to sqlite database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Add data to sqlite table, MACH_UTIL
    try:
        c.execute('''insert into MACH_UTIL values (?,?,?,?)''', data)

    except Exception as e:
        
        # Create and append error log
        with open(log_path, 'a') as f:
            
            text = str(pd.to_datetime('today')) + ' - UTIL_2.py - '  + ' - save_day_util - ' + ' - ERROR:::: ' + str(e) + '\n'
            f.write(text)  
    
    # Close sqlite databaase connection
    conn.commit()
    conn.close()     

def save_live_util(data):
    
   # Set path names
    path = os.getcwd() + '\\DATA\\' 
    db_path = path + 'util.db'
    log_path = path + 'ERROR_LOG'
    
    # Create and connect to sqlite database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Add data to sqlite table, LIVE_UTIL
    try:
        c.execute('''insert into LIVE_UTIL values (?,?,?,?)''', data)

    except:
        
        # Create and append error log
        with open(log_path, 'a') as f:
            
            text = str(pd.to_datetime('today')) + ' - UTIL_2.py - '  + ' - save_day_util - ' + ' - ERROR:::: ' + str(e) + '\n'
            f.write(text)  
    
    # Close sqlite databaase connection
    conn.commit()
    conn.close()    

def past_cumul(yest_date):
    
    past_date = str(yest_date - pd.Timedelta('1 days'))[:10]
    
    # Set path names
    path = os.getcwd() + '\\DATA\\' 
    db_path = path + 'util.db'
    log_path = path + 'ERROR_LOG'

    # Create and connect to sqlite database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Pull data from table, MACH_UTIL, from two days ago
    try:
        c.execute('''SELECT CUMUL_HOURS FROM MACH_UTIL WHERE DATE = ?''', (past_date,))

    except Exception as e:

        # Create and append error log
        with open(log_path, 'a') as f:

            text = str(pd.to_datetime('today')) + ' - UTIL_2.py - '  + ' - save_day_util - ' + ' - ERROR:::: ' + str(e) + '\n'
            f.write(text)  
    
    # Pull past cumulative hours from database if they exist, otherwise set hours as 0
    try:
        
        past_cumul_hrs = c.fetchall()[0][0]
        
    except:
        
        past_cumul_hrs = 0
    
    # Close sqlite connection
    conn.commit()
    conn.close() 
    
    return(past_cumul_hrs)    

def yesterday_hours():
    
    # Set path names
    path = os.getcwd() + '\\DATA\\' 
    log_path = path + 'ERROR_LOG'    
    
    
    yesterdate = pd.to_datetime('today') - pd.Timedelta('1 days')
    recent = pd.to_datetime(str(pd.to_datetime('today'))[0:10] + ' 00:00:01.00')  
    
    yesterdate.strftime('%y%m%d')    
    compareDate = str(yesterdate)[0:10]
    
    try:    
        df = pd.read_csv((path + "MachineResults.csv"), sep='\t', encoding='utf-8')
    
        df_yesterday = df.loc[df['StartDateTime'].str[0:10] == compareDate]
        df_recent = df.loc[df['StartDateTime'] >= str(recent)]    
    
        total_yesterday = df_yesterday['SpindleTime'].sum() / 60
        total_recent = df_recent['SpindleTime'].sum() / 60
    
        total_yesterday = total_yesterday / 60    
        total_recent = total_recent / 60      
        
        return(yesterdate, total_yesterday, total_recent)        
    
    except Exception as e:
        
        # Create and append error log
        with open(log_path, 'a') as f:

            text = str(pd.to_datetime('today')) + ' - UTIL_2.py - '  + ' - save_day_util - ' + ' - ERROR:::: ' + str(e) + '\n'
            f.write(text)        
        
        return(None, None, None)
              
    