/*
 * Library: https://github.com/bolderflight/MPU9250
Basic_I2C.ino
Brian R Taylor
brian.taylor@bolderflight.com

Copyright (c) 2017 Bolder Flight Systems

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/
/*
 * Updated by Ahmad Shamshiri on July 09, 2018 for Robojax.com
 * in Ajax, Ontario, Canada
 * watch instrucion video for this code:
For this sketch you need to connect:
VCC to 5V and GND to GND of Arduino
SDA to A4 and SCL to A5

S20A is 3.3V voltage regulator MIC5205-3.3BM5
*/

#include "MPU9250.h"
#include <stdbool.h>
// an MPU9250 object with the MPU-9250 sensor on I2C bus 0 with address 0x68
MPU9250 IMU(Wire,0x68);
int status;

bool help_flag = false;
float accel_x_data, accel_y_data, accel_z_data;
int help_start_time;
int help_end_time;

void setup() {
    // serial to display data
    Serial.begin(9600);
    while(!Serial) {}

    // start communication with IMU
    status = IMU.begin();
    if (status < 0) {
        Serial.println("IMU initialization unsuccessful");
        Serial.println("Check IMU wiring or try cycling power");
        Serial.print("Status: ");
        Serial.println(status);
    }
}

void loop() {
    // read the sensor
    IMU.readSensor();
    // display the data
    accel_x_data = IMU.getAccelX_mss();
    accel_y_data = IMU.getAccelY_mss();
    accel_z_data = IMU.getAccelZ_mss();

    if(accel_y_data > -6.f) {
        help_end_time = millis();
    }
    else {
        help_flag = false;
        help_start_time = millis();
        help_end_time = millis();
    }

    if(help_end_time - help_start_time > 6000) {
        help_flag = true;
    }

    if(help_flag == false) {
        Serial.print("AccelX: ");
        Serial.print(accel_x_data,6);
        Serial.print("  ");
        Serial.print("AccelY: ");
        Serial.print(accel_y_data,6);
        Serial.print("  ");
        Serial.print("AccelZ: ");
        Serial.println(accel_z_data,6);
    }
    else {
        if(help_end_time - help_start_time < 11000) {
            Serial.println("HELP");
        }
        else {
            Serial.println("HELP2");
        }
    }
    /*
    Serial.print("GyroX: ");
    Serial.print(IMU.getGyroX_rads(),6);
    Serial.print("  ");
    Serial.print("GyroY: ");
    Serial.print(IMU.getGyroY_rads(),6);
    Serial.print("  ");
    Serial.print("GyroZ: ");
    Serial.println(IMU.getGyroZ_rads(),6);

    Serial.print("MagX: ");
    Serial.print(IMU.getMagX_uT(),6);
    Serial.print("  ");
    Serial.print("MagY: ");
    Serial.print(IMU.getMagY_uT(),6);
    Serial.print("  ");
    Serial.print("MagZ: ");
    Serial.println(IMU.getMagZ_uT(),6);

    Serial.print("Temperature in C: ");
    Serial.println(IMU.getTemperature_C(),6);
    Serial.println();
    */
    delay(1000);
}
