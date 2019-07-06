import pandas as pd
import sqlalchemy
import os
import UTIL_FILEACCESS

def main():
    
    data = UTIL_FILEACCESS.user_data()
    path = os.getcwd() + '\\DATA\\' 
    log_path = path + 'ERROR_LOG'
    
    # MS SQL Server Config
    server = data['server']
    port = data['port']
    database = data['database']
    username = data['username']
    password = data['password']
    driver = data['driver']
    schema = data['schema']
    
    
    is_exist = True

    
    try:
        connection_str = f'mssql+pyodbc://{username}:{password}@{server}:{port}/{database}?driver={driver}'
        engine = sqlalchemy.create_engine(connection_str)
        
        a = 'MachineResults'

        query = (f'select * from {a};')
        
        df = pd.read_sql(query, engine)

        print("Finished Reading: ", a)
    
        df.to_csv((path + a + '.csv'), sep='\t', encoding='utf-8')
    
        engine.dispose()        
        
    except:
        is_exist = False        
     
    if not is_exist:  
        try:
            server = 'localhost'
            connection_str = f'mssql+pyodbc://{username}:{password}@{server}:{port}/{database}?driver={driver}'
            engine = sqlalchemy.create_engine(connection_str)
            
            a = 'MachineResults'
    
            query = (f'select * from {a};')
            df = pd.read_sql(query, engine)
    
            print("Finished Reading: ", a)
        
            df.to_csv((path + a + '.csv'), sep='\t', encoding='utf-8')
        
            engine.dispose()          
            
        except:
            is_exist = False
        
    
    if not is_exist:
        
        with open(log_path, 'a') as f:
            text = str(pd.to_datetime('today')) + ' - UTIL_2.py - '  + ' - build_util_table - ' + ' - ERROR:::: ' + 'UNABLE TO CONNECT TO SERVER' + '\n'
            f.write(text)
    