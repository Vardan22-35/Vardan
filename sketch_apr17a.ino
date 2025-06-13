#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include <LiquidCrystal_I2C.h>

// Ստեղծում ենք ADXL345 օբյեկտ
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(123);

// Ստեղծում ենք LCD օբյեկտ (հասցե՝ 0x27, չափ՝ 16x2)
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  // Սերիական մոնիտոր, եթե ուզես տեսնել
  Serial.begin(9600);

  // LCD
  lcd.init();
  lcd.backlight();

  // ADXL345 սկիզբ
  if(!accel.begin()) {
    lcd.setCursor(0, 0);
    lcd.print("Սարքը չկա!");
    while(1);
  }

  lcd.setCursor(0, 0);
  lcd.print("ADXL345 OK");
  delay(1000);
  lcd.clear();
}

void loop() {
  sensors_event_t event;
  accel.getEvent(&event);

  // Արժեքների կլորացում
  float x = event.acceleration.x;
  float y = event.acceleration.y;
  float z = event.acceleration.z;

  // LCD ցուցադրում
  lcd.setCursor(0, 0);
  lcd.print("X:");
  lcd.print(x, 1);
  lcd.print(" Y:");
  lcd.print(y, 1);

  lcd.setCursor(0, 1);
  lcd.print("Z:");
  lcd.print(z, 1);
  lcd.print(" m/s^2  ");

Serial.print(x, 2);
  Serial.print(",");
  Serial.print(y, 2);
  Serial.print(",");
  Serial.println(z, 2);
  
  delay(500); // Թարմացման դադարը
}
