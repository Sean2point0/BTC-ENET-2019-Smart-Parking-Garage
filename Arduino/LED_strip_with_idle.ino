#include <FastLED.h>

#if FASTLED_VERSION < 3001000
#error "Requires FastLED 3.1 or later; check github for latest code."
#endif

#define LED_PIN     2
#define PARK1_PIN   3
#define PARK2_PIN   4
#define PARK3_PIN   5
#define PARK4_PIN   6
#define PARK5_PIN   7
#define PARK6_PIN   8
#define NUM_LEDS    228
#define PARK1_LEDS   24
#define PARK2_LEDS   24
#define PARK3_LEDS   24
#define PARK4_LEDS   24
#define PARK5_LEDS   24
#define PARK6_LEDS   24
#define BRIGHTNESS  64            //max is 255
#define LED_TYPE    WS2812B
#define COLOR_ORDER GRB

uint8_t max_bright = 255;                                     // Overall brightness definition. It can be changed on the fly.
int NewCustomer = 0;
  
struct CRGB leds[NUM_LEDS];
struct CRGB park1[PARK1_LEDS];
struct CRGB park2[PARK2_LEDS];
struct CRGB park3[PARK3_LEDS];
struct CRGB park4[PARK4_LEDS];
struct CRGB park5[PARK5_LEDS];
struct CRGB park6[PARK6_LEDS];

void Park();

void Space1();
void Space2();
void Space3();
void Space4();
void Space5();
void Space6();

void Space1return();
void Space2return();
void Space3return();
void Space4return();
void Space5return();
void Space6return();

void setup(){
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
}

void loop(){
  Serial.println("Press 1 for a ticket");
  
  while(Serial.available()==0){    
    rainbow_march(200, 10);
    FastLED.show();
    }
  NewCustomer = Serial.parseInt();
  if (NewCustomer == 1){
    FastLED.clear();
    Park();
    Space1();
    Space2();
    Space3();
    Space4();
    Space5();
    Space6();
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
  fill_rainbow(park5, PARK5_LEDS, thishue, deltahue);            // Use FastLED's fill_rainbow routine.
  fill_rainbow(park6, PARK6_LEDS, thishue, deltahue);            // Use FastLED's fill_rainbow routine.

} 

void Park(){    
   for(int i = 0; i < NUM_LEDS; i++){
    leds[i].setRGB(255,255,255); 
     if (i>=6){
      leds[i-6].setRGB(0, 0, 0);
    }   
    FastLED[0].showLeds(BRIGHTNESS);
    FastLED.delay(125);
  }
  Serial.println("Now Parking");
  FastLED.delay(500);
  FastLED[0].clearLedData();
}
void Space1(){
  for(int x = PARK1_LEDS; x >= 1; x--){
    if(x<=20){
      park1[x+4].setRGB(0, 0, 0);
    }
    park1[x].setRGB(127,0,255);
    FastLED[1].showLeds(BRIGHTNESS);
    FastLED.delay(100);
  }
  FastLED.delay(500);   
  FastLED[1].clearLedData();
}

void Space2(){
  for(int j = PARK2_LEDS; j >= 1; j--){
    if(j<=20){
      park2[j+4].setRGB(0, 0, 0);
    }
    park2[j].setRGB(127,0,255);
    FastLED[2].showLeds(BRIGHTNESS);
    FastLED.delay(100);
  }
  FastLED.delay(500);   
  FastLED[2].clearLedData();
}

void Space3(){
  for(int x = PARK3_LEDS; x <= 1; x--){
    if(x<=20){
      park3[x+4].setRGB(0, 0, 0);
    }
    park3[x].setRGB(127,0,255);
    FastLED[3].showLeds(BRIGHTNESS);
    FastLED.delay(100);
  }
  FastLED.delay(500);   
  FastLED[3].clearLedData();
}

void Space4(){
  for(int x = PARK4_LEDS; x <= 1 ; x--){
    if(x<=20){
      park4[x+4].setRGB(0, 0, 0);
    }
    park4[x].setRGB(127,0,255);
    FastLED[4].showLeds(BRIGHTNESS);
    FastLED.delay(100);
  }
  FastLED.delay(500);   
  FastLED[4].clearLedData();
}

void Space5(){
  for(int x = PARK5_LEDS; x <= 1 ; x--){
    if(x<=20){
      park5[x+4].setRGB(0, 0, 0);
    }
    park5[x].setRGB(127,0,255);
    FastLED[5].showLeds(BRIGHTNESS);
    FastLED.delay(100);
  }
  FastLED.delay(500);   
  FastLED[5].clearLedData();
}

void Space6(){
  for(int x = PARK6_LEDS; x <= 1; x--){
    if(x<=20){
      park6[x+4].setRGB(0, 0, 0);
    }
    park6[x].setRGB(127,0,255);
    FastLED[6].showLeds(BRIGHTNESS);
    FastLED.delay(100);
  }
  FastLED.delay(500);   
  FastLED[6].clearLedData();
}

/////////////////////////////////////

void Space1return(){
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

void Space2return(){
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

void Space3return(){
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

void Space4return(){
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

void Space5return(){
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

void Space6return(){
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
