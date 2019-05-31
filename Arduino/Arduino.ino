#include <PID_v1.h>
#include <Wire.h>
#include <Servo.h>

#define ServoXPin 3
#define ServoYPin 4
#define LED 13

Servo ServoX;
Servo ServoY;

//int CenterX = 1432, CenterY = 1568;
int CenterX = 1432, CenterY = 1570;
int Interval = 20, Ts = 100;
int JoystickX, JoystickY;
int isStable = 0;

double InputX, OutputX, SetpointX;
double InputY, OutputY, SetpointY;

double KpX=0.822, KiX=0, KdX=0.552;
double KpY=0.822, KiY=0, KdY=0.552;

//PID myPIDX(&InputX, &OutputX, &SetpointX, KpX, KiX, KdX, P_ON_M, REVERSE);
//PID myPIDY(&InputY, &OutputY, &SetpointY, KpY, KiY, KdY, P_ON_M, DIRECT);
PID myPIDX(&InputX, &OutputX, &SetpointX, KpX, KiX, KdX, REVERSE);
PID myPIDY(&InputY, &OutputY, &SetpointY, KpY, KiY, KdY, DIRECT);

String inputString = "";

boolean isXManual = false;
boolean isYManual = false;

boolean stringComplete = false, changeConstant = false;

int16_t Acc_rawX, Acc_rawY, Acc_rawZ,Gyr_rawX, Gyr_rawY, Gyr_rawZ;

float Acceleration_angle[2], Gyro_angle[2], Total_angle[2];
float rad_to_deg = 180/3.141592654;

double elapsedTime, time, timePrev;

void setup()
{
  // I/O Config //
  pinMode(LED, OUTPUT);
  // MPU-6050 Config //
  Wire.begin();
  Wire.beginTransmission(0x68);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);
  // Servos Config //
  ServoX.attach(ServoXPin);
  ServoY.attach(ServoYPin);
  ServoX.writeMicroseconds(CenterX);
  ServoY.writeMicroseconds(CenterY);
  // Serial Config //
  Serial.begin(115200);
  // PID's Config //
  myPIDX.SetMode(AUTOMATIC);
  myPIDY.SetMode(AUTOMATIC);
  myPIDX.SetOutputLimits(-Interval, Interval);
  myPIDY.SetOutputLimits(-Interval, Interval);
  myPIDX.SetSampleTime(Ts);
  myPIDY.SetSampleTime(Ts);
  // Data Config //
  inputString.reserve(500);

  delay(100);
}

void getData()
{
  int divA = inputString.indexOf('!');
  int divB = inputString.indexOf('#');
  int divC = inputString.indexOf('$');
  int divD = inputString.indexOf('%');
  int divE = inputString.indexOf('&');
  int divF = inputString.indexOf('[');
  int divG = inputString.indexOf(']');
  int divH = inputString.indexOf('{');
  int divI = inputString.indexOf('}');
  int len = inputString.length();
  String cpX = inputString.substring(0,divA);
  String cpY = inputString.substring(divA+1,divB);
  String spX = inputString.substring(divB+1,divC);
  String spY = inputString.substring(divC+1,divD);
  String kpx = inputString.substring(divD+1,divE);
  String kix = inputString.substring(divE+1,divF);
  String kdx = inputString.substring(divF+1,divG);
  String kpy = inputString.substring(divG+1,divH);
  String kiy = inputString.substring(divH+1,divI);
  String kdy = inputString.substring(divI+1,len-1);
  InputX = cpX.toDouble();
  InputY = cpY.toDouble();
  SetpointX = spX.toDouble();
  SetpointY = spY.toDouble();
  KpX = kpx.toDouble();
  KiX = kix.toDouble();
  KdX = kdx.toDouble();
  KpY = kpy.toDouble();
  KiY = kiy.toDouble();
  KdY = kdy.toDouble();
  stringComplete = false;
  inputString = "";
}

void sendData()
{
  Serial.print(Total_angle[0]);
  Serial.print(",");
  Serial.print(Total_angle[1] + 2);
  Serial.print(",");
  Serial.print(JoystickX);
  Serial.print(",");
  Serial.print(JoystickY);
  Serial.println(",");
}

void serialEvent()
{
  while(Serial.available())
  {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '@')
    {
      stringComplete = true;
      changeConstant = false;
    }
    else if (inChar == '*')
    {
      stringComplete = true;
      changeConstant = true;
    }
  }
}

void stableCheck(double radius)
{
  double R = sqrt(sq(abs(InputX - SetpointX)) + sq(abs(InputY - SetpointY)));
  if (R <= radius)
  {
    if(isStable > 150)
    {
      OutputX = 0;
      OutputY = 0;
      ServoX.detach();
      ServoY.detach();
      digitalWrite(LED, HIGH);
    }
    else
    {
      isStable++;
    }
  }
  else
  {
    isStable = 0;
    ServoX.attach(ServoXPin);
    ServoY.attach(ServoYPin);
    digitalWrite(LED, LOW);
  }
}

void processAccData()
{
  Acceleration_angle[0] = atan((Acc_rawY/16384.0)/sqrt(pow((Acc_rawX/16384.0),2) + pow((Acc_rawZ/16384.0),2)))*rad_to_deg;
  Acceleration_angle[1] = atan(-1*(Acc_rawX/16384.0)/sqrt(pow((Acc_rawY/16384.0),2) + pow((Acc_rawZ/16384.0),2)))*rad_to_deg;
}

void recordAccReg()
{
  Wire.beginTransmission(0x68);
  Wire.write(0x3B); //Ask for the 0x3B register- correspond to AcX
  Wire.endTransmission(false);
  Wire.requestFrom(0x68,6,true);

  Acc_rawX=Wire.read()<<8|Wire.read(); //each value needs two registres
  Acc_rawY=Wire.read()<<8|Wire.read();
  Acc_rawZ=Wire.read()<<8|Wire.read();
  processAccData();
}

void processGyroData()
{
  Gyro_angle[0] = Gyr_rawX/131.0;
  Gyro_angle[1] = Gyr_rawY/131.0;
}

void recordGyroReg()
{
  Wire.beginTransmission(0x68);
  Wire.write(0x43); //Gyro data first adress
  Wire.endTransmission(false);
  Wire.requestFrom(0x68,4,true); //Just 4 registers

  Gyr_rawX=Wire.read()<<8|Wire.read(); //Once again we shif and sum
  Gyr_rawY=Wire.read()<<8|Wire.read();
  processGyroData();
}

void totalAngle()
{
  Total_angle[0] = 0.98 *(Total_angle[0] + Gyro_angle[0]*elapsedTime) + 0.02*Acceleration_angle[0];
  Total_angle[1] = 0.98 *(Total_angle[1] + Gyro_angle[1]*elapsedTime) + 0.02*Acceleration_angle[1];
}

void processJoystickData()
{
  int AnalogX = map(analogRead(A1), 20, 1000, -200, 200);
  int AnalogY = map(analogRead(A2), 20, 1000, 200, -200);
  if (AnalogX < 0)
  {
    JoystickX = JoystickX + (int)((AnalogX/100)%-10);
    JoystickX = constrain(JoystickX, -200, 200);
  }
  else
  {
    JoystickX = JoystickX + (int)((AnalogX/100)%10);
    JoystickX = constrain(JoystickX, -200, 200);
  }
  if (AnalogY < 0)
  {
    JoystickY = JoystickY + (int)((AnalogY/100)%-10);
    JoystickY = constrain(JoystickY, -200, 200);
  }
  else
  {
    JoystickY = JoystickY + (int)((AnalogY/100)%10);
    JoystickY = constrain(JoystickY, -200, 200);
  }
}

double degToPWM(double deg)
{
    return(deg * 5.555);
}

void loop()
{
  timePrev = time;
  time = millis();
  elapsedTime = (time - timePrev) / 1000;

  recordAccReg();
  processAccData();
  recordGyroReg();
  processGyroData();
  processJoystickData();
  totalAngle();

  stableCheck(1.00);

  myPIDX.Compute();
  myPIDY.Compute();

  ServoX.writeMicroseconds(CenterX + degToPWM(OutputX));
  ServoY.writeMicroseconds(CenterY + degToPWM(OutputY));

  if (stringComplete)
  {
    getData();
    if (changeConstant)
    {
      myPIDX.SetTunings(KpX, KiX, KdX);
      myPIDY.SetTunings(KpY, KiY, KdY);
      changeConstant = false;
    }
    sendData();
  }
}
