import cvlib as cv
from cvlib.object_detection import draw_bbox
import cv2
from ClsFile import *
from GlobalVariable import *


class Cam:

    def __init__(self):
        
        self.camNum = int(GlobalVariable.CameraNum);
        self.cap = self.cam_cap()
        self.videoStart = False
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.fcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        
        self.detectMode = False
        self.frame = None
        self.detectObject = []
        
    def cam_cap(self):
        
        tmpcap = cv2.VideoCapture(self.camNum)
        return tmpcap
        
    def cam_isOpen(self):
        
        if self.cap.isOpened():
            print("Cam Connect")
            return True
        else:
            print("Cam Connect Fail")
            return True
        
    def cam_capture(self):
        
        if self.cam_isOpen:
            ret, frame = self.cap.read()
            frame = cv2.flip(frame,1) # 좌우 대칭
            tmpframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            if ret:
                
                if self.detectMode:
                    
                    bbox, self.detectObject, conf = cv.detect_common_objects(tmpframe)
                    #print(bbox, label, conf)
                    drawframe = draw_bbox(tmpframe,bbox,self.detectObject,conf,write_conf=True)
                    return drawframe
                
            
                else:
                    
                    return tmpframe

                
        
    def cam_video_Save(self):
        
        i = 1
        date = File.get_Today()
        dir1 = GlobalVariable.videoPath
        File.make_foloder(dir1)
        dir2 = GlobalVariable.videoPath + "/" + date
        File.make_foloder(dir2)
        
        while True:
            
            Videopath = dir2 + "/" + str(i)+ ".avi"
            
            if not os.path.exists(Videopath):
                out = cv2.VideoWriter(Videopath, self.fcc, self.fps, (self.width, self.height),isColor=True) # 3 width, 4 height
                break
            else:
                i += 1
        
        while self.videoStart:
            
            if self.cam_isOpen:
                
                ret, frame = self.cap.read()
                frame = cv2.flip(frame,1) # 좌우 대칭
                
                if ret:
                    out.write(frame)

                
            else:
                print("Cam is Not Open")
        
        
    def cam_Image_Save(self,image):
        
        i = 1
            
        date = File.get_Today()
        dir1 = GlobalVariable.imagePath
        File.make_foloder(dir1)
        dir2 = GlobalVariable.imagePath + "/" + date
        File.make_foloder(dir2)
        
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        
        while True:
            
            imgpath = dir2 + "/" + str(i)+ ".png"
            
            if not os.path.exists(imgpath):
                cv2.imwrite(imgpath,image)
                break
            
            else:
                
                i += 1

    def cam_Image_Load(self,Path):
        
        try:
            
            img = cv2.imread(Path, cv2.IMREAD_COLOR)
            frame = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            resizeframe = cv2.resize(frame, dsize=(int(GlobalVariable.cameraX),int(GlobalVariable.cameraY)),interpolation=cv2.INTER_AREA)
            return resizeframe
        
        except:
            pass
    
    