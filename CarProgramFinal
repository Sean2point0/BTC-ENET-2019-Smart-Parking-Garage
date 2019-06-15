#include "simpletools.h"
#include "abdrive360.h"
#include "fdserial.h"

//Light Tracking
  //Base values included with program given by Parallax
    volatile int leftPtran = 9, rightPtran = 5;
    volatile int speedLeft, speedRight, ndiff, stop = 0;
    volatile int lightLeft, lightRight;
    int Pleft = 0, Pright = 0;

  //Values used for proportional speed
    volatile int baseSpeed = 43; //Base speed should be between 43 and 50 @ 125 LED delay
    volatile int doubleBaseSpeed,speedDiff;
    
    //Values used for bluetooth
    int *serialCore;
    int rxpin = 8, txpin = 7, baudRate = 9600;
    int received;
    fdserial *bluetooth;
    
    //Core labels
    int *tickCore;
    
  //Function declaraion
  int RC_check();
  void tickCounter();

int main(){
  
  doubleBaseSpeed = baseSpeed*2;
  bluetooth = fdserial_open(rxpin, txpin, 0, baudRate); //rx, tx, mode, baud rate
  fdserial_rxFlush(bluetooth);
  
  while(1)
  {
  received = fdserial_rxChar(bluetooth);
  if((received == 'g')||(received =='G')){
    pause(100);
    tickCore = cog_run(tickCounter, 128);
    pause(20);
    while(stop == 0){
    lightLeft = RC_check(leftPtran); //Reads the time constant for Left Phototransistor
    lightRight = RC_check(rightPtran); //Reads the time constant for Right Phototransistor
    
    ndiff = doubleBaseSpeed * lightRight / (lightRight + lightLeft) - baseSpeed; //Creates a ratio used to determine robot direction
    
    speedLeft = baseSpeed; speedRight = baseSpeed; //If the robot is within the far limit, the robot moves the adjusted speed
    
    if((lightLeft > 150)&&(lightRight > 150 )){ //Detects if there is a light to follow
      drive_speed(0,0);
    }
    
    else{ //If there is a bright enough light close by 
      if(ndiff >= 0) speedLeft -= (ndiff*2); //Sets the left servo drive speed if the light is brighter to the Parallax's right
      else speedRight += (ndiff*2); //Sets the right servo drive speed if the light is brighter to the Parallax's left
      speedLeft = (speedLeft <= 0) ? 0 : speedLeft;
      speedRight = (speedRight <= 0) ? 0 : speedRight;
      drive_speed(speedLeft, speedRight);
      print("%d %d\n", speedLeft, speedRight);
    }    
    }
    fdserial_txChar(bluetooth, 'd');
    cog_end(tickCore);
    stop = 0;
    drive_speed(0, 0);
    }
  
  else if((received == 'b')||(received == 'B')){
    tickCore = cog_run(tickCounter, 128);
    pause(20);
    while(stop == 0){
    lightLeft = RC_check(rightPtran); //Reads the time constant for Left Phototransistor
    lightRight = RC_check(leftPtran); //Reads the time constant for Right Phototransistor
    
    ndiff = doubleBaseSpeed * lightRight / (lightRight + lightLeft) - baseSpeed; //Creates a ratio used to determine robot direction
    speedLeft = baseSpeed; speedRight = baseSpeed;

    if((lightLeft > 150)&&(lightRight > 150 )){
      drive_speed(0,0); //If there is not a bright enough light, the parallax will stop           
    }      
      
    else{ //If there is a bright enough light close by
      if(ndiff >= 0) speedLeft -= (ndiff*2); //Sets the left servo drive speed if the light is brighter to the Parallax's right
      else speedRight += (ndiff*2); //Sets the right servo drive speed if the light is brighter to the Parallax's left
      speedLeft = (speedLeft <= 0) ? 0 : speedLeft;
      speedRight = (speedRight <= 0) ? 0 : speedRight;
      drive_speed(-speedLeft, -speedRight); //Sets the drive speed according to the difference of RC time constant
      }
    }
    fdserial_txChar(bluetooth, 'd');
    cog_end(tickCore);
    stop = 0;
    drive_speed(0, 0);
    }
  }
}  

int RC_check(int pinNum){ //Function for reading the time constants
  high(pinNum); //Sets pin to high
  pause(1); //Pauses for 1 millisecond
  int RC_return = rc_time(pinNum, 1); //Reads the time constant for Left Phototransistor
  return RC_return; //Returns the time constant
}

void tickCounter(){
  while(1){
   pause(6000);
   int Tright, Tleft;
   drive_getTicks(&Tright, &Tleft);
   if((Tright != Pright)||(Tleft != Pleft)){
      Pright = Tright;
      Pleft = Tleft;
      stop = 0;
   }
   else
    stop = 1;
  }        
}
