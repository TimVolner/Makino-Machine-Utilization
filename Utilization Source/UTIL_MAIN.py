import UTIL_SQLDBACCESS
import UTIL_FILEACCESS
import UTIL_CALC
import UTIL_SQLSERVACCESS
import pandas as pd

def START():    
    
    # Today's Date and Time
    today = pd.to_datetime('today')
    
    # Pull Machine Utilization Records
    UTIL_SQLSERVACCESS.main()
    
    # Build sqlite Database
    UTIL_SQLDBACCESS.build_util_table()
    
    # Read sqlite Database for utilization
    yest_date, day_util, recent_util = UTIL_SQLDBACCESS.yesterday_hours()

    # Get USER INPUT target hours
    user_inp = UTIL_FILEACCESS.user_data()
    # try to extract data from user input settings if available
    try:
        trgt_hrs = float(user_inp['TARGET_HOURS'])
            
    except:
        trgt_hrs = 1.0    
    
    if (yest_date is not None):
        
        # Calculate Past and Current Cumulative Hours
        past_cu_hrs = UTIL_SQLDBACCESS.past_cumul(yest_date)
        
    else:
        past_cu_hrs = 0.0
        
    cur_cu_hrs = UTIL_SQLDBACCESS.past_cumul(today)    
    
    if (day_util is None):
        day_util = 0.0
        
    cumul_hrs = UTIL_CALC.calc_cumul(past_cu_hrs, trgt_hrs, day_util)
    
        
    # Gather necessary data
    data = [str(yest_date)[0:10], day_util, trgt_hrs, cumul_hrs]
    
    
    # Save necessary data
    UTIL_SQLDBACCESS.save_day_util(data)    
        
       
    return(cur_cu_hrs)

def CONTINUE(past_cu_hrs):
    
    # Pull Machine Utilization Records
    UTIL_SQLSERVACCESS.main()    
    
    # Read sqlite Database for utilization
    yest_date, day_util, recent_util = UTIL_SQLDBACCESS.yesterday_hours()

    if (recent_util is None):    
        recent_util = 0.0
        
    # Round recent_util to two decimal places
    recent_util = float("{0:.2f}".format(recent_util))
    
    # Get USER INPUT target hours
    user_inp = UTIL_FILEACCESS.user_data()
    
    # try to extract data from user input settings if available
    try:
        trgt_hrs = float(user_inp['TARGET_HOURS'])
            
    except:
        trgt_hrs = 1.0    
    
        
    # Get target hour based on time of day and user settings
    current_trgt_hrs = UTIL_CALC.trgt_hrs_perc(trgt_hrs)
    
    # Round cumulative hours to two decimal places
    cumul_hrs = float("{0:.2f}".format(UTIL_CALC.calc_cumul(past_cu_hrs, current_trgt_hrs, recent_util))) 
    
    
    return(current_trgt_hrs, cumul_hrs, recent_util)     