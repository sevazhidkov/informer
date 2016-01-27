// Code get from https://geektimes.ru/post/255738/
// Thanks @SLY_G

#include <LiquidCrystal.h>

LiquidCrystal lcd(4, 5, 10, 11, 12, 13);
 
int inb = 0;
int pos = 0;
int line = 0;
 
void setup() 
{
  Serial.begin(9600);
  lcd.begin(16, 2);
}
 
void loop() 
{
  lcd.setCursor(pos, line);
  if (Serial.available() > 0) {
    inb = Serial.read();
 
    if (char(inb) == '|') {
      pos = 0;
      line++;
    }
    else if (char(inb) == '&') {
      pos = 0;
      line = 0;
    }
    else {
      lcd.print(char(inb));
      pos++;
    }  
    lcd.setCursor(pos, line);
  }
}
