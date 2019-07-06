import UTIL_MAIN
import UTIL_SQLDBACCESS
import time
import pandas as pd
from datetime import datetime

past_cumulative = UTIL_MAIN.START()

while True:
    
    # Today's date in HH:MM:SS PM Format
    today = pd.to_datetime('today')
    today = str(today)[11:19]
    today = datetime.strptime(today, '%H:%M:%S')
    today = datetime.strftime(today, '%I:%M:%S %p')

    print("START", today)    
    
    trgt, cumul, util = UTIL_MAIN.CONTINUE(past_cumulative)
    
    UTIL_SQLDBACCESS.save_live_util([str(today), util, trgt, cumul])
    time.sleep(10)