# HDS-Project
In 2024, I developed an innovative project focused on creating a wearable vest designed to monitor the vital signs of employees in large companies. The device is capable of measuring parameters such as heart rate, oxygenation, and body temperature, providing a comprehensive view of the user's health in real time.

In addition to monitoring vital signs, the vest also performs indoor location tracking through triangulation with Wi-Fi routers, ensuring more efficient control of employee movement within the corporate environment. All collected data is sent to a central database, where it is displayed on an interactive dashboard, providing a clear and accurate overview of employee health conditions.

Both the wearable and the dashboard feature emergency tools that assist in quickly assisting employees in abnormal situations, such as critical variations in vital signs. The project also used machine learning to learn from each employee's historical vital sign data, allowing for more accurate interpretation in both emergencies and normal conditions.


## Table of Contents

* [Hardware](#hardware)
* [Software](#software)
* [Compatibility](#compatibility)


## Hardware

sensores.ino
- programmed in ARDUINO IDE
- Sensores: MAX30102, DS18b20
- Sends data via Wifi
- Used Firebase Realtime Database
- Getting current location with Google MAPS API

## Software

credfirebase.json
- Firebase credentials

app.py
- Get Firebase credentials
- Get data from Firebase in JSON format
- Used lib Streamlit to create Dashboard Local Host
- Get with Streamlit a view Map in Realtime
- Sends warnigs to Whatsapp Web used to lib pywhatkit
- Save history in dados.json
- Save history warnigs in PyWhatKit_D8.txt

dados.json
- It has the entire history of vital signs data

machine.py
- Code in machine learning to distinguish normal vital signs, bringing a range of normality
- Get data from dados.json

## Compatibility

MCU                | Work Well    
------------------ | :----------: 
Arduino uno        |      √                
Mega2560        |      √                     
Leonardo        |      √                              
ESP32        |      √                                
ESP8266        |      √                              
FireBeetle-M0        |      √                             

## Credits

Created by ME - Henrique-Muhlmann 



