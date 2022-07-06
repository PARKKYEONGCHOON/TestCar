from encodings import utf_8
import os
from datetime import datetime
import time


class log: 
    def __init__(self):
        
        self.logPath = 'temporary.log'
        
    def log_Set_Path(self,path):
        self.logPath = path
    
    def log_Exist(self,path):
        return os.path.exists(path)
       
    def log_Write(self,Message):
        
        logfile = open(self.logPath, 'a',encoding='utf-8')
        logfile.write("LOG : " + time.strftime("%Y-%m-%d-%X") + " __ " + Message +'\n')
        logfile.close()
        
        