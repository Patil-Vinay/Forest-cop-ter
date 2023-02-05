#include <sim900.h> //download library from https://github.com/Seeed-Studio/GPRS_SIM900
#include <SoftwareSerial.h> //default library
#include <Wire.h> //default library

int Incomingch;
String data,Fdata;

 //Connect Tx pin of GSM to 9 of Arduino
//Connect Rx pin of GSM to 10 of Arduino
SoftwareSerial gprs(9,8);//TX,RX

void setup(){
  Serial.begin(9600); //Serial monitor works on 9600 baudrate for debugging
  sim900_init(&gprs, 9600); //GSM module works on 9600 baudrate
 
  Serial.println("Arduino - Automatic Voice Machine");
}

/Function to read Incoming data from GSM to Arduino/
void check_Incoming()
{
    if(gprs.available()) //If GSM is saying something
    {
   Incomingch = gprs.read(); // Listen to it and store in this variable

  if (Incomingch == 10 || Incomingch ==13) //If it says space (10) or Newline (13) it means it has completed one word
  {Serial.println(data);  Fdata =data; data = ""; } //Print the word and clear the variable to start fresh
  else
  {
  String newchar = String (char(Incomingch)); //convert the char to string by using string objects
  data = data +newchar; // After converting to string, do string concatenation
  }
  }
}
/##End of Function##/

void loop(){

   check_Incoming(); //Read what GSM module is saying

  if(Serial.available()){   //Used for debugging
    gprs.write(Serial.read());  //Used for debugging
  } //Used for debugging

  if (Fdata == "RING") //If the GSM module says RING
  {
  delay(2000); //wait for 5sec to create 3 ring delay.
  gprs.write ("ATA\r\n"); //Answer the call
  Serial.println ("Placed Received");  //Used for debugging
  while(Fdata != "OK") //Until call successfully answered
  {check_Incoming(); //Read what GSM module is saying


 
  }
  } 
}