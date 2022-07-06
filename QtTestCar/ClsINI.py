import configparser
import os


class Inifile:
    
    def __init__(self):
        
        self.config = configparser.ConfigParser()
        self.Inipath = 'temporary.ini'
        
    def InIfile_Set_Path(self,path):
        self.Inipath = path
    
    def InIfile_Exist(self,path):
        return os.path.exists(path)
    
    def InIfile_ReadValue(self,Section,Key):
        
        self.config.read(self.Inipath, encoding='utf-8')
        
        if Section in self.config.sections(): #섹션 존재여부
            
            if Key in self.config[Section].keys(): #키 존재 여부
                
                return self.config[Section][Key]
    
    def InIfile_ReadValue_Path(self,Section,Key,Path):
        
        if os.path.exists(Path):
            
            self.config.read(self.Inipath, encoding='utf-8')
        
            if Section in self.config.sections(): #섹션 존재여부
            
                if Key in self.config[Section].keys(): #키 존재 여부
                
                    return self.config[Section][Key]
                
    
    def InIfile_WriteValue(self,Section,Key,Value):
        
        self.config.read(self.Inipath, encoding='utf-8')
        
        if Section in self.config.sections(): #섹션 존재여부
            
            if Key in self.config[Section].keys(): #키 존재 여부
                
                self.config.set(Section,Key,Value)
                
            else:
                
                self.config[Section][Key] = Value  
                
        else:
            
            self.config.add_section(Section) #섹션 추가
            self.config[Section][Key] = Value
            
            
        
        with open(self.Inipath, 'w+') as configfile:
                    self.config.write(configfile)
            
    
        