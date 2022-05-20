#include <Adafruit_CircuitPlayground.h>
#include <Wire.h>
#include <SPI.h>

#define TWO_PI 6.28318530717f
int color_rainbow[10][3] = {{255,0,0}, {255,153,0}, {204,255,0}, {51,255,0}, {0,255,102}, {0,255,255}, {0,102,255}, {51,0,255}, {204,0,255}, {255,0,153}};

void setup() {
  CircuitPlayground.begin();              // initialize the CP library
  CircuitPlayground.strip.setBrightness(128);

}

// the sound producing function (a brute force way to do it)
void makeTone (unsigned char speakerPin, int frequencyInHertz, long timeInMilliseconds) {
  int x;   
  long delayAmount = (long)(1000000/frequencyInHertz);
  long loopTime = (long)((timeInMilliseconds*1000)/(delayAmount*2));
  for (x=0; x<loopTime; x ++) {        // the wave will be symetrical (same time high & low)
     analogWrite(speakerPin,10);   // Set the pin high
     delayMicroseconds(delayAmount);  // and make the tall part of the wave
     analogWrite(speakerPin,0);    // switch the pin back to low
     delayMicroseconds(delayAmount);  // and make the bottom part of the wave
  }  
}

void loop() {
  // put your main code here, to run repeatedly:
  if(CircuitPlayground.rightButton()) {   // play when we press the right button
    for(int i=98; i < 114; i++) {
      CircuitPlayground.clearPixels();
      int freq = 440*pow(2, (i-69) / 12.0);
      CircuitPlayground.strip.setPixelColor(i % 10, color_rainbow[i%10][0], color_rainbow[i%10][1], color_rainbow[i%10][2]);
      CircuitPlayground.strip.show();
      makeTone(A0, freq, 80);
      delay(40);
      if(CircuitPlayground.leftButton()) {
        break;
      }
      CircuitPlayground.clearPixels();
    }
  }

}
