#include <FastLED.h>

#if FASTLED_VERSION < 3001000
#error "Requires FastLED 3.1 or later; check github for latest code."
#endif

#define LED_PIN     2
#define PARK1_PIN   4
#define PARK2_PIN   7
#define PARK3_PIN   8
#define PARK4_PIN   6
#define PARK5_PIN   5
#define PARK6_PIN   3

#define ONE         6
#define TWO         19
#define THREE       33
#define FOUR        110
#define FIVE        123
#define SIX         137

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
char customer;                         //[] = {'1','2','3','4','5','6','a','c','d','e','f','h'}

struct CRGB leds[NUM_LEDS];
struct CRGB park1[PARK1_LEDS];
struct CRGB park2[PARK2_LEDS];
struct CRGB park3[PARK3_LEDS];
struct CRGB park4[PARK4_LEDS];
struct CRGB park5[PARK5_LEDS];
struct CRGB park6[PARK6_LEDS];

void Park();
void ParkLeds();

void Space1();
void Space2();
void Space3();
void Space4();
void Space5();
void Space6();

void rainbow_march(uint8_t thisdelay, uint8_t deltahue);

void Space1return();
void Space2return();
void Space3return();
void Space4return();
void Space5return();
void Space6return();
void ReturnLeds();

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
  while(Serial.available()==0){    
    rainbow_march(200, 10);
    FastLED.show();
    }
  if(Serial.available()){
     customer = (Serial.read());
     if(customer == '1'){
        for(int x = 0; x <= 6; x++){
          FastLED[x].clearLedData();
        }
        ParkLeds();
        FastLED.show();
        FastLED[0].clearLedData();
        Space1();
        FastLED.show();
        FastLED[1].clearLedData();
      }else if(customer == '2'){
        for(int x = 0; x <= 6; x++){
          FastLED[x].clearLedData();
        }
        ParkLeds();
        FastLED.show();
        FastLED[0].clearLedData();
        Space2();
        FastLED.show();
        FastLED[2].clearLedData();
      }else if (customer == '3'){
        for(int x = 0; x <= 6; x++){
          FastLED[x].clearLedData();
        }
        ParkLeds();
        FastLED.show();
        FastLED[0].clearLedData();
        Space3();
        FastLED.show();
        FastLED[3].clearLedData();
      }else if(customer == '4'){
        for(int x = 0; x <= 6; x++){
          FastLED[x].clearLedData();
        }
        ParkLeds();
        FastLED.show();
        FastLED[0].clearLedData();
        Space4();
        FastLED.show();
        FastLED[4].clearLedData();

      }else if(customer == '5'){
        for(int x = 0; x <= 6; x++){
          FastLED[x].clearLedData();
        }
        ParkLeds();
        FastLED.show();
        FastLED[0].clearLedData();
        Space5();
        FastLED.show();
        FastLED[5].clearLedData();
      }else if(customer == '6'){
        for(int x = 0; x <= 6; x++){
          FastLED[x].clearLedData();
        }
        ParkLeds();
        FastLED.show();
        FastLED[0].clearLedData();
        Space6();
        FastLED.show();
        FastLED[6].clearLedData();
      }else if(customer == 'a'){
          for(int x = 0; x <= 6; x++){
             FastLED[x].clearLedData();
          }
          Space1return();
          FastLED.show();
          FastLED[1].clearLedData();
          ReturnLeds();
          FastLED.show();
          FastLED[0].clearLedData();
        }else if(customer == 'h'){
          for(int x = 0; x <= 6; x++){
             FastLED[x].clearLedData();
          }
          Space2return();
          FastLED.show();
          FastLED[2].clearLedData();
          ReturnLeds();
          FastLED.show();
          FastLED[0].clearLedData();
        }else if(customer == 'c'){
          for(int x = 0; x <= 6; x++){
             FastLED[x].clearLedData();
          }
          Space3return();
          FastLED.show();
          FastLED[3].clearLedData();
          ReturnLeds();
          FastLED.show();
          FastLED[0].clearLedData();
        }else if(customer == 'd'){
          for(int x = 0; x <= 6; x++){
             FastLED[x].clearLedData();
          }
          Space4return();
          FastLED.show();
          FastLED[4].clearLedData();
          ReturnLeds();
          FastLED.show();
          FastLED[0].clearLedData();
        }else if(customer == 'e'){
          for(int x = 0; x <= 6; x++){
             FastLED[x].clearLedData();
          }
          Space5return();
          FastLED.show();
          FastLED[5].clearLedData();
          ReturnLeds();
          FastLED.show();
          FastLED[0].clearLedData();
        }else if(customer == 'f'){
          for(int x = 0; x <= 6; x++){
             FastLED[x].clearLedData();
          }
          Space6return();
          FastLED.show();
          FastLED[6].clearLedData();
          ReturnLeds();
          FastLED.show();
          FastLED[0].clearLedData();
        }
}
}

void rainbow_march(uint8_t thisdelay, uint8_t deltahue) {     // The fill_rainbow call doesn't support brightness levels.

  uint8_t thishue = millis()*(255-thisdelay)/255;             // To change the rate, add a beat or something to the result. 'thisdelay' must be a fixed value.
  
  fill_rainbow(leds, NUM_LEDS, thishue, deltahue);            // Use FastLED's fill_rainbow routine.
  fill_rainbow(park1, PARK1_LEDS, thishue, deltahue);            // Use FastLED's fill_rainbow routine.
  fill_rainbow(park2, PARK2_LEDS, thishue, deltahue);            // Use FastLED's fill_rainbow routine.
  fill_rainbow(park3, PARK3_LEDS, thishue, deltahue);            // Use FastLED's fill_rainbow routine.
  fill_rainbow(park4, PARK4_LEDS, thishue, deltahue);            // Use FastLED's fill_rainbow routine.
  fill_rainbow(park5, PARK5_LEDS, thishue, deltahue);            // Use FastLED's fill_rainbow routine.
  fill_rainbow(park6, PARK6_LEDS, thishue, deltahue);            // Use FastLED's fill_rainbow routine.

}

void ParkLeds(){
  if(customer == '1'){
      for(int x = 0; x <= ONE; x++){
        if(x>=4){
        leds[x-4].setRGB(0, 0, 0);
        }
      leds[x].setRGB(255,255,255);
      FastLED[0].showLeds(BRIGHTNESS);
      FastLED.delay(125);
      }
  }
   else if(customer == '2'){
      for(int x = 0; x <= TWO; x++){
        if(x>=4){
          leds[x-4].setRGB(0, 0, 0);
          }
        leds[x].setRGB(255,255,255);
        FastLED[0].showLeds(BRIGHTNESS);
        FastLED.delay(125);
        }      
      }else if (customer == '3'){
        for(int x = 0; x <= THREE; x++){
        if(x>=4){
        leds[x-4].setRGB(0, 0, 0);
        }
      leds[x].setRGB(255,255,255);
      FastLED[0].showLeds(BRIGHTNESS);
      FastLED.delay(125);
      }
      }else if(customer == '4'){
        for(int x = 0; x <= FOUR; x++){
        if(x>=4){
        leds[x-4].setRGB(0, 0, 0);
        }
      leds[x].setRGB(255,255,255);
      FastLED[0].showLeds(BRIGHTNESS);
      FastLED.delay(125);
        }
      }else if(customer == '5'){
        for(int x = 0; x <= FIVE; x++){
        if(x>=4){
        leds[x-4].setRGB(0, 0, 0);
        }
      leds[x].setRGB(255,255,255);
      FastLED[0].showLeds(BRIGHTNESS);
      FastLED.delay(125);
        }
      }else if(customer == '6'){
        for(int x = 0; x <= SIX; x++){
        if(x>=4){
        leds[x-4].setRGB(0, 0, 0);
        }
      leds[x].setRGB(255,255,255);
      FastLED[0].showLeds(BRIGHTNESS);
      FastLED.delay(125);
        }
      }
}
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#define ONE         6
#define TWO         19
#define THREE       33
#define FOUR        110
#define FIVE        123
#define SIX         137
*/

void ReturnLeds(){
  if(customer == 'a'){
      for(int x = 6; x <= NUM_LEDS; x++){
        if(x>=6){
        leds[x-6].setRGB(0, 0, 0);
        }
      leds[x].setRGB(255,255,255);
      FastLED[0].showLeds(BRIGHTNESS);
      FastLED.delay(125);
      }
  }
   else if(customer == 'h'){
      for(int x = 19; x <= NUM_LEDS; x++){
        if(x>=6){
          leds[x-6].setRGB(0, 0, 0);
          }
        leds[x].setRGB(255,255,255);
        FastLED[0].showLeds(BRIGHTNESS);
        FastLED.delay(125);
        }      
      }else if (customer == 'c'){
        for(int x = 33; x <= NUM_LEDS; x++){
        if(x>=6){
        leds[x-6].setRGB(0, 0, 0);
        }
      leds[x].setRGB(255,255,255);
      FastLED[0].showLeds(BRIGHTNESS);
      FastLED.delay(125);
      }
      }else if(customer == 'd'){
        for(int x = 110; x <= NUM_LEDS; x++){
        if(x>=6){
        leds[x-6].setRGB(0, 0, 0);
        }
      leds[x].setRGB(255,255,255);
      FastLED[0].showLeds(BRIGHTNESS);
      FastLED.delay(125);
        }
      }else if(customer == 'e'){
        for(int x = 123; x <= NUM_LEDS; x++){
        if(x>=6){
        leds[x-6].setRGB(0, 0, 0);
        }
      leds[x].setRGB(255,255,255);
      FastLED[0].showLeds(BRIGHTNESS);
      FastLED.delay(125);
        }
      }else if(customer == 'f'){
        for(int x = 137; x <= NUM_LEDS; x++){
        if(x>=6){
        leds[x-6].setRGB(0, 0, 0);
        }
      leds[x].setRGB(255,255,255);
      FastLED[0].showLeds(BRIGHTNESS);
      FastLED.delay(125);
        }
      }
}


void Space1(){
  for(int x = PARK1_LEDS; x >= 5; x--){
    if(x<=20){
      park1[x+6].setRGB(0, 0, 0);
    }
    park1[x].setRGB(255,255,255);
    FastLED[1].showLeds(BRIGHTNESS);
    FastLED.delay(125);
  }   
  FastLED[1].clearLedData();
}

void Space2(){
  for(int j = PARK2_LEDS; j >= 5; j--){
    if(j<=20){
      park2[j+6].setRGB(0, 0, 0);
    }
    park2[j].setRGB(255,255,255);
    FastLED[2].showLeds(BRIGHTNESS);
    FastLED.delay(125);
  }   
  FastLED[2].clearLedData();
}

void Space3(){
  for(int x = PARK3_LEDS; x >= 5; x--){
    if(x<=20){
      park3[x+6].setRGB(0, 0, 0);
    }
    park3[x].setRGB(255,255,255);
    FastLED[3].showLeds(BRIGHTNESS);
    FastLED.delay(125);
  }
  FastLED[3].clearLedData();
}

void Space4(){
  for(int x = PARK4_LEDS; x >= 5 ; x--){
    if(x<=20){
      park4[x+6].setRGB(0, 0, 0);
    }
    park4[x].setRGB(255,255,255);
    FastLED[4].showLeds(BRIGHTNESS);
    FastLED.delay(125);
  }
  FastLED[4].clearLedData();
}

void Space5(){
  for(int x = PARK5_LEDS; x >= 5 ; x--){
    if(x<=20){
      park5[x+6].setRGB(0, 0, 0);
    }
    park5[x].setRGB(255,255,255);
    FastLED[5].showLeds(BRIGHTNESS);
    FastLED.delay(125);
  }
  FastLED[5].clearLedData();
}

void Space6(){
  for(int x = PARK6_LEDS; x >= 5; x--){
    if(x<=20){
      park6[x+6].setRGB(0, 0, 0);
    }
    park6[x].setRGB(255,255,255);
    FastLED[6].showLeds(BRIGHTNESS);
    FastLED.delay(125);
  }
  FastLED[6].clearLedData();
}

/////////////////////////////////////

void Space1return(){
  for(int x = 0; x < 17; x++){
    if(x>=6){
      park1[x-6].setRGB(0, 0, 0);
    }
    park1[x].setRGB(255,255,255);
    FastLED[1].showLeds(BRIGHTNESS);
    FastLED.delay(125);
  }
  FastLED[1].clearLedData();
}

void Space2return(){
  for(int j = 0; j < PARK2_LEDS; j++){
    if(j>=6){
      park2[j-6].setRGB(0, 0, 0);
    }
    park2[j].setRGB(255,255,255);
    FastLED[2].showLeds(BRIGHTNESS);
    FastLED.delay(125);
  }
  FastLED[2].clearLedData();
}

void Space3return(){
  for(int x = 0; x < PARK3_LEDS; x++){
    if(x>=6){
      park3[x-6].setRGB(0, 0, 0);
    }
    park3[x].setRGB(255,255,255);
    FastLED[3].showLeds(BRIGHTNESS);
    FastLED.delay(125);
  }
  FastLED[3].clearLedData();
}

void Space4return(){
  for(int x = 0; x < PARK4_LEDS; x++){
    if(x>=6){
      park4[x-6].setRGB(0, 0, 0);
    }
    park4[x].setRGB(255,255,255);
    FastLED[4].showLeds(BRIGHTNESS);
    FastLED.delay(125);
  }
  FastLED[4].clearLedData();
}

void Space5return(){
  for(int x = 0; x < PARK5_LEDS; x++){
    if(x>=6){
      park5[x-6].setRGB(0, 0, 0);
    }
    park5[x].setRGB(255,255,255);
    FastLED[5].showLeds(BRIGHTNESS);
    FastLED.delay(125);
  }
  FastLED[5].clearLedData();
}

void Space6return(){
  for(int x = 0; x < PARK6_LEDS; x++){
    if(x>=6){
      park6[x-6].setRGB(0, 0, 0);
    }
    park6[x].setRGB(255,255,255);
    FastLED[6].showLeds(BRIGHTNESS);
    FastLED.delay(125);
  }
  FastLED[6].clearLedData();
}
