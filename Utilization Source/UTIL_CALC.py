import UTIL_FILEACCESS
import pandas as pd

def calc_cumul(past_hrs, trgt, yest_hrs):
    cumul = past_hrs - trgt + yest_hrs
        
    return(cumul)

def trgt_hrs_perc(trgt_hrs):
    
    user_inp = UTIL_FILEACCESS.user_data()
    
    date_string = user_inp['TARGET_HOUR_OPERATING_HOURS']
    date_string = date_string.split(' - ')
        
    now_time = pd.to_datetime('today')
    
    beg_time = now_time
    beg_time = (str(beg_time)[0:10] + ' ' + date_string[0])
    beg_time = pd.to_datetime(beg_time)
    
    end_time = now_time
    end_time = (str(end_time)[0:10] + ' ' + date_string[1])
    end_time = pd.to_datetime(end_time)
    
    
    rest = now_time - beg_time
    
    if rest.total_seconds() > 0:
    
        time_difference = end_time - beg_time
    
        percent = rest.total_seconds() / time_difference.total_seconds()
        
        if percent <= 1:
            cur_trgt = float("{0:.2f}".format(trgt_hrs * percent))
        else:
            cur_trgt = trgt_hrs
        
    else:
        cur_trgt = 0.0
        
    return(cur_trgt)