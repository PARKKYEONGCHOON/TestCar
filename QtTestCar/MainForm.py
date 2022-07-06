
from time import sleep
from tkinter import Image

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import *
import sys
import cv2
from pymysql import NULL



from ClsCam import *
from GlobalVariable import *
from ClsSerial import *
from ClsCar import *
from ClsMysql import *
from ClsImageProcessing import *
from ClsINI import *
import ClsFile as f

diretory = os.path.dirname(os.path.abspath(__file__))
os.chdir(diretory)

class SerialMain(QWidget):
    
    def __init__(self):
        
        super().__init__()
        
        self.ReadRun = False
        self.Connect = False
        self.MovePress = False
        self.tmpSaveImage = None
        self.VideoSave = False
        self.detectObject = []
                   
        self.UI_init()
        self.Setting_Load()
        self.ImageProcessing_Setting_Load()
        self.setWindowTitle("Car Number Palate ")
        self.resize(int(GlobalVariable.FormSizeX),int(GlobalVariable.FormSizeY))
        self.setFixedSize(int(GlobalVariable.FormSizeX), int(GlobalVariable.FormSizeY))
        self.Center()
        self.show()
    
    def UI_init(self):
        
        lstport = []
        self.MainLayOut = QHBoxLayout()
        
        self.MainLetfLayOut = QVBoxLayout()
        self.MainRightLayOut = QVBoxLayout()
        self.MainCenterLayout = QVBoxLayout()
        
        self.MainCenterSubLayout = QVBoxLayout()
        self.MainRightSubLayout = QVBoxLayout()
        
        self.VLayOut2 = QVBoxLayout()
        self.VLayOut3 = QVBoxLayout()
        self.VLayOut4 = QHBoxLayout()
        
        self.VLayOut4Left = QVBoxLayout()
        self.VLayOut4RIGHT = QVBoxLayout()
        self.GLayOut4Btn = QGridLayout()
        self.VLayOut4Set1 = QVBoxLayout()
        self.HLayOutVide = QHBoxLayout()
        self.VLayOutText = QVBoxLayout()
        self.GLayOutCamera = QGridLayout()
        
        self.HLayOutSeriBtn = QHBoxLayout()
        self.VLayoutGrbSerial = QVBoxLayout()
        
        self.Laydetect = QVBoxLayout()
        self.LayImageProcessing = QVBoxLayout()
        
        self.LaydetectObject = QVBoxLayout()
        self.LaydetectImage = QVBoxLayout()
        self.LaydetectOCR = QVBoxLayout()
        self.LaySetting = QGridLayout()
        
        self.LayMophology = QGridLayout()
        self.LayMophologyShape = QGridLayout()
        self.LayMophologyMode = QGridLayout()
        self.LayMophologySize = QHBoxLayout()
        
        self.GrbVideo = QGroupBox("Display")
        self.GrbSerial = QGroupBox("Serial Comm")
        self.GrbBtn = QGroupBox("Move")
        self.GrbCamera = QGroupBox("CAMERA")
        
        self.GrbDetect = QGroupBox("Detect")
        self.GrbDetectImage = QGroupBox("Detect Image")
        self.GrbDetectObeject = QGroupBox("Detect Object")
        self.GrbDetectOCR = QGroupBox("Detect OCR")
        
        self.GrbETC = QGroupBox("SETTING")
        
        
        self.GrbImageProcessing = QGroupBox("Image Processing Setting")
        self.GrbMophology = QGroupBox("Mophology")
        self.GrbMophology_Shape = QGroupBox("Mophology_Shape")
        self.GrbMophology_Mode = QGroupBox("Mophology_Mode")
        self.GrbMophology_Size = QGroupBox("Mophology_Size")
        
        self.GrbBlur = QGroupBox("Blur")
        self.GrbCanny = QGroupBox("Canny")
        self.Grbthreshold = QGroupBox("Threshold")
        self.GrbCountour = QGroupBox("Countour")

        
        
        self.lblVideo = QLabel()
        self.lblVideo.setStyleSheet("background-Color : white")
        self.lblVideo.resize(int(GlobalVariable.cameraX),int(GlobalVariable.cameraY))
        self.lblDetectImage = QLabel()
        self.lblDetectImage.setStyleSheet("background-Color : white")
        self.lblVideo.resize(int(GlobalVariable.cameraX),int(GlobalVariable.cameraY))
        
        self.cbo_Port = QComboBox()
        self.cbo_BaudRate = QComboBox()
        lstport = serCom.serial_ports()
        self.cbo_Port.addItems(lstport)
        self.cbo_BaudRate.addItems(serCom.lst_BaudRate)
        
        self.btn_Connect = QPushButton("Connect")
        self.btn_ReadRun = QPushButton("Read Run")
        self.btn_Read = QPushButton("OneTime Read")
        self.btn_Write = QPushButton("Write")
        
        self.btn_Connect.clicked.connect(self.btn_Connect_Click)
        self.btn_ReadRun.clicked.connect(self.btn_ReadRun_Click)
        self.btn_Read.clicked.connect(self.btn_ReadClick)
        self.btn_Write.clicked.connect(self.btn_WriteClick)
        
        
        self.MoveBtnGroup = QButtonGroup()
        self.MoveBtnGroup.setExclusive(False)
        #self.MoveBtnGroup.buttonClicked[int].connect(self.MoveBtn_clicked)
        self.MoveBtnGroup.buttonPressed[int].connect(self.MoveBtn_clicked)
        self.MoveBtnGroup.buttonReleased[int].connect(self.MoveBtn_Released)
        
        buttonStraight = QPushButton("↑(W)")
        #buttonStraight.setCheckable(true)
        self.MoveBtnGroup.addButton(buttonStraight, 1)
        self.GLayOut4Btn.addWidget(buttonStraight,0,1)
        
        buttonBack = QPushButton("Break(S)")
        #buttonBack.setCheckable(true) ↓ ●
        self.MoveBtnGroup.addButton(buttonBack, 2)
        self.GLayOut4Btn.addWidget(buttonBack,2,1)
        
        buttonLeft = QPushButton("←(A)")
        #buttonLeft.setCheckable(true)
        self.MoveBtnGroup.addButton(buttonLeft, 3)
        self.GLayOut4Btn.addWidget(buttonLeft,1,0)
        
        buttonRight = QPushButton("→(D)")
        #buttonRight.setCheckable(true)
        self.MoveBtnGroup.addButton(buttonRight, 4)
        self.GLayOut4Btn.addWidget(buttonRight,1,2)
        
        self.GearBtnGroup = QButtonGroup()
        self.GearBtnGroup.setExclusive(False)
        self.GearBtnGroup.buttonClicked[int].connect(self.GearBtn_clicked)
        
        buttonR = QPushButton("R(G)")
        self.GearBtnGroup.addButton(buttonR, 1)
        self.GLayOut4Btn.addWidget(buttonR,0,3)
        
        buttonN = QPushButton("N(G)")
        self.GearBtnGroup.addButton(buttonN, 2)
        self.GLayOut4Btn.addWidget(buttonN,1,3)
        
        buttonD = QPushButton("D(G)")
        self.GearBtnGroup.addButton(buttonD, 3)
        self.GLayOut4Btn.addWidget(buttonD,2,3)
        
        self.btn_CamCapture = QPushButton("Image Grab")
        self.GLayOutCamera.addWidget(self.btn_CamCapture,0,0)
        self.btn_CamCapture.clicked.connect(self.btn_CamCapture_Clicked)
        self.btn_CamVideo = QPushButton("Video Start")
        self.GLayOutCamera.addWidget(self.btn_CamVideo,1,0)
        self.btn_CamVideo.clicked.connect(self.btn_CamVideo_Clicked)
        self.btn_Cam_Save = QPushButton("Image Save")
        self.GLayOutCamera.addWidget(self.btn_Cam_Save,0,1)
        self.btn_Cam_Save.clicked.connect(self.btn_Cam_Save_Clicked)
        self.btn_Cam_Load = QPushButton("Image Load")
        self.GLayOutCamera.addWidget(self.btn_Cam_Load,0,2)
        self.btn_Cam_Load.clicked.connect(self.btn_Cam_Load_Clicked)
        
        self.btn_carNumber = QPushButton("Detect OCR")
        #self.GLayOutCamera.addWidget(self.btn_carNumber,2,2)
        self.btn_carNumber.clicked.connect(self.btn_carNumberClick)
        
        self.chk_VideoSave = QCheckBox("Video Save")
        
        self.GLayOutCamera.addWidget(self.chk_VideoSave,1,1)
        self.chk_VideoSave.clicked.connect(self.chk_VideoSave_clicked)
        
        self.chk_ObjectDetect = QCheckBox("Object Detect")
        
        self.GLayOutCamera.addWidget(self.chk_ObjectDetect,1,2)
        self.chk_ObjectDetect.clicked.connect(self.chk_ObjectDetect_clicked)
        
        self.txtEdit_Read = QTextEdit()
        self.txtLine_Write = QLineEdit()
        self.txtEdit_Write = QTextEdit()
        self.txtEdit_Read.setEnabled(False)
        self.txtEdit_Write.setEnabled(False)
        
        self.txtLine_detectObject = QLineEdit()
        self.txtLine_detectObject.setEnabled(False)
        self.txtLine_detectObject.setStyleSheet("background-Color : white")
        
        self.txtLine_detectOCR = QLineEdit()
        self.txtLine_detectOCR.setEnabled(False)
        self.txtLine_detectOCR.setStyleSheet("background-Color : white")
       
        self.setLayout(self.MainLayOut)
        self.MainLayOut.addLayout(self.MainLetfLayOut,stretch=4)
        self.MainLayOut.addLayout(self.MainCenterLayout,stretch=2)
        self.MainLayOut.addLayout(self.MainRightLayOut,stretch=2)
        
        
        self.MainLetfLayOut.addLayout(self.VLayOut2,stretch=4)
        #self.MainLayOut.addLayout(self.VLayOut1,stretch=1)
        self.MainLetfLayOut.addLayout(self.VLayOut3,stretch=2)
        self.MainLetfLayOut.addLayout(self.VLayOut4,stretch=1)
        
        self.VLayOut4.addLayout(self.VLayOut4Left)
        self.VLayOut4.addLayout(self.VLayOut4RIGHT)
        
        self.HLayOutSeriBtn.addWidget(self.cbo_Port)
        self.HLayOutSeriBtn.addWidget(self.cbo_BaudRate)
        self.HLayOutSeriBtn.addWidget(self.btn_Connect)
        self.HLayOutSeriBtn.addWidget(self.btn_ReadRun)
        self.HLayOutSeriBtn.addWidget(self.btn_Read)
        self.HLayOutSeriBtn.addWidget(self.btn_Write)
        
        self.VLayOut2.addWidget(self.GrbVideo)
        
        self.VLayOut3.addWidget(self.GrbSerial)
        
        self.VLayOutText.addWidget(self.txtLine_Write)
        self.VLayOutText.addWidget(self.txtEdit_Write)
        self.VLayOutText.addWidget(self.txtEdit_Read)
        
        self.VLayOut4Left.addWidget(self.GrbBtn)
        self.VLayOut4RIGHT.addWidget(self.GrbCamera)
        self.GrbBtn.setLayout(self.GLayOut4Btn)
        self.GrbVideo.setLayout(self.HLayOutVide)
        self.HLayOutVide.addWidget(self.lblVideo)
        self.GrbCamera.setLayout(self.GLayOutCamera)
        
        self.GrbSerial.setLayout(self.VLayoutGrbSerial)
        self.VLayoutGrbSerial.addLayout(self.HLayOutSeriBtn)
        self.VLayoutGrbSerial.addLayout(self.VLayOutText)
        
        self.GearBtnGroup.button(1).setStyleSheet("background-Color : gray")
        self.GearBtnGroup.button(2).setStyleSheet("background-Color : yellow")
        self.GearBtnGroup.button(3).setStyleSheet("background-Color : gray")
        
        
        ######################################################################################
        
        self.MainCenterLayout.addLayout(self.MainCenterSubLayout)
        self.MainCenterSubLayout.addWidget(self.GrbDetect)
        self.MainCenterSubLayout.addWidget(self.GrbETC)
        
        self.GrbDetect.setLayout(self.Laydetect)
        self.Laydetect.addWidget(self.GrbDetectObeject,stretch=1)
        self.Laydetect.addWidget(self.GrbDetectImage,stretch=3)
        self.Laydetect.addWidget(self.GrbDetectOCR,stretch=2)
        
        self.GrbDetectObeject.setLayout(self.LaydetectObject)
        self.LaydetectObject.addWidget(self.txtLine_detectObject)
        
        self.GrbDetectImage.setLayout(self.LaydetectImage)
        self.LaydetectImage.addWidget(self.lblDetectImage)
        
        self.GrbDetectOCR.setLayout(self.LaydetectOCR)
        self.LaydetectOCR.addWidget(self.txtLine_detectOCR)
        self.LaydetectOCR.addWidget(self.btn_carNumber)
        
        self.GrbETC.setLayout(self.LaySetting)
        self.lbl_MIN_AREA = QLabel("MIN_AREA")
        self.txt_LineEdit_MIN_AREA = QLineEdit()
        self.txt_LineEdit_MIN_AREA.setAlignment(Qt.AlignRight)
        
        self.lbl_MIN_WIDTH = QLabel("MIN_WIDTH")
        self.txt_LineEdit_MIN_WIDTH = QLineEdit()
        self.txt_LineEdit_MIN_WIDTH.setAlignment(Qt.AlignRight)
        
        self.lbl_MIN_HEIGHT = QLabel("MIN_HEIGHT")
        self.txt_LineEdit_MIN_HEIGHT = QLineEdit()
        self.txt_LineEdit_MIN_HEIGHT.setAlignment(Qt.AlignRight)
        
        self.lbl_MIN_RATIO = QLabel("MIN_RATIO")
        self.txt_LineEdit_MIN_RATIO = QLineEdit()
        self.txt_LineEdit_MIN_RATIO.setAlignment(Qt.AlignRight)
        
        self.lbl_MAX_RATIO = QLabel("MAX_RATIO")
        self.txt_LineEdit_MAX_RATIO = QLineEdit()
        self.txt_LineEdit_MAX_RATIO.setAlignment(Qt.AlignRight)
        
        self.lbl_MAX_DIAG_MULTIPLYER = QLabel("MAX_DIAG_MULTIPLYER")
        self.txt_LineEdit_MAX_DIAG_MULTIPLYER = QLineEdit()
        self.txt_LineEdit_MAX_DIAG_MULTIPLYER.setAlignment(Qt.AlignRight)
        
        self.lbl_MAX_ANGLE_DIFF = QLabel("MAX_ANGLE_DIFF")
        self.txt_LineEdit_MAX_ANGLE_DIFF = QLineEdit()
        self.txt_LineEdit_MAX_ANGLE_DIFF.setAlignment(Qt.AlignRight)
        
        self.lbl_MAX_AREA_DIFF = QLabel("MAX_AREA_DIFF")
        self.txt_LineEdit_MAX_AREA_DIFF = QLineEdit()
        self.txt_LineEdit_MAX_AREA_DIFF.setAlignment(Qt.AlignRight)
        
        self.lbl_MAX_HEIGHT_DIFF = QLabel("MAX_HEIGHT_DIFF")
        self.txt_LineEdit_MAX_HEIGHT_DIFF = QLineEdit()
        self.txt_LineEdit_MAX_HEIGHT_DIFF.setAlignment(Qt.AlignRight)
        
        self.lbl_MIN_N_MATCHED = QLabel("MIN_N_MATCHED")
        self.txt_LineEdit_MIN_N_MATCHED = QLineEdit()
        self.txt_LineEdit_MIN_N_MATCHED.setAlignment(Qt.AlignRight)
        
        self.lbl_PLATE_WIDTH_PADDING = QLabel("PLATE_WIDTH_PADDING")
        self.txt_LineEdit_PLATE_WIDTH_PADDING = QLineEdit()
        self.txt_LineEdit_PLATE_WIDTH_PADDING.setAlignment(Qt.AlignRight)
        
        self.lbl_PLATE_HEIGHT_PADDING = QLabel("PLATE_HEIGHT_PADDING")
        self.txt_LineEdit_PLATE_HEIGHT_PADDING = QLineEdit()
        self.txt_LineEdit_PLATE_HEIGHT_PADDING.setAlignment(Qt.AlignRight)
        
        self.lbl_MIN_PLATE_RATIO = QLabel("MIN_PLATE_RATIO")
        self.txt_LineEdit_MIN_PLATE_RATIO = QLineEdit()
        self.txt_LineEdit_MIN_PLATE_RATIO.setAlignment(Qt.AlignRight)
        
        self.lbl_MAX_PLATE_RATIO = QLabel("MAX_PLATE_RATIO")
        self.txt_LineEdit_MAX_PLATE_RATIO = QLineEdit()
        self.txt_LineEdit_MAX_PLATE_RATIO.setAlignment(Qt.AlignRight)
        
        self.btn_Setting_Save = QPushButton("Setting Save")
        self.btn_Setting_Save.clicked.connect(self.btn_Setting_Save_Clickd)
        
        self.btn_ImageProcessing_Save = QPushButton("Image Processing Save")
        self.btn_ImageProcessing_Save.clicked.connect(self.btn_ImageProcessing_Setting_Save_Clickd)
        
        self.LaySetting.addWidget(self.lbl_MIN_AREA,0,0)
        self.LaySetting.addWidget(self.txt_LineEdit_MIN_AREA,0,1)
        
        self.LaySetting.addWidget(self.lbl_MIN_WIDTH,1,0)
        self.LaySetting.addWidget(self.txt_LineEdit_MIN_WIDTH,1,1)
        
        self.LaySetting.addWidget(self.lbl_MIN_HEIGHT,2,0)
        self.LaySetting.addWidget(self.txt_LineEdit_MIN_HEIGHT,2,1)
        
        self.LaySetting.addWidget(self.lbl_MIN_RATIO,3,0)
        self.LaySetting.addWidget(self.txt_LineEdit_MIN_RATIO,3,1)
        
        self.LaySetting.addWidget(self.lbl_MAX_RATIO,4,0)
        self.LaySetting.addWidget(self.txt_LineEdit_MAX_RATIO,4,1)
        
        self.LaySetting.addWidget(self.lbl_MAX_DIAG_MULTIPLYER,5,0)
        self.LaySetting.addWidget(self.txt_LineEdit_MAX_DIAG_MULTIPLYER,5,1)
        
        self.LaySetting.addWidget(self.lbl_MAX_ANGLE_DIFF,6,0)
        self.LaySetting.addWidget(self.txt_LineEdit_MAX_ANGLE_DIFF,6,1)
        
        self.LaySetting.addWidget(self.lbl_MAX_AREA_DIFF,7,0)
        self.LaySetting.addWidget(self.txt_LineEdit_MAX_AREA_DIFF,7,1)
        
        self.LaySetting.addWidget(self.lbl_MAX_HEIGHT_DIFF,8,0)
        self.LaySetting.addWidget(self.txt_LineEdit_MAX_HEIGHT_DIFF,8,1)
        
        self.LaySetting.addWidget(self.lbl_MIN_N_MATCHED,9,0)
        self.LaySetting.addWidget(self.txt_LineEdit_MIN_N_MATCHED,9,1)
        
        self.LaySetting.addWidget(self.lbl_PLATE_WIDTH_PADDING,10,0)
        self.LaySetting.addWidget(self.txt_LineEdit_PLATE_WIDTH_PADDING,10,1)
        
        self.LaySetting.addWidget(self.lbl_PLATE_HEIGHT_PADDING,11,0)
        self.LaySetting.addWidget(self.txt_LineEdit_PLATE_HEIGHT_PADDING,11,1)
        
        self.LaySetting.addWidget(self.lbl_MIN_PLATE_RATIO,12,0)
        self.LaySetting.addWidget(self.txt_LineEdit_MIN_PLATE_RATIO,12,1)
        
        self.LaySetting.addWidget(self.lbl_MAX_PLATE_RATIO,13,0)
        self.LaySetting.addWidget(self.txt_LineEdit_MAX_PLATE_RATIO,13,1)
        
        self.LaySetting.addWidget(self.btn_Setting_Save,14,0)
        self.LaySetting.addWidget(self.btn_ImageProcessing_Save,14,1)
        
        
        #############################################################
        self.MainRightLayOut.addLayout(self.MainRightSubLayout)
        self.MainRightSubLayout.addWidget(self.GrbImageProcessing)
        
        self.GrbImageProcessing.setLayout(self.LayImageProcessing)
        self.LayImageProcessing.addWidget(self.GrbMophology)
        self.GrbMophology.setLayout(self.LayMophology)
        
        self.chk_MophologyUse = QCheckBox("USE")
        self.chk_MophologyUse.clicked.connect(self.chk_MophologyUse_clicked)
        self.LayMophology.addWidget(self.chk_MophologyUse)
        self.LayMophology.addWidget(self.GrbMophology_Shape)
        self.LayMophology_Shape = QGridLayout()
        self.GrbMophology_Shape.setLayout(self.LayMophology_Shape)
        
        
        
        self.rbo_MORPH_CROSS = QRadioButton("MORPH_CROSS")
        self.rbo_MORPH_CROSS.clicked.connect(self.rdo_Mophology_shape_clicked)
        self.rbo_MORPH_RECT = QRadioButton("MORPH_RECT")
        self.rbo_MORPH_RECT.clicked.connect(self.rdo_Mophology_shape_clicked)
        self.rbo_MORPH_ELLIPSE = QRadioButton("MORPH_ELLIPSE")
        self.rbo_MORPH_ELLIPSE.clicked.connect(self.rdo_Mophology_shape_clicked)
        
        self.LayMophology_Shape.addWidget(self.rbo_MORPH_CROSS,0,0)
        self.LayMophology_Shape.addWidget(self.rbo_MORPH_RECT,0,1)
        self.LayMophology_Shape.addWidget(self.rbo_MORPH_ELLIPSE,0,2)
        
        self.LayMophology.addWidget(self.GrbMophology_Mode)
        self.LayMophology_Mode = QGridLayout()
        self.GrbMophology_Mode.setLayout(self.LayMophology_Mode)
        
        self.rbo_MORPH_OPEN = QRadioButton("MORPH_OPEN")
        self.rbo_MORPH_OPEN.clicked.connect(self.rdo_Mophology_Mode_clicked)
        self.rbo_MORPH_CLOSE = QRadioButton("MORPH_CLOSE")
        self.rbo_MORPH_CLOSE.clicked.connect(self.rdo_Mophology_Mode_clicked)
        self.rbo_MORPH_GRADIENT = QRadioButton("MORPH_GRADIENT")
        self.rbo_MORPH_GRADIENT.clicked.connect(self.rdo_Mophology_Mode_clicked)
        self.rbo_MORPH_TOPHAT = QRadioButton("MORPH_TOPHAT")
        self.rbo_MORPH_TOPHAT.clicked.connect(self.rdo_Mophology_Mode_clicked)
        self.rbo_MORPH_BLACKHAT = QRadioButton("MORPH_BLACKHAT")
        self.rbo_MORPH_BLACKHAT.clicked.connect(self.rdo_Mophology_Mode_clicked)
        
        self.LayMophology_Mode.addWidget(self.rbo_MORPH_OPEN,0,0)
        self.LayMophology_Mode.addWidget(self.rbo_MORPH_CLOSE,0,1)
        self.LayMophology_Mode.addWidget(self.rbo_MORPH_GRADIENT,0,2)
        self.LayMophology_Mode.addWidget(self.rbo_MORPH_TOPHAT,1,0)
        self.LayMophology_Mode.addWidget(self.rbo_MORPH_BLACKHAT,1,1)
        
        
        self.LayMophology.addWidget(self.GrbMophology_Size)
        self.LayMophology_Size = QHBoxLayout()
        self.GrbMophology_Size.setLayout(self.LayMophology_Size)
        self.lblMopholX = QLabel("X")
        self.txt_Line_MopholX = QLineEdit()
        self.txt_Line_MopholX.setAlignment(Qt.AlignRight)
        self.lblMopholY = QLabel("Y")
        self.txt_Line_MopholY = QLineEdit()
        self.txt_Line_MopholY.setAlignment(Qt.AlignRight)
        
        self.LayMophology_Size.addWidget(self.lblMopholX)
        self.LayMophology_Size.addWidget(self.txt_Line_MopholX)
        self.LayMophology_Size.addWidget(self.lblMopholY)
        self.LayMophology_Size.addWidget(self.txt_Line_MopholY)
        
        
        self.LayImageProcessing.addWidget(self.GrbBlur)
        self.LayBlur = QGridLayout()
        self.GrbBlur.setLayout(self.LayBlur)
        
        self.chk_BluryUse = QCheckBox("USE")
        self.chk_BluryUse.clicked.connect(self.chk_BluryUse_clicked)
        self.rbo_blur = QRadioButton("Blur")
        self.rbo_blur.clicked.connect(self.rdo_Blur_Mode_clicked)
        self.rbo_GaussianBlur = QRadioButton("GaussianBlur")
        self.rbo_GaussianBlur.clicked.connect(self.rdo_Blur_Mode_clicked)
        self.rbo_medianBlur = QRadioButton("MedianBlur")
        self.rbo_medianBlur.clicked.connect(self.rdo_Blur_Mode_clicked)
        self.rbo_bilateralFilter = QRadioButton("BilateralFilter")
        self.rbo_bilateralFilter.clicked.connect(self.rdo_Blur_Mode_clicked)
        
        self.lblBlurX = QLabel("Size X")
        self.txt_Line_BlurX = QLineEdit()
        self.txt_Line_BlurX.setAlignment(Qt.AlignRight)
        self.lblBlurY = QLabel("Size Y")
        self.txt_Line_BlurY = QLineEdit()
        self.txt_Line_BlurY.setAlignment(Qt.AlignRight)

        self.LayBlur.addWidget(self.chk_BluryUse,0,0)
        self.LayBlur.addWidget(self.rbo_blur,1,0)
        self.LayBlur.addWidget(self.rbo_GaussianBlur,1,1)
        self.LayBlur.addWidget(self.rbo_medianBlur,1,2)
        self.LayBlur.addWidget(self.rbo_bilateralFilter,1,3)
        
        self.LayBlur.addWidget(self.lblBlurX,2,0)
        self.LayBlur.addWidget(self.txt_Line_BlurX,2,1)
        self.LayBlur.addWidget(self.lblBlurY,2,2)
        self.LayBlur.addWidget(self.txt_Line_BlurY,2,3)
        
        
        self.LayImageProcessing.addWidget(self.GrbCanny)
        self.LayCanny = QGridLayout()
        self.GrbCanny.setLayout(self.LayCanny)
        
        self.chk_CannyUse = QCheckBox("USE")
        self.chk_CannyUse.clicked.connect(self.chk_CannyUse_clicked)
        self.lbl_thre1 = QLabel("Threshold 1")
        self.txt_Line_thre1 = QLineEdit()
        self.txt_Line_thre1.setAlignment(Qt.AlignRight)
        self.lbl_thre2 = QLabel("Threshold 2")
        self.txt_Line_thre2 = QLineEdit()
        self.txt_Line_thre2.setAlignment(Qt.AlignRight)
        
        self.LayCanny.addWidget(self.chk_CannyUse,0,0)
        self.LayCanny.addWidget(self.lbl_thre1,1,0)
        self.LayCanny.addWidget(self.txt_Line_thre1,1,1)
        self.LayCanny.addWidget(self.lbl_thre2,1,2)
        self.LayCanny.addWidget(self.txt_Line_thre2,1,3)
        
        self.LayImageProcessing.addWidget(self.Grbthreshold)
        self.Laythreshold = QVBoxLayout()
        self.Grbthreshold.setLayout(self.Laythreshold)
        self.chk_ThresholdUse = QCheckBox("USE")
        self.chk_ThresholdUse.clicked.connect(self.chk_ThresholdUse_clicked)
        self.Grb_ThreshMode = QGroupBox("ThreshMode")
        self.Grb_AdaptMode = QGroupBox("AdaptMode")
        self.Grb_ThreshVal = QGroupBox("Thresh Value && Max Value")
        self.Grb_ThreshSize = QGroupBox("Block Size && C")
        
    
        self.Laythreshold.addWidget(self.chk_ThresholdUse)
        
        self.Laythreshold.addWidget(self.Grb_ThreshMode)
        self.Lay_ThreshMode = QGridLayout()
        self.Grb_ThreshMode.setLayout(self.Lay_ThreshMode)
        self.rdo_THRESH_BINARY = QRadioButton("THRESH_BINARY")
        self.rdo_THRESH_BINARY.clicked.connect(self.rdo_Thresh_Mode_clicked)
        self.rdo_THRESH_BINARY_INV = QRadioButton("THRESH_BINARY_INV")
        self.rdo_THRESH_BINARY_INV.clicked.connect(self.rdo_Thresh_Mode_clicked)
        self.rdo_THRESH_TRUNC = QRadioButton("THRESH_TRUNC")
        self.rdo_THRESH_TRUNC.clicked.connect(self.rdo_Thresh_Mode_clicked)
        self.rdo_THRESH_TOZERO = QRadioButton("THRESH_TOZERO")
        self.rdo_THRESH_TOZERO.clicked.connect(self.rdo_Thresh_Mode_clicked)
        self.rdo_THRESH_TOZERO_INV = QRadioButton("THRESH_TOZERO_INV")
        self.rdo_THRESH_TOZERO_INV.clicked.connect(self.rdo_Thresh_Mode_clicked)
        
        self.Lay_ThreshMode.addWidget(self.rdo_THRESH_BINARY,0,0)
        self.Lay_ThreshMode.addWidget(self.rdo_THRESH_BINARY_INV,0,1)
        self.Lay_ThreshMode.addWidget(self.rdo_THRESH_TRUNC,0,2)
        self.Lay_ThreshMode.addWidget(self.rdo_THRESH_TOZERO,1,0)
        self.Lay_ThreshMode.addWidget(self.rdo_THRESH_TOZERO_INV,1,1)
        
        self.Laythreshold.addWidget(self.Grb_AdaptMode)
        self.Lay_ThresAdabtive = QGridLayout()
        self.Grb_AdaptMode.setLayout(self.Lay_ThresAdabtive)
        self.rdo_Threshold = QRadioButton("Threshold")
        self.rdo_Threshold.clicked.connect(self.rdo_Adapt_Mode_clicked)
        self.rdo_ADAPTIVE_THRESH_MEAN_C = QRadioButton("ADAPTIVE_MEAN")
        self.rdo_ADAPTIVE_THRESH_MEAN_C.clicked.connect(self.rdo_Adapt_Mode_clicked)
        self.rdo_ADAPTIVE_THRESH_GAUSSIAN_C = QRadioButton("ADAPTIVE_GAUSSIAN")
        self.rdo_ADAPTIVE_THRESH_GAUSSIAN_C.clicked.connect(self.rdo_Adapt_Mode_clicked)
        self.Lay_ThresAdabtive.addWidget(self.rdo_Threshold,0,0)
        self.Lay_ThresAdabtive.addWidget(self.rdo_ADAPTIVE_THRESH_MEAN_C,0,1)
        self.Lay_ThresAdabtive.addWidget(self.rdo_ADAPTIVE_THRESH_GAUSSIAN_C,0,2)
        
        
        self.Laythreshold.addWidget(self.Grb_ThreshVal)
        self.Lay_ThresVal = QGridLayout()
        self.Grb_ThreshVal.setLayout(self.Lay_ThresVal)
        self.lbl_Thresval = QLabel("Thresh Value")
        self.txt_LineThreVal = QLineEdit()
        self.txt_LineThreVal.setAlignment(Qt.AlignRight)
        self.lbl_Maxval = QLabel("Max Value")
        self.txt_LineMaxVal = QLineEdit()
        self.txt_LineMaxVal.setAlignment(Qt.AlignRight)
        self.Lay_ThresVal.addWidget(self.lbl_Thresval,0,0)
        self.Lay_ThresVal.addWidget(self.txt_LineThreVal,0,1)
        self.Lay_ThresVal.addWidget(self.lbl_Maxval,0,2)
        self.Lay_ThresVal.addWidget(self.txt_LineMaxVal,0,3)
        
        self.Laythreshold.addWidget(self.Grb_ThreshSize)
        self.ThreshSize = QGridLayout()
        self.Grb_ThreshSize.setLayout(self.ThreshSize)
        self.lbl_blockSize = QLabel("block size")
        self.txt_LineblockSize = QLineEdit()
        self.txt_LineblockSize.setAlignment(Qt.AlignRight)
        self.lbl_C = QLabel("C")
        self.txt_LineC = QLineEdit()
        self.txt_LineC.setAlignment(Qt.AlignRight)
        self.ThreshSize.addWidget(self.lbl_blockSize,0,0)
        self.ThreshSize.addWidget(self.txt_LineblockSize,0,1)
        self.ThreshSize.addWidget(self.lbl_C,0,2)
        self.ThreshSize.addWidget(self.txt_LineC,0,3)
        
        self.LayImageProcessing.addWidget(self.GrbCountour)
        self.LayCountour = QVBoxLayout()
        self.GrbCountour.setLayout(self.LayCountour)
        self.chk_ContourUse = QCheckBox("USE")
        self.chk_ContourUse.clicked.connect(self.chk_ContourUse_clicked)
        self.Grb_ContourMode = QGroupBox("ContourMode")
        self.Grb_ContourMethod = QGroupBox("ContourMethod")
        
        self.LayCountour.addWidget(self.chk_ContourUse)
        self.LayCountour.addWidget(self.Grb_ContourMode)
        self.LayContourMode = QGridLayout()
        self.Grb_ContourMode.setLayout(self.LayContourMode)
        self.rdo_RETR_EXTERNAL = QRadioButton("RETR_EXTERNAL")
        self.rdo_RETR_EXTERNAL.clicked.connect(self.rdo_Contour_Mode_clicked)
        self.rdo_RETR_LIST = QRadioButton("RETR_LIST")
        self.rdo_RETR_LIST.clicked.connect(self.rdo_Contour_Mode_clicked)
        self.rdo_RETR_CCOMP = QRadioButton("RETR_CCOMP")
        self.rdo_RETR_CCOMP.clicked.connect(self.rdo_Contour_Mode_clicked)
        self.rdo_RETR_TREE = QRadioButton("RETR_TREE")
        self.rdo_RETR_TREE.clicked.connect(self.rdo_Contour_Mode_clicked)
        
        self.LayContourMode.addWidget(self.rdo_RETR_EXTERNAL,0,0)
        self.LayContourMode.addWidget(self.rdo_RETR_LIST,0,1)
        self.LayContourMode.addWidget(self.rdo_RETR_CCOMP,1,0)
        self.LayContourMode.addWidget(self.rdo_RETR_TREE,1,1)
        
        self.LayCountour.addWidget(self.Grb_ContourMethod)
        self.LayContourMethod = QGridLayout()
        self.Grb_ContourMethod.setLayout(self.LayContourMethod)
        self.rdo_CHAIN_APPROX_NONE = QRadioButton("CHAIN_APPROX_NONE")
        self.rdo_CHAIN_APPROX_NONE.clicked.connect(self.rdo_Contour_Method_clicked)
        self.rdo_CHAIN_APPROX_SIMPLE = QRadioButton("CHAIN_APPROX_SIMPLE")
        self.rdo_CHAIN_APPROX_SIMPLE.clicked.connect(self.rdo_Contour_Method_clicked)
        self.rdo_CHAIN_APPROX_TC89_L1 = QRadioButton("CHAIN_APPROX_TC89_L1")
        self.rdo_CHAIN_APPROX_TC89_L1.clicked.connect(self.rdo_Contour_Method_clicked)
        self.rdo_CHAIN_APPROX_TC89_KCOS = QRadioButton("CHAIN_APPROX_TC89_KCOS")
        self.rdo_CHAIN_APPROX_TC89_KCOS.clicked.connect(self.rdo_Contour_Method_clicked)
        
        self.LayContourMethod.addWidget(self.rdo_CHAIN_APPROX_NONE,0,0)
        self.LayContourMethod.addWidget(self.rdo_CHAIN_APPROX_SIMPLE,0,1)
        self.LayContourMethod.addWidget(self.rdo_CHAIN_APPROX_TC89_L1,1,0)
        self.LayContourMethod.addWidget(self.rdo_CHAIN_APPROX_TC89_KCOS,1,1)
        
        
        
        
            
    def Center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def btn_Connect_Click(self):
        
        if self.Connect:
            self.Connect = False
            self.Connect = serCom.portClose()
            self.setDisplayReadText("DisConnect")
            self.btn_Connect.setText("Connect")
        else:
            self.Connect = True
            self.Connect = serCom.Connect(self.cbo_Port.currentText(),self.cbo_BaudRate.currentText())
            self.setDisplayReadText("Connect:" + str(self.Connect))
            self.btn_Connect.setText("DisConnect")
            #MoveWorker.start()
            
    def btn_ReadRun_Click(self):
        
        if self.Connect:
            if self.ReadRun:
                self.ReadRun = False
                self.btn_ReadRun.setText("Read Run")
                worker.RunSwitch = False
                worker.stop()
                
            else:
                self.ReadRun = True
                self.btn_ReadRun.setText("Read Stop")
                worker.RunSwitch = True
                worker.start()
        else:
            self.txtEdit_Read("Connect Afrer Run") 
    
    def btn_ReadClick(self):
        
        data = serCom.ReadSerial()
        self.txtEdit_Read.append(str(data))
    
    def btn_WriteClick(self):
        
        data = self.txtLine_Write.text()
        self.txtEdit_Write.append(data)
        self.txtLine_Write.clear()
        serCom.WriteEncodeSerial(data)
    
    def MoveBtn_clicked(self, id):
        
        testCar.direction = id
        
        if id == 2:
            testCar.Speed = 0
        else:
            testCar.Speed = 1
            
        MoveWorker.btnpressed = True
        MoveWorker.start()
    
    def MoveBtn_Released(self, id):
            
        MoveWorker.btnpressed = False
        testCar.Speed = 0
        #MoveWorker.stop()
    
    def GearBtn_clicked(self,id):
        
        self.SetGearBtnColor(id)
        testCar.Gear = id
    
    def keyPressEvent(self, e):
        
        if e.key() == Qt.Key_W:
            testCar.Speed = 1
            testCar.direction = 0
            MoveWorker.btnpressed = True
            MoveWorker.start()
            
        elif e.key() == Qt.Key_A:
            testCar.Speed = 1
            testCar.direction = 3
            MoveWorker.btnpressed = True
            MoveWorker.start()
            
        elif e.key() == Qt.Key_S:
            
            testCar.Speed = 0
            testCar.direction = 0
            MoveWorker.btnpressed = True
            MoveWorker.start()
        
        elif e.key() == Qt.Key_D:
            testCar.Speed = 1
            testCar.direction = 4
            MoveWorker.btnpressed = True
            MoveWorker.start()
            
            
        elif e.key() == Qt.Key_G:
            testCar.Gear += 1
            if testCar.Gear > 3:
                testCar.Gear = 1
            self.SetGearBtnColor(testCar.Gear)
            
    def keyReleaseEvent(self, e):
        
        if e.key() == Qt.Key_W:
            
            testCar.Speed = 0
            testCar.direction = 0
            MoveWorker.btnpressed = False
            MoveWorker.stop()
            
            
        elif e.key() == Qt.Key_A:
            
            testCar.Speed = 0
            testCar.direction = 0
            MoveWorker.btnpressed = False
            MoveWorker.stop()
           
            
        elif e.key() == Qt.Key_S:
            
            testCar.Speed = 0
            testCar.direction = 0
            MoveWorker.btnpressed = False
            MoveWorker.stop()
           
        
        elif e.key() == Qt.Key_D:
            
            testCar.Speed = 0
            testCar.direction = 0
            MoveWorker.btnpressed = False
            MoveWorker.stop()
            
    def btn_CamCapture_Clicked(self):
        
        self.ImageGrab()

    def btn_CamVideo_Clicked(self):
        
        if Cam.videoStart:
            
            Cam.videoStart = False
            self.btn_CamVideo.setText("Video Start")
            ImageWorker.videoThread = False
            ImageWorker.stop()
            
            if self.VideoSave:
                SaveWorker.stop()
            
        else:
            
            Cam.videoStart = True
            self.btn_CamVideo.setText("Video Stop")
            ImageWorker.videoThread = True
            ImageWorker.start()
            
            if self.VideoSave:
                SaveWorker.start()
            
    
    def btn_Cam_Save_Clicked(self):
        
        Cam.cam_Image_Save(self.tmpSaveImage)
    
    def btn_Cam_Load_Clicked(self):
        
        FileOpen = QFileDialog.getOpenFileName(self, 'Open file', './')
        FileName = FileOpen[0]
        tmpImage = Cam.cam_Image_Load(FileName)
        self.tmpSaveImage = tmpImage
        tmpImage = QImage(tmpImage.data, tmpImage.shape[1], tmpImage.shape[0], QImage.Format_RGB888)
        tmpPixmap = QPixmap(tmpImage)
        self.lblVideo.setPixmap(tmpPixmap)
       #self.lblVideo.resize(int(GlobalVariable.cameraX),int(GlobalVariable.cameraY))
        self.lblVideo.update()
        
        
    def setDisplayReadText(self,txt):
        self.txtEdit_Read.append(txt)
    
    def setDisplayWriteText(self,txt):
        self.txtEdit_Write.append(txt)
        
    def SetGearBtnColor(self,id):
        
        if(id == 1):
            self.GearBtnGroup.button(1).setStyleSheet("background-Color : yellow")
            self.GearBtnGroup.button(2).setStyleSheet("background-Color : gray")
            self.GearBtnGroup.button(3).setStyleSheet("background-Color : gray")
        elif(id == 2):
            self.GearBtnGroup.button(1).setStyleSheet("background-Color : gray")
            self.GearBtnGroup.button(2).setStyleSheet("background-Color : yellow")
            self.GearBtnGroup.button(3).setStyleSheet("background-Color : gray")
        elif(id == 3):
            self.GearBtnGroup.button(1).setStyleSheet("background-Color : gray")
            self.GearBtnGroup.button(2).setStyleSheet("background-Color : gray")
            self.GearBtnGroup.button(3).setStyleSheet("background-Color : yellow")

    def chk_VideoSave_clicked(self):
        
        
        if self.chk_VideoSave.isChecked():
            self.chk_VideoSave.setChecked(True)
            self.VideoSave = True
            
        else:
            self.chk_VideoSave.setChecked(False)
            self.VideoSave = False
    
    def chk_ObjectDetect_clicked(self):
        
        if self.chk_ObjectDetect.isChecked():
            self.chk_ObjectDetect.setChecked(True)
            Cam.detectMode = True
        else:
            self.chk_ObjectDetect.setChecked(False)
            Cam.detectMode = False
            
    
    def ImageGrab(self):
        
        tmpImage = Cam.cam_capture()
        self.tmpSaveImage = tmpImage
        tmpImage = QImage(tmpImage.data, tmpImage.shape[1], tmpImage.shape[0], QImage.Format_RGB888)
        tmpPixmap = QPixmap(tmpImage)
        self.lblVideo.setPixmap(tmpPixmap)
        self.lblVideo.update()
        
        if Cam.detectMode:
            time = f.File.get_TodayTime()
            #mySQL.MySQL_INSERT(GlobalVariable.TableName,'DATE',time)
            #mySQL.MySQL_INSERT(GlobalVariable.TableName,'RESULT',str(Cam.detectObject))
            mySQL.MySQL_INSERT2(GlobalVariable.TableName,'DATE','RESULT',time,str(Cam.detectObject))
        
    
    def btn_carNumberClick(self):
        
        try:
            
            image = self.tmpSaveImage
            image = imagePro.Image_Load(image)
            tmp = image.copy()
            
            tmp,tmpObject = imagePro.DetectCar(tmp)
            
            self.txtLine_detectObject.setText(tmpObject[0])
            
            tmpImage = QImage(tmp.data, tmp.shape[1], tmp.shape[0], QImage.Format_RGB888)
            tmpPixmap = QPixmap(tmpImage)
            self.lblVideo.resize(tmpPixmap.width(),tmpPixmap.height())
            self.lblVideo.setPixmap(tmpPixmap)
            self.lblVideo.update()   
            
            
            resImage,CarNumber = imagePro.AutoProcessing(image)
            
            self.txtLine_detectOCR.setText(CarNumber)
            
            tmpImage = imagePro.result_Plate_Load()
            tmpImage = QImage(tmpImage.data, tmpImage.shape[1], tmpImage.shape[0], QImage.Format_RGB888)
            tmpPixmap = QPixmap(tmpImage)
            self.lblDetectImage.resize(tmpPixmap.width(),tmpPixmap.height())
            self.lblDetectImage.setPixmap(tmpPixmap)
            self.lblDetectImage.update()
            
            tmpImage = QImage(resImage.data, resImage.shape[1], resImage.shape[0], QImage.Format_RGB888)
            tmpPixmap = QPixmap(tmpImage)
            self.lblVideo.resize(tmpPixmap.width(),tmpPixmap.height())
            self.lblVideo.setPixmap(tmpPixmap)
            self.lblVideo.update()   
            
        except Exception as e:
            #시퀀스 에러로 빠지면 초기화
            imagePro.AutoSequence = 0;
            imagePro.ArrayReset()
            print(e)
        
    
    def btn_Setting_Save_Clickd(self):
        
        self.Setting_Save()
    
    def btn_ImageProcessing_Setting_Save_Clickd(self):
        
        self.ImageProcessing_Setting_Save()
    
    def Setting_Save(self):
        
        ini = Inifile()
        path = 'Setting.ini'
        ini.InIfile_Set_Path(path)
        
        if ini.InIfile_Exist(path):
            
            tmpval = self.txt_LineEdit_MIN_AREA.text()
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Setting','MIN_AREA','0')
            else:
                ini.InIfile_WriteValue('Setting','MIN_AREA',tmpval)
                
            GlobalVariable.MIN_AREA = tmpval

            tmpval = self.txt_LineEdit_MIN_WIDTH.text()
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Setting','MIN_WIDTH','0')
            else:
                ini.InIfile_WriteValue('Setting','MIN_WIDTH',tmpval)
                
            GlobalVariable.MIN_WIDTH = tmpval
            
            tmpval = self.txt_LineEdit_MIN_HEIGHT.text()
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Setting','MIN_HEIGHT','0')
            else:
                ini.InIfile_WriteValue('Setting','MIN_HEIGHT',tmpval)
            
            GlobalVariable.MIN_HEIGHT = tmpval
            
            tmpval = self.txt_LineEdit_MIN_RATIO.text()
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Setting','MIN_RATIO','0')
            else:
                ini.InIfile_WriteValue('Setting','MIN_RATIO',tmpval)
                
            GlobalVariable.MIN_RATIO = tmpval
            
            tmpval = self.txt_LineEdit_MAX_RATIO.text()
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Setting','MAX_RATIO','0')
            else:
                ini.InIfile_WriteValue('Setting','MAX_RATIO',tmpval)
                
            GlobalVariable.MAX_RATIO = tmpval
            
            tmpval = self.txt_LineEdit_MAX_DIAG_MULTIPLYER.text()
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Setting','MAX_DIAG_MULTIPLYER','0')
            else:
                ini.InIfile_WriteValue('Setting','MAX_DIAG_MULTIPLYER',tmpval)
                
            GlobalVariable.MAX_DIAG_MULTIPLYER = tmpval
            
            tmpval = self.txt_LineEdit_MAX_ANGLE_DIFF.text()
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Setting','MAX_ANGLE_DIFF','0')
            else:
                ini.InIfile_WriteValue('Setting','MAX_ANGLE_DIFF',tmpval)
                
            GlobalVariable.MAX_ANGLE_DIFF = tmpval
                
            tmpval = self.txt_LineEdit_MAX_AREA_DIFF.text()
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Setting','MAX_AREA_DIFF','0')
            else:
                ini.InIfile_WriteValue('Setting','MAX_AREA_DIFF',tmpval)
                
            GlobalVariable.MAX_AREA_DIFF = tmpval
                
            tmpval = self.txt_LineEdit_MAX_HEIGHT_DIFF.text()
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Setting','MAX_HEIGHT_DIFF','0')
            else:
                ini.InIfile_WriteValue('Setting','MAX_HEIGHT_DIFF',tmpval)
                
            GlobalVariable.MAX_HEIGHT_DIFF = tmpval
                
            tmpval = self.txt_LineEdit_MIN_N_MATCHED.text()
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Setting','MIN_N_MATCHED','0')
            else:
                ini.InIfile_WriteValue('Setting','MIN_N_MATCHED',tmpval)
                
            GlobalVariable.MIN_N_MATCHED = tmpval
                
            tmpval = self.txt_LineEdit_PLATE_WIDTH_PADDING.text()
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Setting','PLATE_WIDTH_PADDING','0')
            else:
                ini.InIfile_WriteValue('Setting','PLATE_WIDTH_PADDING',tmpval)
                
            GlobalVariable.PLATE_WIDTH_PADDING = tmpval
                
            tmpval = self.txt_LineEdit_PLATE_HEIGHT_PADDING.text()
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Setting','PLATE_HEIGHT_PADDING','0')
            else:
                ini.InIfile_WriteValue('Setting','PLATE_HEIGHT_PADDING',tmpval)
                
            GlobalVariable.PLATE_HEIGHT_PADDING = tmpval
                
            tmpval = self.txt_LineEdit_MIN_PLATE_RATIO.text()
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Setting','MIN_PLATE_RATIO','0')
            else:
                ini.InIfile_WriteValue('Setting','MIN_PLATE_RATIO',tmpval)
                
            GlobalVariable.MIN_PLATE_RATIO = tmpval
                
            tmpval = self.txt_LineEdit_MAX_PLATE_RATIO.text()
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Setting','MAX_PLATE_RATIO','0')
            else:
                ini.InIfile_WriteValue('Setting','MAX_PLATE_RATIO',tmpval)
                
            GlobalVariable.MAX_PLATE_RATIO = tmpval
        
    
    def ImageProcessing_Setting_Save(self):
        ini = Inifile()
        path = 'Setting.ini'
        ini.InIfile_Set_Path(path)
        
        if ini.InIfile_Exist(path):
            
            tmpval = int(self.chk_MophologyUse.isChecked())
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Imageprocessing','MophologyUse','0')
            else:
                ini.InIfile_WriteValue('Imageprocessing','MophologyUse',str(tmpval))
            
            imagePro.MophologyUse = tmpval
                
            tmpval = imagePro.MophologyShape
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Imageprocessing','MophologyShape','0')
            else:
                ini.InIfile_WriteValue('Imageprocessing','MophologyShape',str(tmpval))
                
            #imagePro.MophologyShape = tmpval
                
            tmpval = imagePro.MophologyMode
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Imageprocessing','MophologyMode','0')
            else:
                ini.InIfile_WriteValue('Imageprocessing','MophologyMode',str(tmpval))
                
            #imagePro.MophologyMode = tmpval
                
            tmpval = self.txt_Line_MopholX.text()
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Imageprocessing','MopholX','0')
            else:
                ini.InIfile_WriteValue('Imageprocessing','MopholX',str(tmpval))
                
            imagePro.MopholX = int(tmpval)
                
            tmpval = self.txt_Line_MopholY.text()
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Imageprocessing','MopholY','0')
            else:
                ini.InIfile_WriteValue('Imageprocessing','MopholY',str(tmpval))
                
            imagePro.MopholY = int(tmpval)
                
            tmpval = int(self.chk_BluryUse.isChecked())
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Imageprocessing','BlurUse','0')
            else:
                ini.InIfile_WriteValue('Imageprocessing','BlurUse',str(tmpval))
                
            imagePro.BlurUse = tmpval    
                
            tmpval = imagePro.BlurMode
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Imageprocessing','BlurMode','0')
            else:
                ini.InIfile_WriteValue('Imageprocessing','BlurMode',str(tmpval))
                
            #imagePro.BlurMode = tmpval
            
            tmpval = self.txt_Line_BlurX.text()
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Imageprocessing','BlurX','0')
            else:
                ini.InIfile_WriteValue('Imageprocessing','BlurX',str(tmpval))
                
            imagePro.BlurX = int(tmpval)
            
            tmpval = self.txt_Line_BlurY.text()
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Imageprocessing','BlurY','0')
            else:
                ini.InIfile_WriteValue('Imageprocessing','BlurY',str(tmpval))
                
            imagePro.BlurY = int(tmpval)

            tmpval = int(self.chk_CannyUse.isChecked())
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Imageprocessing','CannyUse','0')
            else:
                ini.InIfile_WriteValue('Imageprocessing','CannyUse',str(tmpval))
                
            imagePro.CannyUse = tmpval
                
            tmpval = self.txt_Line_thre1.text()
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Imageprocessing','CannyThresh1','0')
            else:
                ini.InIfile_WriteValue('Imageprocessing','CannyThresh1',str(tmpval))
                
            imagePro.cannythresh1 = int(tmpval)
                
            tmpval = self.txt_Line_thre2.text()
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Imageprocessing','CannyThresh2','0')
            else:
                ini.InIfile_WriteValue('Imageprocessing','CannyThresh2',str(tmpval))
                
            imagePro.cannythresh2 = int(tmpval)
                
            tmpval = int(self.chk_ThresholdUse.isChecked())
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Imageprocessing','ThresholdUse','0')
            else:
                ini.InIfile_WriteValue('Imageprocessing','ThresholdUse',str(tmpval))
                
            imagePro.ThresholdUse = tmpval
            
            tmpval = imagePro.ThreshMode
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Imageprocessing','ThreshMode','0')
            else:
                ini.InIfile_WriteValue('Imageprocessing','ThreshMode',str(tmpval))
                
            #imagePro.ThreshMode = tmpval
                
            tmpval = imagePro.AdaptMode
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Imageprocessing','AdaptMode','0')
            else:
                ini.InIfile_WriteValue('Imageprocessing','AdaptMode',str(tmpval))
                
            #imagePro.AdaptMode = tmpval
                
            tmpval = self.txt_LineThreVal.text()
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Imageprocessing','ThreshValue','0')
            else:
                ini.InIfile_WriteValue('Imageprocessing','ThreshValue',str(tmpval))
                
            imagePro.threshvalue = int(tmpval)
                
            tmpval = self.txt_LineMaxVal.text()
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Imageprocessing','MaxValue','0')
            else:
                ini.InIfile_WriteValue('Imageprocessing','MaxValue',str(tmpval))
                
            imagePro.maxvalue = int(tmpval)
            
            tmpval = self.txt_LineblockSize.text()
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Imageprocessing','BlockSize','0')
            else:
                ini.InIfile_WriteValue('Imageprocessing','BlockSize',str(tmpval))
                
            imagePro.blocksize = int(tmpval)
                
            tmpval = self.txt_LineC.text()
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Imageprocessing','C','0')
            else:
                ini.InIfile_WriteValue('Imageprocessing','C',str(tmpval))
                
            imagePro.c = int(tmpval)        
            
            tmpval = int(self.chk_ContourUse.isChecked())
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Imageprocessing','ContourUse','0')
            else:
                ini.InIfile_WriteValue('Imageprocessing','ContourUse',str(tmpval))

            imagePro.ContourUse = tmpval
            
            tmpval = imagePro.ContourMode
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Imageprocessing','ContourMode','0')
            else:
                ini.InIfile_WriteValue('Imageprocessing','ContourMode',str(tmpval))
                
            #imagePro.ContourMode = tmpval
                
            tmpval = imagePro.ContourMethod
            if tmpval == NULL or tmpval == " ":
                ini.InIfile_WriteValue('Imageprocessing','ContourMethod','0')
            else:
                ini.InIfile_WriteValue('Imageprocessing','ContourMethod',str(tmpval))
                
            #imagePro.ContourMethod = tmpval    
            
            
    def chk_MophologyUse_clicked(self):
        
        if self.chk_MophologyUse.isChecked():
            self.chk_MophologyUse.setChecked(True)
            imagePro.MophologyUse = True
            
        else:
            self.chk_MophologyUse.setChecked(False)
            imagePro.MophologyUse = False
            
    def chk_BluryUse_clicked(self):
        
        if self.chk_BluryUse.isChecked():
            self.chk_BluryUse.setChecked(True)
            imagePro.BlurUse = True
            
        else:
            self.chk_BluryUse.setChecked(False)
            imagePro.BlurUse = False
            
    def chk_ThresholdUse_clicked(self):
        
        if self.chk_ThresholdUse.isChecked():
            self.chk_ThresholdUse.setChecked(True)
            imagePro.ThresholdUse = True
            
        else:
            self.chk_ThresholdUse.setChecked(False)
            imagePro.ThresholdUse = False
            
    def chk_CannyUse_clicked(self):
        
        if self.chk_CannyUse.isChecked():
            self.chk_CannyUse.setChecked(True)
            imagePro.CannyUse = True
            
        else:
            self.chk_CannyUse.setChecked(False)
            imagePro.CannyUse = False
            
            
    def chk_ContourUse_clicked(self):
        
        if self.chk_ContourUse.isChecked():
            self.chk_ContourUse.setChecked(True)
            imagePro.ContourUse = True
            
        else:
            self.chk_ContourUse.setChecked(False)
            imagePro.ContourUse = False
            
    def rdo_Mophology_shape_clicked(self):
        
        if self.rbo_MORPH_CROSS.isChecked():
            imagePro.MophologyShape = 1
            
        elif self.rbo_MORPH_RECT.isChecked():
            imagePro.MophologyShape = 2
        elif self.rbo_MORPH_ELLIPSE.isChecked():
            imagePro.MophologyShape = 3
        
    def rdo_Mophology_Mode_clicked(self):
        
        if self.rbo_MORPH_OPEN.isChecked():
            imagePro.MophologyMode = 1
        elif self.rbo_MORPH_CLOSE.isChecked():
            imagePro.MophologyMode = 2
        elif self.rbo_MORPH_GRADIENT.isChecked():
            imagePro.MophologyMode = 3
        elif self.rbo_MORPH_TOPHAT.isChecked():
            imagePro.MophologyMode = 4
        elif self.rbo_MORPH_BLACKHAT.isChecked():
            imagePro.MophologyMode = 5
            
    def rdo_Blur_Mode_clicked(self):
        
        if self.rbo_blur.isChecked():
            imagePro.BlurMode = 1
        elif self.rbo_GaussianBlur.isChecked():
            imagePro.BlurMode = 2
        elif self.rbo_medianBlur.isChecked():
            imagePro.BlurMode = 3
        elif self.rbo_bilateralFilter.isChecked():
            imagePro.BlurMode = 4
            
    def rdo_Thresh_Mode_clicked(self):
        
        if self.rdo_THRESH_BINARY.isChecked():
            imagePro.ThreshMode = 1
        elif self.rdo_THRESH_BINARY_INV.isChecked():
            imagePro.ThreshMode = 2
        elif self.rdo_THRESH_TRUNC.isChecked():
            imagePro.ThreshMode = 3
        elif self.rdo_THRESH_TOZERO.isChecked():
            imagePro.ThreshMode = 4
        elif self.rdo_THRESH_TOZERO_INV.isChecked():
            imagePro.ThreshMode = 5
            
    def rdo_Adapt_Mode_clicked(self):
        
        if self.rdo_Threshold.isChecked():
            imagePro.AdaptMode = 1
        elif self.rdo_ADAPTIVE_THRESH_MEAN_C.isChecked():
            imagePro.AdaptMode = 2
        elif self.rdo_ADAPTIVE_THRESH_GAUSSIAN_C.isChecked():
            imagePro.AdaptMode = 3
            
    def rdo_Contour_Mode_clicked(self):
        
        if self.rdo_RETR_EXTERNAL.isChecked():
            imagePro.ContourMode = 1
        elif self.rdo_RETR_LIST.isChecked():
            imagePro.ContourMode = 2
        elif self.rdo_RETR_CCOMP.isChecked():
            imagePro.ContourMode = 3
        elif self.rdo_RETR_TREE.isChecked():
            imagePro.ContourMode = 4
            
    def rdo_Contour_Method_clicked(self):
        
        if self.rdo_CHAIN_APPROX_NONE.isChecked():
            imagePro.ContourMethod = 1
        elif self.rdo_CHAIN_APPROX_SIMPLE.isChecked():
            imagePro.ContourMethod = 2
        elif self.rdo_CHAIN_APPROX_TC89_L1.isChecked():
            imagePro.ContourMethod = 3
        elif self.rdo_CHAIN_APPROX_TC89_KCOS.isChecked():
            imagePro.ContourMethod = 4
            
    def Setting_Load(self):
        
        iniFile = Inifile()
        iniFile.InIfile_Set_Path('Setting.ini')
        
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Setting','min_area')
        if tmpval != NULL and tmpval != "":
            self.txt_LineEdit_MIN_AREA.setText(tmpval)
        else:
            self.txt_LineEdit_MIN_AREA.setText("0")
            
        GlobalVariable.MIN_AREA = tmpval
        
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Setting','min_width')
        if tmpval != NULL and tmpval != "":
            self.txt_LineEdit_MIN_WIDTH.setText(tmpval)
        else:
            self.txt_LineEdit_MIN_WIDTH.setText("0")
            
        GlobalVariable.MIN_WIDTH = tmpval
            
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Setting','min_height')
        if tmpval != NULL and tmpval != "":
            self.txt_LineEdit_MIN_HEIGHT.setText(tmpval)
        else:
            self.txt_LineEdit_MIN_HEIGHT.setText("0")
            
        GlobalVariable.MIN_HEIGHT = tmpval
            
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Setting','min_ratio')
        if tmpval != NULL and tmpval != "":
            self.txt_LineEdit_MIN_RATIO.setText(tmpval)
        else:
            self.txt_LineEdit_MIN_RATIO.setText("0")
            
        GlobalVariable.MIN_RATIO = tmpval
            
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Setting','max_ratio')
        if tmpval != NULL and tmpval != "":
            self.txt_LineEdit_MAX_RATIO.setText(tmpval)
        else:
            self.txt_LineEdit_MAX_RATIO.setText("0")
            
        GlobalVariable.MAX_RATIO = tmpval
            
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Setting','max_diag_multiplyer')
        if tmpval != NULL and tmpval != "":
            self.txt_LineEdit_MAX_DIAG_MULTIPLYER.setText(tmpval)
        else:
            self.txt_LineEdit_MAX_DIAG_MULTIPLYER.setText("0")
            
        GlobalVariable.MAX_DIAG_MULTIPLYER = tmpval
            
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Setting','max_angle_diff')
        if tmpval != NULL and tmpval != "":
            self.txt_LineEdit_MAX_ANGLE_DIFF.setText(tmpval)
        else:
            self.txt_LineEdit_MAX_ANGLE_DIFF.setText("0")
            
        GlobalVariable.MAX_ANGLE_DIFF = tmpval
            
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Setting','max_area_diff')
        if tmpval != NULL and tmpval != "":
            self.txt_LineEdit_MAX_AREA_DIFF.setText(tmpval)
        else:
            self.txt_LineEdit_MAX_AREA_DIFF.setText("0")
            
        GlobalVariable.MAX_AREA_DIFF = tmpval
            
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Setting','max_height_diff')
        if tmpval != NULL and tmpval != "":
            self.txt_LineEdit_MAX_HEIGHT_DIFF.setText(tmpval)
        else:
            self.txt_LineEdit_MAX_HEIGHT_DIFF.setText("0")
            
        GlobalVariable.MAX_HEIGHT_DIFF = tmpval
            
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Setting','min_n_matched')
        if tmpval != NULL and tmpval != "":
            self.txt_LineEdit_MIN_N_MATCHED.setText(tmpval)
        else:
            self.txt_LineEdit_MIN_N_MATCHED.setText("0")
            
        GlobalVariable.MIN_N_MATCHED = tmpval
            
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Setting','plate_width_padding')
        if tmpval != NULL and tmpval != "":
            self.txt_LineEdit_PLATE_WIDTH_PADDING.setText(tmpval)
        else:
            self.txt_LineEdit_PLATE_WIDTH_PADDING.setText("0")
            
        GlobalVariable.PLATE_WIDTH_PADDING = tmpval
            
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Setting','plate_height_padding')
        if tmpval != NULL and tmpval != "":
            self.txt_LineEdit_PLATE_HEIGHT_PADDING.setText(tmpval)
        else:
            self.txt_LineEdit_PLATE_HEIGHT_PADDING.setText("0")
            
        GlobalVariable.PLATE_HEIGHT_PADDING = tmpval
            
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Setting','min_plate_ratio')
        if tmpval != NULL and tmpval != "":
            self.txt_LineEdit_MIN_PLATE_RATIO.setText(tmpval)
        else:
            self.txt_LineEdit_MIN_PLATE_RATIO.setText("0")
            
        GlobalVariable.MIN_PLATE_RATIO = tmpval
            
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Setting','max_plate_ratio')
        if tmpval != NULL and tmpval != "":
            self.txt_LineEdit_MAX_PLATE_RATIO.setText(tmpval)
        else:
            self.txt_LineEdit_MAX_PLATE_RATIO.setText("0")
            
        GlobalVariable.MAX_PLATE_RATIO = tmpval
        
    def ImageProcessing_Setting_Load(self):
        
        iniFile = Inifile()
        iniFile.InIfile_Set_Path('Setting.ini')
        
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Imageprocessing','mophologyuse')
        if int(tmpval) == 1:
            self.chk_MophologyUse.setChecked(bool(int(tmpval)))
        else:
            self.chk_MophologyUse.setChecked(False)
            
        imagePro.MophologyUse = int(tmpval)
            
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Imageprocessing','mophologyshape')
        if int(tmpval) == 1:
            self.rbo_MORPH_CROSS.setChecked(True)
            imagePro.MophologyShape = int(tmpval)
        elif int(tmpval) == 2:
            self.rbo_MORPH_RECT.setChecked(True)
            imagePro.MophologyShape = int(tmpval)
        elif int(tmpval) == 3:
            self.rbo_MORPH_ELLIPSE.setChecked(True)
            imagePro.MophologyShape = int(tmpval)
        else:
            self.rbo_MORPH_CROSS.setChecked(True)
            imagePro.MophologyShape = 1
            
        #imagePro.MophologyShape = int(tmpval)
            
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Imageprocessing','mophologymode')
        if int(tmpval) == 1:
            self.rbo_MORPH_OPEN.setChecked(True)
            imagePro.MophologyMode = int(tmpval)
        elif int(tmpval) == 2:
            self.rbo_MORPH_CLOSE.setChecked(True)
            imagePro.MophologyMode = int(tmpval)
        elif int(tmpval) == 3:
            self.rbo_MORPH_GRADIENT.setChecked(True)
            imagePro.MophologyMode = int(tmpval)
        elif int(tmpval) == 4:
            self.rbo_MORPH_TOPHAT.setChecked(True)
            imagePro.MophologyMode = int(tmpval)
        elif int(tmpval) == 5:
            self.rbo_MORPH_BLACKHAT.setChecked(True)
            imagePro.MophologyMode = int(tmpval)
        else:
            self.rbo_MORPH_OPEN.setChecked(True)
            imagePro.MophologyMode = 1
            
        #imagePro.MophologyMode = int(tmpval)
            
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Imageprocessing','mopholx')
        if tmpval != NULL and tmpval != "":
            self.txt_Line_MopholX.setText(tmpval)
        else:
            self.txt_Line_MopholX.setText("0")
        
        imagePro.MopholX = int(tmpval)    
        
            
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Imageprocessing','mopholy')
        if tmpval != NULL and tmpval != "":
            self.txt_Line_MopholY.setText(tmpval)
        else:
            self.txt_Line_MopholY.setText("0")
            
        imagePro.MopholY = int(tmpval)
            
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Imageprocessing','bluruse')
        if int(tmpval) == 1:
            self.chk_BluryUse.setChecked(bool(int(tmpval)))
        else:
            self.chk_BluryUse.setChecked(False)
            
        imagePro.BlurUse = int(tmpval)
            
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Imageprocessing','blurmode')
        if int(tmpval) == 1:
            self.rbo_blur.setChecked(True)
            imagePro.BlurMode = int(tmpval)
        elif int(tmpval) == 2:
            self.rbo_GaussianBlur.setChecked(True)
            imagePro.BlurMode = int(tmpval)
        elif int(tmpval) == 3:
            self.rbo_medianBlur.setChecked(True)
            imagePro.BlurMode = int(tmpval)
        elif int(tmpval) == 4:
            self.rbo_bilateralFilter.setChecked(True)
            imagePro.BlurMode = int(tmpval)
        else:
            self.rbo_blur.setChecked(True)
            imagePro.BlurMode = 1
        
        imagePro.BlurMode = int(tmpval)
        
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Imageprocessing','blurX')
        if tmpval != NULL and tmpval != "":
            self.txt_Line_BlurX.setText(tmpval)
        else:
            self.txt_Line_BlurX.setText("0")
            
        imagePro.BlurX = int(tmpval)
        
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Imageprocessing','blurY')
        if tmpval != NULL and tmpval != "":
            self.txt_Line_BlurY.setText(tmpval)
        else:
            self.txt_Line_BlurY.setText("0")
            
        imagePro.BlurY = int(tmpval)
        
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Imageprocessing','cannyuse')
        if int(tmpval) == 1:
            self.chk_CannyUse.setChecked(bool(int(tmpval)))
        else:
            self.chk_CannyUse.setChecked(False)
            
        imagePro.CannyUse = int(tmpval)
            
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Imageprocessing','cannythresh1')
        if tmpval != NULL and tmpval != "":
            self.txt_Line_thre1.setText(tmpval)
        else:
            self.txt_Line_thre1.setText("0")
            
        imagePro.cannythresh1 = int(tmpval)
            
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Imageprocessing','cannythresh2')
        if tmpval != NULL and tmpval != "":
            self.txt_Line_thre2.setText(tmpval)
        else:
            self.txt_Line_thre2.setText("0")
            
        imagePro.cannythresh2 = int(tmpval)
            
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Imageprocessing','thresholduse')
        if int(tmpval) == 1:
            self.chk_ThresholdUse.setChecked(bool(int(tmpval)))
        else:
            self.chk_ThresholdUse.setChecked(False)
            
        imagePro.ThresholdUse = int(tmpval)
            
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Imageprocessing','threshmode')
        if int(tmpval) == 1:
            self.rdo_THRESH_BINARY.setChecked(True)
            imagePro.ThreshMode = int(tmpval)
        elif int(tmpval) == 2:
            self.rdo_THRESH_BINARY_INV.setChecked(True)
            imagePro.ThreshMode = int(tmpval)
        elif int(tmpval) == 3:
            self.rdo_THRESH_TRUNC.setChecked(True)
            imagePro.ThreshMode = int(tmpval)
        elif int(tmpval) == 4:
            self.rdo_THRESH_TOZERO.setChecked(True)
            imagePro.ThreshMode = int(tmpval)
        elif int(tmpval) == 5:
            self.rdo_THRESH_TOZERO_INV.setChecked(True)
            imagePro.ThreshMode = int(tmpval)
        else:
            self.rdo_THRESH_BINARY.setChecked(True)
            imagePro.ThreshMode = 1
            
        imagePro.ThreshMode = int(tmpval)
            
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Imageprocessing','adaptmode')
        if int(tmpval) == 1:
            self.rdo_Threshold.setChecked(True)
            imagePro.AdaptMode = int(tmpval)
        elif int(tmpval) == 2:
            self.rdo_ADAPTIVE_THRESH_MEAN_C.setChecked(True)
            imagePro.AdaptMode = int(tmpval)
        elif int(tmpval) == 3:
            self.rdo_ADAPTIVE_THRESH_GAUSSIAN_C.setChecked(True)
            imagePro.AdaptMode = int(tmpval)
        else:
            self.rdo_Threshold.setChecked(True)
            imagePro.AdaptMode = 1
            
        imagePro.AdaptMode = int(tmpval)
            
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Imageprocessing','threshvalue')
        if tmpval != NULL and tmpval != "":
            self.txt_LineThreVal.setText(tmpval)
        else:
            self.txt_LineThreVal.setText("0")
            
        imagePro.threshvalue = int(tmpval)
            
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Imageprocessing','maxvalue')
        if tmpval != NULL and tmpval != "":
            self.txt_LineMaxVal.setText(tmpval)
        else:
            self.txt_LineMaxVal.setText("0")
            
        imagePro.maxvalue = int(tmpval)
            
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Imageprocessing','blocksize')
        if tmpval != NULL and tmpval != "":
            self.txt_LineblockSize.setText(tmpval)
        else:
            self.txt_LineblockSize.setText("0")
            
        imagePro.blocksize = int(tmpval)
            
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Imageprocessing','c')
        if tmpval != NULL and tmpval != "":
            self.txt_LineC.setText(tmpval)
        else:
            self.txt_LineC.setText("0")
            
        imagePro.c = int(tmpval)   
       
       
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Imageprocessing','contouruse')
        if int(tmpval) == 1:
            self.chk_ContourUse.setChecked(bool(int(tmpval)))
        else:
            self.chk_ContourUse.setChecked(False)
            
        imagePro.ContourUse = int(tmpval)
            
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Imageprocessing','contourmode')
        if int(tmpval) == 1:
            self.rdo_RETR_EXTERNAL.setChecked(True)
            imagePro.ContourMode = int(tmpval)
        elif int(tmpval) == 2:
            self.rdo_RETR_LIST.setChecked(True)
            imagePro.ContourMode = int(tmpval)
        elif int(tmpval) == 3:
            self.rdo_RETR_CCOMP.setChecked(True)
            imagePro.ContourMode = int(tmpval)
        elif int(tmpval) == 4:
            self.rdo_RETR_TREE.setChecked(True)
            imagePro.ContourMode = int(tmpval)
        else:
            self.rdo_RETR_EXTERNAL.setChecked(True)
            imagePro.ContourMode = 1
            
        #imagePro.ContourMode = int(tmpval)
            
        tmpval = Inifile.InIfile_ReadValue(iniFile,'Imageprocessing','contourmethod')
        if int(tmpval) == 1:
            self.rdo_CHAIN_APPROX_NONE.setChecked(True)
            imagePro.ContourMethod = int(tmpval)
        elif int(tmpval) == 2:
            self.rdo_CHAIN_APPROX_SIMPLE.setChecked(True)
            imagePro.ContourMethod = int(tmpval)
        elif int(tmpval) == 3:
            self.rdo_CHAIN_APPROX_TC89_L1.setChecked(True)
            imagePro.ContourMethod = int(tmpval)
        elif int(tmpval) == 4:
            self.rdo_CHAIN_APPROX_TC89_KCOS.setChecked(True)
            imagePro.ContourMethod = int(tmpval)
        else:
            self.rdo_CHAIN_APPROX_NONE.setChecked(True)
            imagePro.ContourMethod = 1
            
        #imagePro.ContourMethod = int(tmpval)
        
    
class ReadWorker(QThread):
    updatePrintText = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.RunSwitch = True
    
    def run(self):
        while self.RunSwitch:
            
            #main.setDisplayText(serCom.ReadSerial())
            data = serCom.ReadSerial()
            self.updatePrintText.emit(data)
            
            sleep(1)

    def stop(self):
        self.RunSwitch = False
        self.quit()
        self.wait(1000)

class WriteWorker(QThread):
    
    PrintText = pyqtSignal(str)
    writedata = pyqtSignal(bytes)
    
    def __init__(self):
        super().__init__()
        self.btnpressed = False
        
    def run(self):
        
        while self.btnpressed:
        
        #while true:
            
            tmpGear = testCar.Gear
            tmpdirection = testCar.direction
            tmpSpeed = testCar.Speed
        
            data = str(tmpGear) + ',' + str(tmpdirection) + ',' + str(tmpSpeed) + '\n'
            
            serCom.WriteSerial(data)
            
            self.PrintText.emit(data)
        
            sleep(0.1)
            
    def stop(self):
        
        self.btnpressed = False
        self.quit()
        self.wait(1000)
        

class VideoWorker(QThread):
    
    updateImage = pyqtSignal(QImage)
    
    def __init__(self):
        super().__init__()
        self.videoThread = False
        
    def run(self):
        
        while self.videoThread:
        
            main.ImageGrab() 

            sleep(0.1)
        
            
    def stop(self):
        
        self.videoThread = False
        self.quit()
        self.wait(1000)

class VideoSaveWorker(QThread):
    
    def __init__(self):
        super().__init__()
        self.videoSaveThread = False
        
    def run(self):
        
        Cam.videoStart = True
        Cam.cam_video_Save()
             
    def stop(self):
        
        Cam.videoStart = False
        self.quit()
        self.wait(1000)
            
if __name__ == "__main__":
    
    serCom = SerialComm()
    imagePro = ImageProcessing()
    app = QApplication(sys.argv)
    main = SerialMain()
    
    testCar = Car()
    Cam = Cam()
    
    
    worker = ReadWorker()
    worker.updatePrintText.connect(main.setDisplayReadText)
    MoveWorker = WriteWorker()
    MoveWorker.PrintText.connect(main.setDisplayWriteText)
    ImageWorker = VideoWorker()
    SaveWorker = VideoSaveWorker()

    mySQL = Mysql()
    mySQL.MySQL_Connect()
    
    app.exec_()
    