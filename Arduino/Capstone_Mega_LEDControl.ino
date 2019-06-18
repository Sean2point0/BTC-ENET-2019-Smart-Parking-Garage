#include <FastLED.h>

#define LED_PIN     2
#define PARK1_PIN   4
#define PARK2_PIN   7
#define PARK3_PIN   8
#define PARK4_PIN   6
#define PARK5_PIN   5
#define PARK6_PIN   3
#define ENTRANCE    12
#define EXIT        13

#define ONE         7
#define TWO         19
#define THREE       33
#define FOUR        110
#define FIVE        123
#define SIX         137

#define NUM_LEDS    228
#define SPACE1_LEDS 20
#define PARK_LEDS   24
#define LEDDELAY    150
#define BRIGHTNESS  64            //max is 255
#define LED_TYPE    WS2812B
#define COLOR_ORDER GRB

uint8_t max_bright = 255;         // Overall brightness definition. It can be changed on the fly.
char customer;                         

struct CRGB leds[NUM_LEDS];
struct CRGB park[6][PARK_LEDS];

void ParkLeds(int spaceNum);
void Space(int spaceNum);
void rainbow_march(uint8_t thisdelay, uint8_t deltahue);
void SpaceReturn(int spaceNum);
void ReturnLeds(int spaceNum);

int LEDCountToSpace[] = {ONE, TWO, THREE, FOUR, FIVE, SIX};

void setup(){
  delay(3000);
  Serial.begin(9600);
  pinMode(ENTRANCE, OUTPUT);
  pinMode(EXIT, OUTPUT);
  digitalWrite(ENTRANCE, LOW);
  digitalWrite(EXIT, HIGH);
  LEDS.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
  LEDS.addLeds<LED_TYPE, PARK1_PIN, COLOR_ORDER>(park[0], PARK_LEDS);
  LEDS.addLeds<LED_TYPE, PARK2_PIN, COLOR_ORDER>(park[1], PARK_LEDS);
  LEDS.addLeds<LED_TYPE, PARK3_PIN, COLOR_ORDER>(park[2], PARK_LEDS);
  LEDS.addLeds<LED_TYPE, PARK4_PIN, COLOR_ORDER>(park[3], PARK_LEDS);
  LEDS.addLeds<LED_TYPE, PARK5_PIN, COLOR_ORDER>(park[4], PARK_LEDS);
  LEDS.addLeds<LED_TYPE, PARK6_PIN, COLOR_ORDER>(park[5], PARK_LEDS);

  FastLED.setBrightness(max_bright);
  set_max_power_in_volts_and_milliamps(5, 1000);              // FastLED 2.1 Power management set at 5V, 500mA
}

void loop(){
  while(Serial.available()==0){    
    rainbow_march(200, 10);
    FastLED.show();
  }
  if(Serial.available()){
    for(int x = 0; x <= 6; x++){
      FastLED[x].clearLedData();
    }
    customer = Serial.read();
    if(isDigit(customer)){
      int parkSpot = customer - '1';
      digitalWrite(ENTRANCE, HIGH);
      delay(1000);
      ParkLeds(parkSpot);
      FastLED.show();
      FastLED[0].clearLedData();
      Space(parkSpot);
      FastLED.show();
      FastLED[parkSpot].clearLedData();
    }else if(isAlpha(customer)){
      int parkSpot = customer - 'a';
      SpaceReturn(parkSpot);
      FastLED.show();
      FastLED[parkSpot].clearLedData();
      while(Serial.available()==0);
      Serial.read();
      ReturnLeds(parkSpot);
      FastLED.show();
      FastLED[0].clearLedData();
    }
  }
}

void rainbow_march(uint8_t thisdelay, uint8_t deltahue) {     // The fill_rainbow call doesn't support brightness levels.

  uint8_t thishue = millis()*(255-thisdelay)/255;             // To change the rate, add a beat or something to the result. 'thisdelay' must be a fixed value.
  
  fill_rainbow(leds, NUM_LEDS, thishue, deltahue);             // Use FastLED's fill_rainbow routine.
  for (int x = 0; x < 6; x++){
    fill_rainbow(park[x], PARK_LEDS, thishue, deltahue);            // Use FastLED's fill_rainbow routine.
  }
}

void ParkLeds(int spaceNum){
  for(int x = 0; x <= LEDCountToSpace[spaceNum]; x++){
    if(x>=4){
      leds[x-4].setRGB(0, 0, 0);
    }
    leds[x].setRGB(255,255,255);
    FastLED[0].showLeds(BRIGHTNESS);
    FastLED.delay(LEDDELAY);
    if (x == 18){
      digitalWrite(ENTRANCE, LOW);
    }
  }
}

void ReturnLeds(int spaceNum){
  for(int x = LEDCountToSpace[spaceNum] - 4; x <= NUM_LEDS; x++){
    if(x>=6){
      leds[x-6].setRGB(0, 0, 0);
    }
    leds[x].setRGB(255,255,255);
    FastLED[0].showLeds(BRIGHTNESS);
    FastLED.delay(LEDDELAY);
    if (x == (NUM_LEDS - 68)){
      digitalWrite(EXIT, LOW);
      delay(1000);
    }else if (x == (NUM_LEDS - 50)){
      digitalWrite(EXIT, HIGH);
      delay(1000);
    }
  }
}

void Space(int spaceNum){
  for(int x = PARK_LEDS; x >= 5; x--){
    if(x<=18){
      park[spaceNum][x+6].setRGB(0, 0, 0);
    }
    park[spaceNum][x].setRGB(255,255,255);
    FastLED[spaceNum + 1].showLeds(BRIGHTNESS);
    FastLED.delay(LEDDELAY);
  }
  FastLED[spaceNum + 1].clearLedData();
  if (spaceNum == 0){
    digitalWrite(ENTRANCE, LOW);
  }
}

void SpaceReturn(int spaceNum){
  int count;
  if (spaceNum == 1){
    count = SPACE1_LEDS;
  }else{
    count = PARK_LEDS;
  }
  for(int x = 0; x < count; x++){
    if(x>=6){
      park[spaceNum][x-6].setRGB(0, 0, 0);
    }
    park[spaceNum][x].setRGB(255,255,255);
    FastLED[spaceNum + 1].showLeds(BRIGHTNESS);
    FastLED.delay(LEDDELAY);
  }
  FastLED[spaceNum + 1].clearLedData();
}
