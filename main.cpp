#include <Arduino.h>

int main() {
    init();
    Serial.begin(9600);


    pinMode(13, OUTPUT);
    int numberTimes = 100;
    int x = 0;

    while(1==1){
        char input = Serial.read();
        if (input == 'T') {
            String strToBeOutputted = "{";
            strToBeOutputted += "'Value1':" + String(x) + "," + "\"Value2\":" + String(x +1) + "}";
            Serial.println(strToBeOutputted);
            Serial.println("NOTICED");
            x++;
        }
       
    }

    Serial.println("end");

    return 0;
}
