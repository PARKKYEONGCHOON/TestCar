import serial
import threading, time
import serial.tools.list_ports as sp
import sys
import glob

class SerialComm:
    
    def __init__(self):
        
        self.port = 'COM7'
        self.baudrate = 115200
        self.parity = serial.PARITY_NONE
        self.stopBits = serial.STOPBITS_ONE
        self.DataBits = serial.EIGHTBITS
        self.lst_BaudRate = ['50', '75', '110', '134', '150', '200', '300', '600', '1200', '1800', '2400', '4800', '9600', '19200', '38400', '57600', '115200']
        self.ReadStart = False
        self.WriteStart = False
        self.ReadData = ''
    def Connect(self,port,baudrate):
        
        try:
            self.ser = serial.Serial(port,int(baudrate), timeout=1)
            self.PortOpen()
            print("Connect Complete")
            return True
        except:
            print("Connect Fail")
            return False
    
    def ReadSerial(self):
        if self.Port_IsOpen():
            if self.ser.readable():
                #self.ReadData = self.ser.readline().decode("ascii").strip()
                self.ReadData = self.ser.readline()
                return str(self.ReadData)
                
        else:
            
            print("Port Connect Fail")
            
    def ReadRun(self):
        
        if self.Port_IsOpen():
            
            self.ReadStart = True
            
            while self.ReadStart:
                if self.ser.readable():
                    #res = self.ser.readline().decode("ascii").strip()
                    res = self.ser.readline()
                    print(res)
                    
                    
            #time.sleep(1000)
            
            
                    
        else:
            
            self.threadSwitch = False
            print("Port Connect Fail")
            
    
    def WriteSerial(self,data):
        
        try:
            if self.Port_IsOpen():
                self.ser.write(data.encode())
            else:
                print("port Open Fail")
        except:
            
            #self.portClose()
            print("Write Fail")
             
    def WriteEncodeSerial(self, data):
        
        data = data.encode('utf-8')
        
        try:
            if self.Port_IsOpen():
                self.ser.write(data)
            else:
                print("port Open Fail")
        except:
            
            self.portClose()
            print("Write Fail")
    
    def PortOpen(self):
        
        try:
            
            if self.ser.is_open:
                
                self.ser.close()    
                self.ser.open()
            else:
                
                self.ser.open()
            
        except:
            print("Port Open Fail")
            
    def Port_IsOpen(self):
        
       res =  self.ser.isOpen()
       return res
   
    def portClose(self):
        
        self.ser.close()
        
    def serial_ports(self):
            
        """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

