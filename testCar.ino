#include <Servo.h>
const int DCA1 = 3;
const int DCA2 = 4;
const int DCB1 = 5;
const int DCB2 = 6;
const int SV = 9;
const int bz = 10;
const int tri = 11;
const int echo = 12;

String strData;
char chrData;
int intData;

int fData;
int SData;
int tData;

String strCarGear;
String strCarDirection;
String strCarSpeed;
String zero = "0";

int iCarGear;
int iCarDirection;
int iCarSpeed;

//int tones[] = {261, 277, 294, 311, 330, 349, 370, 392};
int tones[] = {370, 392,349};
int numTones = 3;
Servo servo;

void setup() {
  // put your setup code here, to run once:

  Serial.begin(115200);
  
  servo.attach(SV);
  servo.write(90);

  pinMode(tri,OUTPUT);
  pinMode(echo,INPUT);
  pinMode(DCA1,OUTPUT);
  pinMode(DCA2,OUTPUT);
  pinMode(DCB1,OUTPUT);
  pinMode(DCB2,OUTPUT);


}

void loop() {
  // put your main code here, to run repeatedly:

  ReadData();
  MotorOperation(iCarGear,iCarDirection,iCarSpeed);
  distCheck();
  
}

void ReadData()
{
  
  if(Serial.available()>0)
  {
    strData = Serial.readStringUntil('/n');
    strData.trim();
    //strData = Serial.readString();
    //Serial.print(strData);

    fData = strData.indexOf(',');
    SData = strData.indexOf(',',fData+1);
    tData = strData.indexOf(',',SData+1);

    strCarGear = strData.substring(0,fData);
    strCarDirection = strData.substring(fData+1,SData);
    strCarSpeed = strData.substring(SData+1,tData);
        
    iCarGear = strCarGear.toInt();
    iCarDirection = strCarDirection.toInt();
    iCarSpeed = strCarSpeed.toInt();
    
    //Serial.println(strCarGear+','+strCarDirection+','+strCarSpeed);
    
  }
  else
  {
    iCarGear = 0;
    iCarDirection = 0;
    iCarSpeed = 0;
  }
  
}

void MotorOperation(int gear, int dir, int sp)
{
  
  
  switch(gear)
  {
    case 1: //후진
      if(dir == 3) //좌
      {
        servo.write(0);
        delay(10);
        digitalWrite(DCA1, 0);
        digitalWrite(DCA2, sp);
        digitalWrite(DCB1, 0);
        digitalWrite(DCB2, 0);
        //servo.write(90);
        //delay(10);
      }
      else if(dir == 4) //우
      {
        servo.write(180);
        delay(10);
        digitalWrite(DCA1, 0);
        digitalWrite(DCA2, 0);
        digitalWrite(DCB1, 0);
        digitalWrite(DCB2, sp);
        //servo.write(90);
        //delay(10);
      }
      else
      {
        servo.write(90);
        delay(10);
        digitalWrite(DCA1, 0);
        digitalWrite(DCA2, sp);
        digitalWrite(DCB1, 0);
        digitalWrite(DCB2, sp);
      }
        
    break;
    
    case 2: //중립
      servo.write(90);
      delay(20);
      digitalWrite(DCA1, 0);
      digitalWrite(DCA2, 0);
      digitalWrite(DCB1, 0);
      digitalWrite(DCB2, 0);
    break;
    
    case 3: //전진
      if(dir == 3) //좌
      {
        servo.write(0);
        delay(10);
        digitalWrite(DCA1, sp);
        digitalWrite(DCA2, 0);
        digitalWrite(DCB1, 0);
        digitalWrite(DCB2, 0);
        //servo.write(90);
        //delay(20);
      }
      else if(dir == 4) //우
      {
        servo.write(180);
        delay(20);
        digitalWrite(DCA1, 0);
        digitalWrite(DCA2, 0);
        digitalWrite(DCB1, sp);
        digitalWrite(DCB2, 0);
        //servo.write(90);
        //delay(20);
      }
      else
      {
        servo.write(90);
        delay(20);
        digitalWrite(DCA1, sp);
        digitalWrite(DCA2, 0);
        digitalWrite(DCB1, sp);
        digitalWrite(DCB2, 0);
      }
    break;

    default:
    break;
  }
}

void distCheck()
{
  digitalWrite(tri, 0);
  delayMicroseconds(20);
  digitalWrite(tri, 1);
  delayMicroseconds(10);
  digitalWrite(tri, 0);

  double duration = pulseIn(echo, HIGH);
  double tmpdistance = (duration/2) / 29.1;

  if(tmpdistance < 4)
  {
    for(int i = 0; i<3; i++)
    {
      Alarm();
      digitalWrite(DCA1, 0);
      digitalWrite(DCA2, 0);
      digitalWrite(DCB1, 0);
      digitalWrite(DCB2, 0);
    }
  }

}

void Alarm()
{
  for(int i = 0; i < numTones; i++)
    {
      tone(bz, tones[i]);
      delay(250);
    }
    noTone(bz);
    delay(500);
}
