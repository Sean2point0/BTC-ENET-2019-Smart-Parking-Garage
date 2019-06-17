#include<Servo.h>

//Definitions for Servo positions in degrees
#define OPEN 180
#define CLOSED 90

//Define digitalRead pins for entrance and exit to dictate open or closed state
#define EXITREAD 2
#define ENTRANCEREAD 3

//Defines pins attached to entrance and exit
#define ENTRANCESERVO 10
#define EXITSERVO 11
//Declaring entrance and exit servo structs
Servo entranceServo;
Servo exitServo;

//Used to store the states of each servo (either open or closed)
int exitState, entranceState;

void setup() {
pinMode(ENTRANCEREAD, INPUT); //Declares the ENTRANCEREAD pin as input
pinMode(EXITREAD, INPUT); //Declares the EXITREAD pin as input
entranceServo.attach(ENTRANCESERVO); //Attaches the ENTRANCESERVO to its defined pin
exitServo.attach(EXITSERVO); //Attaches the EXITSERVO to its defined pin
}

void loop() {
entranceState = (digitalRead(ENTRANCEREAD)==HIGH) ? OPEN : CLOSED; //Checks the ENTRANCEREAD pin, if high open, if low close
exitState = (digitalRead(EXITREAD)==HIGH) ? OPEN : CLOSED; //Checks the EXITREAD pin, if high open, if low close
entranceServo.write(entranceState); //Writes the entrance servo to its dictated state
exitServo.write(exitState); //Writes the exit servo to its dictated state

}
