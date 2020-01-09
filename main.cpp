#include <Arduino.h>

void setup() {
    init();
    Serial.begin(9600);
}


int main(){
  setup();
  int x = 0;

  while (1 == 1) {
    if (Serial.available() > 0) {
      char input = Serial.read();

      if (char(input) == 'T'){
        String strToBeOutputted = "{\"Value1\":" + String(x) + ",\"Value2\":" + String(x +1) + "}";
        Serial.println(strToBeOutputted);
        x++;
      }
    }
  }
  Serial.println("end");
  return 0;
}

// void setup(){
//   init();
//   Serial.begin(9600);
// }
//
// int main() {
//   setup();
//   int x = 0;
//
//   while (1) {
//     Serial.print("THIS");
//     Serial.println(x);
//     x++;
//     delay(1000);
//   }
//
//   return(0);
// }
