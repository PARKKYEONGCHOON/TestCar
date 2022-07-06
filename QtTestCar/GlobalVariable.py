from ClsINI import *
from enum import Enum

diretory = os.path.dirname(os.path.abspath(__file__))
os.chdir(diretory)

class GlobalVariable:
    
    rootPath = diretory
    
    iniFile = Inifile()
    iniFile.InIfile_Set_Path('Setting.ini')
    
    FormSizeX = Inifile.InIfile_ReadValue(iniFile,'Setting','FormSizeX')
    FormSizeY = Inifile.InIfile_ReadValue(iniFile,'Setting','FormSizeY')
    CameraNum = Inifile.InIfile_ReadValue(iniFile,'Setting','cameranum')
    cameraX = Inifile.InIfile_ReadValue(iniFile,'Setting','cameraX')
    cameraY = Inifile.InIfile_ReadValue(iniFile,'Setting','cameraY')
    imagePath = Inifile.InIfile_ReadValue(iniFile,'Setting','imagePath')
    videoPath = Inifile.InIfile_ReadValue(iniFile,'Setting','videoPath')
    tempImagePath = Inifile.InIfile_ReadValue(iniFile,'Setting','tempImagePath')
    
    dbName = Inifile.InIfile_ReadValue(iniFile,'DB','dbName')
    TableName = Inifile.InIfile_ReadValue(iniFile,'DB','TableName')
    
    MIN_AREA = 80
    MIN_WIDTH = 2
    MIN_HEIGHT = 8
    MIN_RATIO = 0.25
    MAX_RATIO = 1.0
    MAX_DIAG_MULTIPLYER = 5 
    MAX_ANGLE_DIFF = 12.0 
    MAX_AREA_DIFF = 0.5 
    MAX_WIDTH_DIFF = 0.8
    MAX_HEIGHT_DIFF = 0.2
    MIN_N_MATCHED = 3
    PLATE_WIDTH_PADDING = 1.3
    PLATE_HEIGHT_PADDING = 1.5
    MIN_PLATE_RATIO = 3
    MAX_PLATE_RATIO = 10
    longest_idx, longest_text = -1, 0
    
    def __init__(self):
        pass
        
        
class enum(Enum):
    def __init__(self):
        super().__init__()
    