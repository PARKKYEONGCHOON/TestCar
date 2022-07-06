
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pymysql import NULL
import pytesseract
import PIL

import cvlib as cv
from cvlib.object_detection import draw_bbox

import GlobalVariable as Gv
import ClsFile as f
import os
import ClsCam as cam

plt.style.use('dark_background')

class ImageProcessing:
    
    def __init__(self):
        
        self.AutoSequence = 0
        self.AutoSequenceImage = None
        self.ProcessWhile = False
        self.img = None
        self.height = None
        self.width = None
        self.channel = None
        
        
        
        self.longest_idx, self.longest_text = -1, 0
       
        self.contours_dict = []
        self.possible_contours = []
        self.plate_chars = []
        self.plate_imgs = []
        self.plate_infos = []
        self.MophologyUse = False
        self.BlurUse = False
        self.CannyUse = False
        self.ThresholdUse = False
        self.ContourUse = False
        
        self.MophologyShape = None
        self.MophologyMode = None
        self.BlurMode = None
        self.ThreshMode = None
        self.AdaptMode = None
        self.ContourMode = None
        self.ContourMethod = None
        self.MopholX = None
        self.MopholY = None
        self.BlurX = None
        self.BlurY = None
        self.cannythresh1 = None
        self.cannythresh2 = None
        self.threshvalue = None
        self.maxvalue = None
        self.blocksize = None
        self.c = None
    
    def Image_Load(self,img):
        
        try:
            
            #img = cv2.imread(Path, cv2.IMREAD_COLOR)
            self.img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            self.img = cv2.resize(self.img,(800,600),interpolation= cv2.INTER_AREA)
            self.height, self.width, self.channel = self.img.shape
            return self.img
        
        except:
            pass
    
    def Image_gray(self,image):
        
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        #cv2.imshow('gray',gray)
        return gray
    
    def Image_Mophogolgy(self,image,MORPH_Shape,MORPH_MODE,kx,ky):
        
        if MORPH_Shape == 1:
            kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(kx,ky))
        elif MORPH_Shape == 2:
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(kx,ky))
        elif MORPH_Shape == 3:
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(kx,ky))
        else:
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(kx,ky))
            
            
        if MORPH_MODE == 1:
            Mophol_image = cv2.morphologyEx(image,cv2.MORPH_OPEN,kernel)
        elif MORPH_MODE == 2:
            Mophol_image = cv2.morphologyEx(image,cv2.MORPH_CLOSE,kernel)
        elif MORPH_MODE == 3:
            Mophol_image = cv2.morphologyEx(image,cv2.MORPH_GRADIENT,kernel)
        elif MORPH_MODE == 4:
            Mophol_image = cv2.morphologyEx(image,cv2.MORPH_TOPHAT,kernel)
        elif MORPH_MODE == 5:
            Mophol_image = cv2.morphologyEx(image,cv2.MORPH_BLACKHAT,kernel)
        else:
            Mophol_image = cv2.morphologyEx(image,cv2.MORPH_OPEN,kernel)
            
        return Mophol_image
    
    
    def Image_Blur(self, image, BlurMode, kx,ky):
        
        if BlurMode == 1:
            Blur_image = cv2.blur(image,(kx,ky))
        elif BlurMode == 2:
            Blur_image = cv2.GaussianBlur(image,(kx,ky),0)
        elif BlurMode == 3: #잡음제거에 효과적
            Blur_image = cv2.medianBlur(image,kx)
        elif BlurMode == 4: #잡음제거,가장자리 보존,속도가 느림
            Blur_image = cv2.bilateralFilter(image,9,75,75)
            
        return Blur_image
    
    def Image_CannyEdge(self,image, thre1, thre2):
        
        Canny_image = cv2.Canny(image,thre1,thre2)
        
        cv2.imshow('canny',Canny_image)
        
        return Canny_image
    
    
    def Image_thresh(self, image, thresh_Mode, Adapt_Mode, threshVal, MaxVal, blockSize, C):
        
        if thresh_Mode == 1:
            if Adapt_Mode == 1:
                Thresh_image = cv2.threshold(image, threshVal, MaxVal, cv2.THRESH_BINARY)
            elif Adapt_Mode == 2:
                Thresh_image = cv2.adaptiveThreshold(image, MaxVal, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize, C)
            elif Adapt_Mode == 3:
                Thresh_image = cv2.adaptiveThreshold(image, MaxVal, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize, C)    

        elif thresh_Mode == 2:
            
            if Adapt_Mode == 1:
                Thresh_image = cv2.threshold(image, threshVal, MaxVal, cv2.THRESH_BINARY_INV)
            elif Adapt_Mode == 2:
                Thresh_image = cv2.adaptiveThreshold(image, MaxVal, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, blockSize, C)
            elif Adapt_Mode == 3:
                Thresh_image = cv2.adaptiveThreshold(image, MaxVal, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, blockSize, C)    

        elif thresh_Mode == 3:
        
            if Adapt_Mode == 1:
                Thresh_image = cv2.threshold(image, threshVal, MaxVal, cv2.THRESH_TRUNC)
            elif Adapt_Mode == 2:
                Thresh_image = cv2.adaptiveThreshold(image, MaxVal, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_TRUNC, blockSize, C)
            elif Adapt_Mode == 3:
                Thresh_image = cv2.adaptiveThreshold(image, MaxVal, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_TRUNC, blockSize, C) 
            
        elif thresh_Mode == 4:
            
            if Adapt_Mode == 1:
                Thresh_image = cv2.threshold(image, threshVal, MaxVal, cv2.THRESH_TOZERO)
            elif Adapt_Mode == 2:
                Thresh_image = cv2.adaptiveThreshold(image, MaxVal, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_TOZERO, blockSize, C)
            elif Adapt_Mode == 3:
                Thresh_image = cv2.adaptiveThreshold(image, MaxVal, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_TOZERO, blockSize, C) 
            
            
        elif thresh_Mode == 5:
            
            if Adapt_Mode == 1:
                Thresh_image = cv2.threshold(image, threshVal, MaxVal, cv2.THRESH_TOZERO_INV)
            elif Adapt_Mode == 2:
                Thresh_image = cv2.adaptiveThreshold(image, MaxVal, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_TOZERO_INV, blockSize, C)
            elif Adapt_Mode == 3:
                Thresh_image = cv2.adaptiveThreshold(image, MaxVal, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_TOZERO_INV, blockSize, C)
        
        return Thresh_image
    
    def Image_Templete_Match(self,image,tempImage,mode):
        
        w,h = tempImage.shape[::-1]
        
        if mode == 1:
            res = cv2.matchTemplate(image,tempImage,cv2.TM_CCOEFF)
        elif mode == 2:
            res = cv2.matchTemplate(image,tempImage,cv2.TM_CCOEFF_NORMED)
        elif mode == 3:
            res = cv2.matchTemplate(image,tempImage,cv2.TM_CCORR)
        elif mode == 4:
            res = cv2.matchTemplate(image,tempImage,cv2.TM_CCORR_NORMED)
        elif mode == 5:
            res = cv2.matchTemplate(image,tempImage,cv2.TM_SQDIFF)
        elif mode == 6:
            res = cv2.matchTemplate(image,tempImage,cv2.TM_SQDIFF_NORMED)
        else:    
            res = cv2.matchTemplate(image,tempImage,cv2.TM_CCOEFF)
            
        min_Val, max_Val, min_Loc, max_Loc = cv2.minMaxLoc(res)
        
        if mode == 5 or mode == 6:
            top_left = min_Loc
        else:
            top_left = max_Loc
            
        bottom_right = (top_left[0] + w, top_left[1] + h)
        resImage = cv2.rectangle(image, top_left, bottom_right, 255, 2) 
    
    def templete_Image_Save(self):
        
        date = f.File.get_Today()
        dir1 = Gv.GlobalVariable.tempImagePath
        f.File.make_foloder(dir1)
        dir2 = Gv.GlobalVariable.tempImagePath + "/" + date
        f.File.make_foloder(dir2)
        
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        
        
            
        imgpath = dir2 + "/" + "Templete.jpg"
            
        if not os.path.exists(imgpath):
            cv2.imwrite(imgpath,image)
        else:
            os.remove(imgpath)
            cv2.imwrite(imgpath,image)
        
    
    def templete_Image_Load(self):
        pass    
    
    def Image_countour(self, image,ContourMode,ContourMethod):
        
        #검색 방법Permalink
        #cv2.RETR_EXTERNAL : 외곽 윤곽선만 검출하며, 계층 구조를 구성하지 않습니다.
        #cv2.RETR_LIST : 모든 윤곽선을 검출하며, 계층 구조를 구성하지 않습니다.
        #cv2.RETR_CCOMP : 모든 윤곽선을 검출하며, 계층 구조는 2단계로 구성합니다.
        #cv2.RETR_TREE : 모든 윤곽선을 검출하며, 계층 구조를 모두 형성합니다. (Tree 구조)

        #근사화 방법Permalink
        #cv2.CHAIN_APPROX_NONE : 윤곽점들의 모든 점을 반환합니다.
        #cv2.CHAIN_APPROX_SIMPLE : 윤곽점들 단순화 수평, 수직 및 대각선 요소를 압축하고 끝점만 남겨 둡니다.
        #cv2.CHAIN_APPROX_TC89_L1 : 프리먼 체인 코드에서의 윤곽선으로 적용합니다.
        #cv2.CHAIN_APPROX_TC89_KCOS : 프리먼 체인 코드에서의 윤곽선으로 적용합니다.
        
        if ContourMode == 1:
            
            if ContourMethod == 1:
                contours, hi = cv2.findContours(image, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
            elif ContourMethod == 2:
                contours, hi = cv2.findContours(image, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            elif ContourMethod == 3:
                contours, hi = cv2.findContours(image, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_TC89_L1)
            elif ContourMethod == 4:
                contours, hi = cv2.findContours(image, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_TC89_KCOS)
                
        elif ContourMode == 2:
            
            if ContourMethod == 1:
                contours, hi = cv2.findContours(image, cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
            elif ContourMethod == 2:
                contours, hi = cv2.findContours(image, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
            elif ContourMethod == 3:
                contours, hi = cv2.findContours(image, cv2.RETR_LIST,cv2.CHAIN_APPROX_TC89_L1)
            elif ContourMethod == 4:
                contours, hi = cv2.findContours(image, cv2.RETR_LIST,cv2.CHAIN_APPROX_TC89_KCOS)
                
        elif ContourMode == 3:
            
            if ContourMethod == 1:
                contours, hi = cv2.findContours(image, cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)
            elif ContourMethod == 2:
                contours, hi = cv2.findContours(image, cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
            elif ContourMethod == 3:
                contours, hi = cv2.findContours(image, cv2.RETR_CCOMP,cv2.CHAIN_APPROX_TC89_L1)
            elif ContourMethod == 4:
                contours, hi = cv2.findContours(image, cv2.RETR_CCOMP,cv2.CHAIN_APPROX_TC89_KCOS)
                
        elif ContourMode == 4:
             
            if ContourMethod == 1:
                contours, hi = cv2.findContours(image, cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
            elif ContourMethod == 2:
                contours, hi = cv2.findContours(image, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            elif ContourMethod == 3:
                contours, hi = cv2.findContours(image, cv2.RETR_TREE,cv2.CHAIN_APPROX_TC89_L1)
            elif ContourMethod == 4:
                contours, hi = cv2.findContours(image, cv2.RETR_TREE,cv2.CHAIN_APPROX_TC89_KCOS)
        
        
        Contours_image = cv2.drawContours(image, contours, -1, (0, 255, 0))
        temp_result = np.zeros((self.height, self.width, self.channel), dtype=np.uint8)
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(temp_result, pt1=(x, y), pt2=(x+w, y+h), 
                    color=(255, 255, 255), thickness=2)
        
        
            self.contours_dict.append({
                'contour': contour,
                'x': x,
                'y': y,
                'w': w,
                'h': h,
                'cx': x + (w / 2),
                'cy': y + (h / 2)
            })
            
        cv2.imshow("Contours_image",Contours_image)
        cv2.imshow("temp_result",temp_result)
            
        return Contours_image, temp_result, self.contours_dict
    
    
    def Image_countour_sort(self, image, listContour):

        count = 0
        
        for d in listContour:
            area = d['w'] * d['h']
            ratio = d['w'] / d['h']
    
            if area > float(Gv.GlobalVariable.MIN_AREA) \
                    and d['w'] > float(Gv.GlobalVariable.MIN_WIDTH) and d['h'] > float(Gv.GlobalVariable.MIN_HEIGHT) \
                    and float(Gv.GlobalVariable.MIN_RATIO) < ratio < float(Gv.GlobalVariable.MAX_RATIO):
                d['idx'] = count
                count += 1
                self.possible_contours.append(d)
        
        temp_result = np.zeros((self.height, self.width, self.channel), dtype=np.uint8)

        for d in self.possible_contours:
    
            cv2.rectangle(temp_result, pt1=(d['x'], d['y']), pt2=(d['x']+d['w'], d['y']+d['h']), 
                  color=(255, 255, 255), thickness=2)
        
        cv2.imshow('possible_contours',temp_result)
        
        
        return self.possible_contours, temp_result
    
    
    def find_chars(self,contour_list):
        matched_result_idx = []

        
        for d1 in contour_list:
            matched_contours_idx = []
            for d2 in contour_list:
                if d1['idx'] == d2['idx']:
                    continue

                dx = abs(d1['cx'] - d2['cx'])
                dy = abs(d1['cy'] - d2['cy'])

                diagonal_length1 = np.sqrt(d1['w'] ** 2 + d1['h'] ** 2)

                distance = np.linalg.norm(np.array([d1['cx'], d1['cy']]) - np.array([d2['cx'], d2['cy']]))
                if dx == 0:
                    angle_diff = 90
                else:
                    angle_diff = np.degrees(np.arctan(dy / dx))
                area_diff = abs(d1['w'] * d1['h'] - d2['w'] * d2['h']) / (d1['w'] * d1['h'])
                width_diff = abs(d1['w'] - d2['w']) / d1['w']
                height_diff = abs(d1['h'] - d2['h']) / d1['h']

                if distance < diagonal_length1 * float(Gv.GlobalVariable.MAX_DIAG_MULTIPLYER) \
                and angle_diff < float(Gv.GlobalVariable.MAX_ANGLE_DIFF) and area_diff < float(Gv.GlobalVariable.MAX_AREA_DIFF) \
                and width_diff < float(Gv.GlobalVariable.MAX_WIDTH_DIFF) and height_diff < float(Gv.GlobalVariable.MAX_HEIGHT_DIFF):
                    matched_contours_idx.append(d2['idx'])

            matched_contours_idx.append(d1['idx'])

            if len(matched_contours_idx) < float(Gv.GlobalVariable.MIN_N_MATCHED):
                continue

            matched_result_idx.append(matched_contours_idx)

            unmatched_contour_idx = []
            for d4 in contour_list:
                if d4['idx'] not in matched_contours_idx:
                    unmatched_contour_idx.append(d4['idx'])

            unmatched_contour = np.take(self.possible_contours, unmatched_contour_idx)
                
            recursive_contour_list = self.find_chars(unmatched_contour)
                
            for idx in recursive_contour_list:
                matched_result_idx.append(idx)

            break

        return matched_result_idx
        
       
    
    def find_match(self, result_idx):
        matched_result = []
        
        for idx_list in result_idx:
            matched_result.append(np.take(self.possible_contours, idx_list))

        temp_result = np.zeros((self.height, self.width, self.channel), dtype=np.uint8)

        for r in matched_result:
            for d in r:

                cv2.rectangle(temp_result, pt1=(d['x'], d['y']), 
                      pt2=(d['x']+d['w'], d['y']+d['h']), 
                      color=(255, 255, 255), thickness=2)
                
        cv2.imshow('match',temp_result)
        
                
        return matched_result, temp_result
    
    
    def find_cropp(self, matched_result,img_thresh):
        
        for i, matched_chars in enumerate(matched_result):
            sorted_chars = sorted(matched_chars, key=lambda x: x['cx'])

            plate_cx = (sorted_chars[0]['cx'] + sorted_chars[-1]['cx']) / 2
            plate_cy = (sorted_chars[0]['cy'] + sorted_chars[-1]['cy']) / 2

            plate_width = (sorted_chars[-1]['x'] + sorted_chars[-1]['w'] - sorted_chars[0]['x']) * float(Gv.GlobalVariable.PLATE_WIDTH_PADDING)

            sum_height = 0
            for d in sorted_chars:
                sum_height += d['h']

            plate_height = int(sum_height / len(sorted_chars) * float(Gv.GlobalVariable.PLATE_HEIGHT_PADDING))

            triangle_height = sorted_chars[-1]['cy'] - sorted_chars[0]['cy']
            triangle_hypotenus = np.linalg.norm(
                np.array([sorted_chars[0]['cx'], sorted_chars[0]['cy']]) - 
                np.array([sorted_chars[-1]['cx'], sorted_chars[-1]['cy']])
            )

            angle = np.degrees(np.arcsin(triangle_height / triangle_hypotenus))

            rotation_matrix = cv2.getRotationMatrix2D(center=(plate_cx, plate_cy), angle=angle, scale=1.0)

            img_rotated = cv2.warpAffine(img_thresh, M=rotation_matrix, dsize=(self.width, self.height))

            img_cropped = cv2.getRectSubPix(
                img_rotated, 
                patchSize=(int(plate_width), int(plate_height)), 
                center=(int(plate_cx), int(plate_cy))
            )

            if img_cropped.shape[1] / img_cropped.shape[0] < float(Gv.GlobalVariable.MIN_PLATE_RATIO) or img_cropped.shape[1] / img_cropped.shape[0] < float(Gv.GlobalVariable.MIN_PLATE_RATIO) > float(Gv.GlobalVariable.MAX_PLATE_RATIO):
                continue

            self.plate_imgs.append(img_cropped)
            self.plate_infos.append({
                'x': int(plate_cx - plate_width / 2),
                'y': int(plate_cy - plate_height / 2),
                'w': int(plate_width),
                'h': int(plate_height)
            })
            
        cam.Cam.cam_Image_Save(cam.Cam.cam_cap,self.plate_imgs[0])
        self.result_Plate_Save(self.plate_imgs[0])
            
        
        cv2.imshow('plate_imgs', self.plate_imgs[0])
            
        return self.plate_imgs, img_cropped



    def findOCR(self, plate_imgs):
        
        
        for i, plate_img in enumerate(plate_imgs):
            plate_img = cv2.resize(plate_img, dsize=(0, 0), fx=1.6, fy=1.6)
            _, plate_img = cv2.threshold(plate_img, thresh=0.0, maxval=255.0, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        
            contours, _= cv2.findContours(plate_img,mode=cv2.RETR_LIST,method=cv2.CHAIN_APPROX_SIMPLE)
            plate_min_x, plate_min_y = plate_img.shape[1], plate_img.shape[0]
            plate_max_x, plate_max_y = 0, 0
            
            print(contours)

            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                
                area = w * h
                ratio = w / h

                if area > int(Gv.GlobalVariable.MIN_AREA) \
                and w > int(Gv.GlobalVariable.MIN_WIDTH) and h > int(Gv.GlobalVariable.MIN_HEIGHT) \
                and float(Gv.GlobalVariable.MIN_RATIO) < ratio < float(Gv.GlobalVariable.MAX_RATIO):
                    if x < plate_min_x:
                        plate_min_x = x
                    if y < plate_min_y:
                        plate_min_y = y
                    if x + w > plate_max_x:
                        plate_max_x = x + w
                    if y + h > plate_max_y:
                        plate_max_y = y + h
                        
            img_result = plate_img[plate_min_y:plate_max_y, plate_min_x:plate_max_x]
            
            img_result = cv2.GaussianBlur(img_result, ksize=(3, 3), sigmaX=0)
            _, img_result = cv2.threshold(img_result, thresh=0.0, maxval=255.0, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            img_result = cv2.copyMakeBorder(img_result, top=10, bottom=10, left=10, right=10, borderType=cv2.BORDER_CONSTANT, value=(0,0,0))

            chars = pytesseract.image_to_string(img_result, lang='kor', config='--psm 7 --oem 0')
            
            result_chars = ''
            has_digit = False
            for c in chars:
                if ord('가') <= ord(c) <= ord('힣') or c.isdigit():
                    if c.isdigit():
                        has_digit = True
                    result_chars += c
            
            print(result_chars)
            self.plate_chars.append(result_chars)

            if has_digit and len(result_chars) > self.longest_text:
                self.longest_idx = i


        info = self.plate_infos[self.longest_idx]
        chars = self.plate_chars[self.longest_idx]

        print(chars)

        img_out = self.img.copy()

        cv2.rectangle(img_out, pt1=(info['x'], info['y']), pt2=(info['x']+info['w'], info['y']+info['h']), color=(255,0,0), thickness=2)
        
        return img_out, chars
        
    def result_Plate_Save(self,image):
        
        date = f.File.get_Today()
        dir1 = Gv.GlobalVariable.imagePath
        f.File.make_foloder(dir1)
        dir2 = Gv.GlobalVariable.imagePath + "/" + date
        f.File.make_foloder(dir2)
        
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        
        imgpath = dir2 + "/temp.png"
            
        if not os.path.exists(imgpath):
            cv2.imwrite(imgpath,image)   
        else:
            os.remove(imgpath)   
            cv2.imwrite(imgpath,image)
            
    def result_Plate_Load(self):
        
        date = f.File.get_Today()
        dir1 = Gv.GlobalVariable.imagePath
        f.File.make_foloder(dir1)
        dir2 = Gv.GlobalVariable.imagePath + "/" + date
        f.File.make_foloder(dir2)
        
        imgpath = dir2 + "/temp.png"
            
        if os.path.exists(imgpath):
            image = cv2.imread(imgpath)   
        
            
        return image
               
    def AutoProcessing(self, image):
        
        cv2.destroyAllWindows()
        self.ProcessWhile = True
        
        try:
        
            while self.ProcessWhile:
            
                if self.AutoSequence == 0: #이미지 블러와
                    
                    self.AutoSequenceImage = self.Image_Load(image)
                    originImage = self.AutoSequenceImage # 원본 저장
                    cv2.imshow('Load',self.AutoSequenceImage)
                    self.AutoSequence += 1
                
                elif self.AutoSequence == 1: #그레이 변환
                    
                    self.AutoSequenceImage = self.Image_gray(self.AutoSequenceImage)
                    cv2.imshow('Gray',self.AutoSequenceImage)
                    self.AutoSequence += 1
                    
                    #CarNumber = pytesseract.image_to_string(self.AutoSequenceImage, lang='kor', config='--psm 7 --oem 0')
                    #print(CarNumber)
                        
                elif self.AutoSequence == 2: #모폴로지
                    
                    if bool(self.MophologyUse):
                    
                        self.AutoSequenceImage = self.Image_Mophogolgy(self.AutoSequenceImage,self.MophologyShape,self.MophologyMode,self.MopholX,self.MopholY)
                        cv2.imshow('Mophogy',self.AutoSequenceImage)
                        
                    self.AutoSequence += 1
                
                elif self.AutoSequence == 3: #블러    
                    
                    if bool(self.BlurUse):
                        
                        self.AutoSequenceImage = self.Image_Blur(self.AutoSequenceImage,self.BlurMode,self.BlurX,self.BlurY)
                        cv2.imshow('Blur',self.AutoSequenceImage)
                        
                    self.AutoSequence += 1
                
                elif self.AutoSequence == 4: #캐니
                    
                    if bool(self.CannyUse):
                        
                        self.AutoSequenceImage = self.Image_CannyEdge(self.AutoSequenceImage,self.cannythresh1,self.cannythresh2)
                        cv2.imshow('Canny',self.AutoSequenceImage) 
                        
                    self.AutoSequence += 1
                
                elif self.AutoSequence == 5: #쓰레쉬    
                    
                    if bool(self.ThresholdUse):
                        
                        self.AutoSequenceImage = self.Image_thresh(self.AutoSequenceImage,self.ThreshMode,self.AdaptMode,self.threshvalue,self.maxvalue,self.blocksize,self.c)
                        cv2.imshow('THRESH',self.AutoSequenceImage)
                        
                    self.AutoSequence += 1
                    
                elif self.AutoSequence == 6: #컨투어
                    
                    if bool(self.ContourUse):
                        
                        image,conBoximmge, condict = self.Image_countour(self.AutoSequenceImage,self.ContourMode,self.ContourMethod)
                
                        possible_contours, conBoximmge = self.Image_countour_sort(conBoximmge,condict)
                        
                        matched_result_idx = self.find_chars(possible_contours)
                
                        matchresult,b = self.find_match(matched_result_idx)
                
                        plate, cropped_image = self.find_cropp(matchresult,self.AutoSequenceImage)
                        
                        self.AutoSequence += 1
                        
                elif self.AutoSequence == 7: #OCR
                    
                    resImg,CarNumber=self.findOCR(plate)
                        
                    self.AutoSequence += 1
                
                elif self.AutoSequence == 8: #Reset
                    
                    self.ArrayReset()
                    self.AutoSequence = 0    
                    break
                    
            return resImg,CarNumber
        
        except Exception as e:
            
            print(e)
            self.ProcessWhile = False
            
    def ArrayReset(self):
        
        self.contours_dict = []
        self.possible_contours = []
        self.plate_chars = []
        self.plate_imgs = []
        self.plate_infos = []
        
    
    def DetectCar(self, image):
        car = 'car'
        tmpBox = []
        tmpObeject = []
        tmpconf = []
        bbox, detectObject, conf = cv.detect_common_objects(image)
        #print(bbox, detectObject, conf)
        
        if car in detectObject:
            for i in range(len(detectObject)):
                if detectObject[i] == car:
                    
                    tmpBox.append(bbox[i]) 
                    tmpObeject.append(detectObject[i]) 
                    tmpconf.append(conf[i]) 
                    
        #print(tmpBox)
        #print(tmpObeject)
        #print(tmpconf)
            
        drawframe = draw_bbox(image,tmpBox,tmpObeject,tmpconf,write_conf=True)
        return drawframe, tmpObeject
        
                
            
    
