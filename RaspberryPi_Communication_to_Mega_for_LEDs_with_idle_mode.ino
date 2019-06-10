#include <FastLED.h>

#define LED_PIN     2
#define PARK1_PIN   3
#define PARK2_PIN   4
#define PARK3_PIN   5
#define PARK4_PIN   6
#define PARK5_PIN   7
#define PARK6_PIN   8

#define NUM_LEDS    200
#define ONE         30
#define TWO         40
#define THREE       50
#define FOUR        60
#define FIVE        70
#define SIX         80

#define PARK1_LEDS   24
#define PARK2_LEDS   24
#define PARK3_LEDS   24
#define PARK4_LEDS   24
#define PARK5_LEDS   24
#define PARK6_LEDS   24
#define BRIGHTNESS  64            //max is 255
#define LED_TYPE    WS2812B
#define COLOR_ORDER GRB

CRGB leds[NUM_LEDS];
CRGB park1[PARK1_LEDS];
CRGB park2[PARK2_LEDS];
CRGB park3[PARK3_LEDS];
CRGB park4[PARK4_LEDS];
CRGB park5[PARK5_LEDS];
CRGB park6[PARK6_LEDS];

void Park();
void ParkLeds();
void Space1();
void Space2();
void Space3();
void Space4();
void Space5();
void Space6();

char customer;
uint8_t max_bright = 255;                                     // Overall brightness definition. It can be changed on the fly.

void setup(){
  
  //int NewCustomer = 0;
  delay(3000);
  Serial.begin(9600);
  while(!Serial){}

  LEDS.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
  LEDS.addLeds<LED_TYPE, PARK1_PIN, COLOR_ORDER>(park1, PARK1_LEDS);
  LEDS.addLeds<LED_TYPE, PARK2_PIN, COLOR_ORDER>(park2, PARK2_LEDS);
  LEDS.addLeds<LED_TYPE, PARK3_PIN, COLOR_ORDER>(park3, PARK3_LEDS);
  LEDS.addLeds<LED_TYPE, PARK4_PIN, COLOR_ORDER>(park4, PARK4_LEDS);
  LEDS.addLeds<LED_TYPE, PARK5_PIN, COLOR_ORDER>(park5, PARK5_LEDS);
  LEDS.addLeds<LED_TYPE, PARK6_PIN, COLOR_ORDER>(park6, PARK6_LEDS);


  FastLED.setBrightness(max_bright);
  set_max_power_in_volts_and_milliamps(5, 1000);              // FastLED 2.1 Power management set at 5V, 500mA

  //Serial.println("Press 1 for a ticket");
  //while(Serial.available()==0){
    // }
 /* NewCustomer = Serial.parseInt();
  if (NewCustomer == 1){
    Park();
    Space1();
    Space2();
    Space3();
    Space4();
   // Space5();
   // Space6();
  }
}*/  
}
void loop() { 
  while(Serial.available()==0){    
    rainbow_march(200, 10);
    FastLED.show();
  }
  if(Serial.available()){
     customer = (Serial.read());
     if(customer == '1'){
        ParkLeds();
        FastLED[0].clearLedData();
        Space1();
        FastLED[1].clearLedData();
      }else if(customer == '2'){
        ParkLeds();
        FastLED[0].clearLedData();
        Space2();
        FastLED[2].clearLedData();
      }else if (customer == '3'){
        ParkLeds();
        FastLED[0].clearLedData();
        Space3();
        FastLED[3].clearLedData();
      }else if(customer == '4'){
        ParkLeds();
        FastLED[0].clearLedData();
        Space4();
        FastLED[4].clearLedData();
      }
      }
        delay(500);
  }

void Park(){ 
     
  for(int i = 0; i < NUM_LEDS; i++){
    if (i>=4){
      leds[i-4].setRGB(0, 0, 0);
    }
    leds[i].setRGB(127,0,255);
    FastLED[0].showLeds(BRIGHTNESS);
    FastLED.delay(100);
  }
  FastLED.delay(500);
  FastLED[0].clearLedData();
}

void Space1(){
  for(int x = 0; x < PARK1_LEDS; x++){
    if(x>=4){
      park1[x-4].setRGB(0, 0, 0);
    }
    park1[x].setRGB(127,0,255);
    FastLED[1].showLeds(BRIGHTNESS);
    FastLED.delay(100);
  }
  FastLED.delay(500);   
  FastLED[1].clearLedData();
}

void Space2(){
  for(int j = 0; j < PARK2_LEDS; j++){
    if(j>=4){
      park2[j-4].setRGB(0, 0, 0);
    }
    park2[j].setRGB(127,0,255);
    FastLED[2].showLeds(BRIGHTNESS);
    FastLED.delay(100);
  }
  FastLED.delay(500);   
  FastLED[2].clearLedData();
}

void Space3(){
  for(int x = 0; x < PARK3_LEDS; x++){
    if(x>=4){
      park3[x-4].setRGB(0, 0, 0);
    }
    park3[x].setRGB(127,0,255);
    FastLED[3].showLeds(BRIGHTNESS);
    FastLED.delay(100);
  }
  FastLED.delay(500);   
  FastLED[3].clearLedData();
}

void Space4(){
  for(int x = 0; x < PARK4_LEDS; x++){
    if(x>=4){
      park4[x-4].setRGB(0, 0, 0);
    }
    park4[x].setRGB(127,0,255);
    FastLED[4].showLeds(BRIGHTNESS);
    FastLED.delay(100);
  }
  FastLED.delay(500);   
  FastLED[4].clearLedData();
}

void Space5(){
  for(int x = 0; x < PARK5_LEDS; x++){
    if(x>=4){
      park5[x-4].setRGB(0, 0, 0);
    }
    park5[x].setRGB(127,0,255);
    FastLED[5].showLeds(BRIGHTNESS);
    FastLED.delay(100);
  }
  FastLED.delay(500);   
  FastLED[5].clearLedData();
}

void Space6(){
  for(int x = 0; x < PARK6_LEDS; x++){
    if(x>=4){
      park6[x-4].setRGB(0, 0, 0);
    }
    park6[x].setRGB(127,0,255);
    FastLED[6].showLeds(BRIGHTNESS);
    FastLED.delay(100);
  }
  FastLED.delay(500);   
  FastLED[6].clearLedData();
}

void ParkLeds(){
  if(customer == '1'){
      for(int x = 0; x <= 10; x++){
        if(x>=4){
        leds[x-4].setRGB(0, 0, 0);
        }
      leds[x].setRGB(127,0,255);
      FastLED[0].showLeds(BRIGHTNESS);
      FastLED.delay(100);
      }
  }
   else if(customer == '2'){
      for(int x = 0; x <= 20; x++){
        if(x>=4){
          leds[x-4].setRGB(0, 0, 0);
          }
        leds[x].setRGB(127,0,255);
        FastLED[0].showLeds(BRIGHTNESS);
        FastLED.delay(100);
        }      
      }else if (customer == '3'){
        for(int x = 0; x <= 30; x++){
        if(x>=4){
        leds[x-4].setRGB(0, 0, 0);
        }
      leds[x].setRGB(127,0,255);
      FastLED[0].showLeds(BRIGHTNESS);
      FastLED.delay(100);
      }
      }else if(customer == '4'){
        for(int x = 0; x <= 40; x++){
        if(x>=4){
        leds[x-4].setRGB(0, 0, 0);
        }
      leds[x].setRGB(127,0,255);
      FastLED[0].showLeds(BRIGHTNESS);
      FastLED.delay(100);
        }
      }
}

void rainbow_march(uint8_t thisdelay, uint8_t deltahue) {     // The fill_rainbow call doesn't support brightness levels.

  uint8_t thishue = millis()*(255-thisdelay)/255;             // To change the rate, add a beat or something to the result. 'thisdelay' must be a fixed value.
  
// thishue = beat8(50);                                       // This uses a FastLED sawtooth generator. Again, the '50' should not change on the fly.
// thishue = beatsin8(50,0,255);                              // This can change speeds on the fly. You can also add these to each other.
  
  fill_rainbow(leds, NUM_LEDS, thishue, deltahue);            // Use FastLED's fill_rainbow routine.
  fill_rainbow(park1, PARK1_LEDS, thishue, deltahue);            // Use FastLED's fill_rainbow routine.
  fill_rainbow(park2, PARK2_LEDS, thishue, deltahue);            // Use FastLED's fill_rainbow routine.
  fill_rainbow(park3, PARK3_LEDS, thishue, deltahue);            // Use FastLED's fill_rainbow routine.
  fill_rainbow(park4, PARK4_LEDS, thishue, deltahue);            // Use FastLED's fill_rainbow routine.
}
