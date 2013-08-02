
// Get 1-wire Library here: http://www.pjrc.com/teensy/td_libs_OneWire.html
#include <OneWire.h>

#include <TM1638.h>

TM1638 module(5, 3, 4 );

int current = 0;


#define ONE_WIRE_BUS_PIN 2

OneWire ds(ONE_WIRE_BUS_PIN);

// http://www.hacktronics.com/Tutorials/arduino-1-wire-address-finder.html

byte probe01[8] = { 0x28, 0x09, 0xD9, 0xDD, 0x04, 0x00, 0x00, 0x27 }; 
byte probe02[8] = { 0x28, 0x5D, 0x78, 0xDE, 0x04, 0x00, 0x00, 0xA3 };
byte probe03[8] = { 0x28, 0x50, 0x05, 0xDE, 0x04, 0x00, 0x00, 0x68 };

void setup() {
  // start serial port to show results
  Serial.begin(9600);  
}

void loop() {
  checkButtons();
  updateDisplay();
  delay(100);
}

void checkButtons(void) {
  int buttons = module.getButtons();
  if (buttons != 0) {
    Serial.println(buttons);
    if (buttons == 0b00000001) {
      current = 0;
      module.setLEDs(0x0100);
    } else if (buttons == 0b00000010) {
      current = 1;
      module.setLEDs(0x0200);
    } else if (buttons == 0b00000100) {
      current = 2;
      module.setLEDs(0x0400);
    }
  }
}

void updateDisplay(void) {
  byte (*currAdd)[8];
  if (current == 0) {
    currAdd = &probe01;
  } else if (current == 1) {
    currAdd = &probe02;
  } else if (current == 2) {
    currAdd = &probe03;
  }
  float temperature = getTemp(*currAdd);
  module.setDisplayToSignedDecNumber(temperature*10,2,false);
}


// Getting the temperature from a specific sensor.
// Modified version of http://bildr.org/2011/07/ds18b20-arduino/

float getTemp(byte addr[8]){
	//returns the temperature from one DS18S20 in DEG Celsius
	byte data[12];

	if ( OneWire::crc8( addr, 7) != addr[7]) {
		Serial.println("CRC is not valid!");
		return -1000;
	}

	if ( addr[0] != 0x10 && addr[0] != 0x28) {
		Serial.print("Device is not recognized");
		return -1000;
	}

	ds.reset();
	ds.select(addr);
	ds.write(0x44,1); // start conversion, with parasite power on at the end

	byte present = ds.reset();
	ds.select(addr);
	ds.write(0xBE); // Read Scratchpad


	for (int i = 0; i < 9; i++) { // we need 9 bytes
		data[i] = ds.read();
	}

	ds.reset_search();

	byte MSB = data[1];
	byte LSB = data[0];

	float tempRead = ((MSB << 8) | LSB); //using two's compliment
	float TemperatureSum = tempRead / 16;

	return TemperatureSum;

}
