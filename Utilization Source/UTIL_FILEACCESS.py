import os
import pandas as pd

def user_data():
    
    # Set variables including path where User Input Settings are stored.
    path = os.getcwd() + '\\DATA\\' 
    uis_path = path + 'USER_INPUT.txt'
    log_path = path + 'ERROR_LOG'
    line = 0
    user_input = {}
    
    # Read file for user settings
    try:
        with open(uis_path, 'r') as f:
            user_inp = f.read()
            user_inp = user_inp.replace('\n', ', ')
            user_inp = '{' + user_inp + '}'
            user_inp = eval(user_inp)
    
    except:
        # Create and append error log
        with open(log_path, 'a') as f:

            text = str(pd.to_datetime('today')) + ' - UTIL_2.py - '  + ' - save_day_util - ' + ' - ERROR:::: ' + str(e) + '\n'
            f.write(text)  
            
        
    
    return(user_inp)