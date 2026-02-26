#include <SPI.h>
#include <SD.h>
#include <FunctionButtons.h>
#include <TimeLib.h>
#include <scd30_modbus.h>
#include <TinyTimer.h>

#define LED_SD_ACT 2
#define LED_SD_CARD 3
#define LED_REC_OK 10

#define EDA_IN A1
#define ACC_X_IN A6
#define ACC_Y_IN A5
#define ACC_Z_IN A4
#define ANALOG_IN_1 A8
#define ANALOG_IN_2 A7

#define POT_INCR 4
#define POT_UD 5
#define POT_H 6
#define POT_CS 14

#define CO2_TX1 0
#define CO2_RX1 1
#define CO2_TX2 7
#define CO2_RX2 8

#define BTN_REC_START 9
#define SW_MEDIA 11

#define BUFF_MAX 10

TinyTimer scheduler;
bool updateScheduler = false;
bool updateCO2Scheduler = false;

uint32_t start_millis;

FunctionButtons FB;
bool recording;

bool sd_card_present = false;
File eda_file;

bool eda_calibrated = false;
int eda_val = 0;

int acc_x_val = 0;
int acc_y_val = 0;
int acc_z_val = 0;

int vas_val = 0;

SCD30_Modbus scd30_1;
bool scd30_1_connected = true;
float scd30_1_temp = 0.0;
float scd30_1_co2 = 0.0;
float scd30_1_rh = 0.0;

SCD30_Modbus scd30_2;
bool scd30_2_connected = true;
float scd30_2_temp = 0.0;
float scd30_2_co2 = 0.0;
float scd30_2_rh = 0.0;

void store_sensor_data()
{
    digitalWrite(LED_SD_ACT, HIGH);

    String row = String(now()) + ";" + 
        String(millis()-start_millis) + ";" + 
        String(eda_val) + ";" + 
        String(vas_val) + ";" + 
        String(scd30_1_co2) + ";" + 
        String(scd30_1_rh) + ";" + 
        String(scd30_1_temp) + ";" + 
        String(scd30_2_co2) + ";" + 
        String(scd30_2_rh) + ";" +
        String(scd30_2_temp) + ";" +
        String(acc_x_val) + ";" +
        String(acc_y_val) + ";" + 
        String(acc_z_val) + "\n";
    if(eda_file)
    {
        eda_file.write(row.c_str());
    }

    digitalWrite(LED_SD_ACT, LOW);
}

void writeTestFile()
{
    digitalWrite(LED_SD_ACT, HIGH);
    String filename = "test_file.csv";
    eda_file = SD.open(filename.c_str(), FILE_WRITE);

    if(eda_file)
    {
        eda_file.write(String(now()).c_str());
    }

    digitalWrite(LED_SD_ACT, LOW);
}

void onRecFunction(uint8_t uid, uint8_t state)
{
    // Field calibration to align both sensors
    if (state == FunctionButtons::LONG_PRESS) {
        Serial.println("Start recalibration at 400 PPM (outside air)...");
        scd30_1.forceRecalibrationWithReference(400);
        scd30_2.forceRecalibrationWithReference(400);
        return;
    }
    
    // if no media is present, don't start or stop recording
    if (!sd_card_present)
    {
        FB.set_fbutton_state(uid, false);
        Serial.println("No media present!");
        //TODO: add media led blinking to inform about erronous state
        return;
    }
    
    if (state == FunctionButtons::FUNCTION_ON)
    {
        Serial.println("Start recording.");
        start_millis = millis();

        digitalWrite(LED_SD_ACT, HIGH);
        String filename = "sensordata_" + String(now()) + ".csv";
        eda_file = SD.open(filename.c_str(), FILE_WRITE);

        String header = String("Timestamp; Timestamp_ms; GSR; VAS; CO2_1; RH_1; Temp_1; CO2_2; RH_2; Temp_2; Acc_X; Acc_Y; Acc_Z") + "\n";
        if(eda_file)
        {
            eda_file.write(header.c_str());
        }

        digitalWrite(LED_SD_ACT, LOW);
        recording = true;
    }

    if (state == FunctionButtons::FUNCTION_OFF)
    {
        Serial.println("Stop recording.");

        digitalWrite(LED_SD_ACT, HIGH);
        recording = false;
        if (eda_file)
        {
            eda_file.flush();
            eda_file.close();
        }
        digitalWrite(LED_SD_ACT, LOW);

        clearSensorValues();
    }
}

void clearSensorValues()
{
    eda_val = 0;
    vas_val = 0;
    scd30_1_co2 = 0;
    scd30_1_rh = 0;
    scd30_1_temp = 0;
    scd30_2_co2 = 0;
    scd30_2_rh = 0;
    scd30_2_temp = 0;
    acc_x_val = 0;
    acc_y_val = 0;
    acc_z_val = 0;
    start_millis = millis();
}

void onSDCardChange(uint8_t uid, uint8_t state)
{
    if (state == FunctionButtons::BUTTON_UP)
    {
        Serial.println("SD Card ejected");
        recording = false;
        digitalWrite(LED_SD_CARD, LOW);
    }
    if (state == FunctionButtons::BUTTON_DOWN) {
        Serial.println("SD Card inserted");
        
        sd_card_present = BeginSDMedia();
        
        Serial.printf("SD Card detected: %d \n", sd_card_present);
        digitalWrite(LED_SD_CARD, sd_card_present);
    }
}

/**
 * Calibrate EDA Signal
 * @brief Get the analog value at around 400, this allows for some wiggle room. We expect the signal to go up since there is going to be sweat.
 * Needs work, nothing has been implemented thus far. Now it just gets the signal as low as possible
 * 
 * Make a seperate library for the chip that stores the current step position and the calibration logic
 * 
 */
void calibrate_eda()
{
    Serial.println("EDA Calibration started...");
    digitalWrite(POT_INCR, HIGH);
    digitalWrite(POT_UD, LOW);
    digitalWrite(POT_CS, LOW);

    //uint16_t preCal = analogRead(EDA_IN);
    uint16_t calValue = analogRead(EDA_IN);
    delayMicroseconds(10); // settle
    for(uint8_t i = 0; i<16; i++)
    {
        // step var resistor
        digitalWrite(POT_INCR, HIGH);
        delayMicroseconds(10);
        digitalWrite(POT_INCR, LOW);
        delayMicroseconds(40);
        // take reading, aim between 500-700
        calValue = analogRead(EDA_IN);
        if (calValue < 500 && calValue > 700) break;
    }
    
    Serial.println("EDA Calibration ended.");

    digitalWrite(POT_CS, HIGH);
    eda_calibrated = true;
}

void updateSensors(uint8_t tid)
{
    updateScheduler = true;
}

void updateCO2(uint8_t tid)
{
    updateCO2Scheduler = true;
}

time_t getRTC()
{
  return rtc_get();
}

bool BeginSDMedia()
{
    digitalWrite(LED_SD_ACT, HIGH);
    
    SD.begin(BUILTIN_SDCARD);
    SD.setMediaDetectPin(SW_MEDIA);
    
    digitalWrite(LED_SD_ACT, LOW);

    return SD.mediaPresent();

}

void setup()
{
    setSyncProvider(getRTC);
    // adjust time for GMT+1 resetting it to UTC, rtc lib quirk
    adjustTime(-3600);
    //adjustTime(-3600);

    analogReadResolution(10);

    pinMode(13, OUTPUT);
    digitalWrite(13, LOW);

    pinMode(ACC_X_IN, INPUT_DISABLE);
    pinMode(ACC_Y_IN, INPUT_DISABLE);
    pinMode(ACC_Z_IN, INPUT_DISABLE);
    pinMode(EDA_IN, INPUT_DISABLE);
    pinMode(POT_H, INPUT);
    pinMode(POT_CS, OUTPUT);
    pinMode(POT_INCR, OUTPUT);
    pinMode(POT_UD, OUTPUT);
    pinMode(ANALOG_IN_1, INPUT);

    pinMode(SW_MEDIA, INPUT);
    pinMode(LED_SD_ACT, OUTPUT);
    digitalWrite(LED_SD_ACT, LOW);
    pinMode(LED_SD_CARD, OUTPUT);
    digitalWrite(LED_SD_CARD, LOW);
    
    Serial.begin(115200);
    
    recording = false;
    //while(!Serial);

    //SCD30 sensors
    Serial.println("Initializing SCD30 sensors...");
    scd30_1.begin(&Serial1);
    scd30_2.begin(&Serial2);

    if (!scd30_1.setMeasurementInterval(2)){
        scd30_1_connected = false;
        Serial.println("SCD30_1 is not connected.");
    }
    if (!scd30_2.setMeasurementInterval(2)){
        scd30_2_connected = false;
        Serial.println("SCD30_2 is not connected.");
    }

    if (scd30_1_connected){
        scd30_1.selfCalibrationEnabled(true);
        scd30_1.setMeasurementInterval(2);
        scd30_1.startContinuousMeasurement();
    }
    if (scd30_2_connected){
        scd30_2.selfCalibrationEnabled(true);
        scd30_2.setMeasurementInterval(2);
        scd30_2.startContinuousMeasurement();
    }

    Serial.printf("SCD30_1: %d, SCD30_2: %d \n", scd30_1_connected, scd30_2_connected);

    // default ambient pressure = 1013.25 mBar
    // clean room might be at higher differential pressure
    // clean room suit might be at higher differential pressure due to ventilation static pressure
    // Serial.print(scd30_1.getAmbientPressureOffset());
    // Serial.println(scd30_2.getAmbientPressureOffset());
    
    FB.add_fbutton(SW_MEDIA, LED_SD_CARD, NULL, onSDCardChange);
    uint8_t rec_btn_id = FB.add_fbutton(BTN_REC_START, LED_REC_OK, onRecFunction, NULL, 5000);
    FB.set_blink_action(rec_btn_id, FunctionButtons::LONG_PRESS, 200);

    scheduler.setInterval(100, updateSensors);  // every 100ms - 10Hz
    scheduler.setInterval(500, updateCO2);  // co2 has an update every 2s, 500ms is generous

    sd_card_present = BeginSDMedia();

    Serial.printf("SD Card: %d \n", sd_card_present);

    digitalWrite(LED_SD_CARD, sd_card_present);

    // adjust time for GMT+1 resetting it to UTC, like why is it not already...!?
    adjustTime(-3600);
    // Taking DST in account when neccesary
    //adjustTime(-3600);
}

// benchmarking used with oscilloscope for profiling
bool bmPinState = false;
void toggleDebugBenchmark()
{
    bmPinState = !bmPinState;
    digitalWrite(13, bmPinState);
}

void loop()
{
    scheduler.run();
    FB.run();

    if(recording)
    {
        while(!eda_calibrated)
        {
            calibrate_eda();
        }

        // updateScheduler is set to true every x ms, handled by the scheduler
        // this sets the update frequency of all the analog sensors
        // the CO2 sensors only update at .5Hz, seperate scheduler to reduce the
        // modbus calls for dataready
        if(updateCO2Scheduler){  //at 2Hz
            if (scd30_1_connected && scd30_1.dataReady()){
                if (scd30_1.read())
                { 
                    scd30_1_co2 = scd30_1.CO2;
                    scd30_1_rh = scd30_1.relative_humidity;
                    scd30_1_temp = scd30_1.temperature;
                }
            }
            if (scd30_2_connected && scd30_2.dataReady()){
                if (scd30_2.read())
                { 
                    scd30_2_co2 = scd30_2.CO2;
                    scd30_2_rh = scd30_2.relative_humidity;
                    scd30_2_temp = scd30_2.temperature;
                }
            }
            updateCO2Scheduler = false;
        }
        
        if(updateScheduler)  //at 50Hz
        {
            // converting sensor data to practical values
            vas_val = digitalRead(ANALOG_IN_1);
            eda_val = 1023-analogRead(EDA_IN);
            acc_x_val = analogRead(ACC_X_IN)-512;
            acc_y_val = analogRead(ACC_Y_IN)-512;
            acc_z_val = analogRead(ACC_Z_IN)-512;
            
            store_sensor_data();
            
            updateScheduler = false;
        }
    }
}