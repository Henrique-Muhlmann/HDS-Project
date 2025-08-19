# HDS-Project
> **Health Data System** - Intelligent Corporate Health Monitoring System

[![Arduino](https://img.shields.io/badge/Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white)](https://www.arduino.cc/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Firebase](https://img.shields.io/badge/Firebase-039BE5?style=for-the-badge&logo=Firebase&logoColor=white)](https://firebase.google.com/)
[![Machine Learning](https://img.shields.io/badge/Machine%20Learning-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)

## About the Project
In 2024, I developed an innovative project focused on creating a wearable vest designed to monitor the vital signs of employees in large companies. The device is capable of measuring parameters such as heart rate, oxygenation, and body temperature, providing a comprehensive view of the user's health in real time.

In addition to monitoring vital signs, the vest also performs indoor location tracking through triangulation with Wi-Fi routers, ensuring more efficient control of employee movement within the corporate environment. All collected data is sent to a central database, where it is displayed on an interactive dashboard, providing a clear and accurate overview of employee health conditions.

Both the wearable and the dashboard feature emergency tools that assist in quickly assisting employees in abnormal situations, such as critical variations in vital signs. The project also used machine learning to learn from each employee's historical vital sign data, allowing for more accurate interpretation in both emergencies and normal conditions.

### Key Features

- **Vital Signs Monitoring**: Heart rate, oxygen saturation, and body temperature
- **Indoor Location Tracking**: Real-time Wi-Fi triangulation positioning
- **Interactive Dashboard**: Centralized visualization of all collected data
- **Emergency System**: Automatic WhatsApp alerts for critical situations
- **Machine Learning**: Predictive analysis based on individual employee history
- **Secure Storage**: Firebase database with complete historical data

## System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   IoT Vest      │───▶│   Firebase DB    │───▶│   Web Dashboard     │
│  (Sensors)      │    │  (Real-time)     │    │   (Streamlit)       │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
         │                        │                         │
         │                        ▼                         ▼
         │              ┌──────────────────┐    ┌─────────────────────┐
         │              │  Machine Learning │    │   Alert System     │
         │              │   (AI Analysis)   │    │   (WhatsApp Bot)    │
         │              └──────────────────┘    └─────────────────────┘
         │
         ▼
┌─────────────────┐
│  Location       │
│  (WiFi + GPS)   │
└─────────────────┘
```

## 📋 Table of Contents

- [Installation](#-installation)
- [Hardware](#-hardware)
- [Software](#-software)
- [Compatibility](#compatibility)
- [Project Structure](#-project-structure)
- [Author](#-author)

## 🚀 Installation

### Prerequisites
- Arduino IDE 1.8+
- Python 3.8+
- Firebase account
- MAX30102 and DS18B20 sensors
- Required Arduino libraries (see Hardware section)

### 1. Hardware Setup
```bash
# Clone the repository
git clone https://github.com/Henrique-Muhlmann/HDS-Project.git
cd HDS-Project

# Open sensores.ino in Arduino IDE
# Install required libraries
# Configure WiFi and Firebase credentials
# Upload to microcontroller
```

### 2. Software Setup
```bash
# Install Python dependencies
pip install streamlit firebase-admin pywhatkit pandas numpy scikit-learn

# Configure credentials file
cp credfirebase.json.example credfirebase.json
# Edit with your Firebase credentials

# Run dashboard
streamlit run app.py
```

## 🔧 Hardware

### Main Components
- **Microcontroller**: ESP32/ESP8266 (recommended)
- **Heart Rate Sensor**: MAX30102 (SpO2 + Heart Rate)
- **Temperature Sensor**: DS18B20 (Waterproof)
- **Connectivity**: Integrated WiFi
- **Power Supply**: Li-Po 3.7V battery

### Required Arduino Libraries
The `sensores.ino` file requires the following libraries:

```cpp
#include <WiFi.h>                    // ESP32 WiFi connectivity
#include <IOXhop_FirebaseESP32.h>    // Firebase real-time database
#include <WiFiClientSecure.h>        // Secure WiFi connections
#include <DFRobot_MAX30102.h>        // Heart rate and SpO2 sensor
#include <OneWire.h>                 // OneWire protocol for DS18B20
#include <DallasTemperature.h>       // Temperature sensor library
```

### Firmware Features (`sensores.ino`)
- Developed in Arduino IDE
- WiFi communication with Firebase
- Google Maps API integration for geolocation
- Data collection every 5 seconds
- Automatic reconnection system
- Real-time sensor reading and transmission

## 💻 Software

### Main Dashboard (`app.py`)
- **Framework**: Streamlit for responsive web interface
- **Database**: Firebase Realtime Database
- **Visualization**: Real-time charts and interactive maps
- **Alerts**: WhatsApp integration via PyWhatKit
- **History**: Local storage in `dados.json`

### Machine Learning System (`machine.py`)
- **Algorithm**: Statistical analysis for anomaly detection
- **Data**: Personalized history per employee
- **Output**: Dynamic normality ranges
- **Accuracy**: Continuous improvement with more data

### Data Structure
```json
{
    {
        "nome": "henrique",
        "cardiaca": 107,
        "oxigenacao": 92,
        "temperatura": 37.0
    }, 
}
```

## Compatibility

| Microcontroller | Status | Notes |
|----------------|--------|-------|
| Arduino Uno    | ✅ Works | Limited (no native WiFi) |
| Mega2560       | ✅ Works | Limited (no native WiFi) |
| Leonardo       | ✅ Works | Limited (no native WiFi) |
| **ESP32**      | ✅ **Recommended** | WiFi + Bluetooth integrated |
| **ESP8266**    | ✅ **Recommended** | WiFi integrated |
| FireBeetle-M0  | ✅ Works | Good performance |

> **💡 Tip**: For best experience, use ESP32 or ESP8266 with integrated WiFi.

## 📁 Project Structure

```
HDS-Project/
├── 📁 hardware/
│   └── sensores.ino          # Microcontroller code
├── 📁 software/
│   ├── app.py                # Main dashboard
│   ├── machine.py            # ML algorithms
│   └── credfirebase.json     # Firebase credentials
├── 📁 data/
│   ├── dados.json            # Data history
│   └── PyWhatKit_D8.txt      # Alert logs
└──  📁 docs/
    └── README.md             # Documentation

```


## 👨‍💻 Author

**Henrique Muhlmann**
- GitHub: [@Henrique-Muhlmann](https://github.com/Henrique-Muhlmann)
- LinkedIn: [Henrique Muhlmann](https://www.linkedin.com/in/henrique-amaral-muhlmann-3b28042b6/)

---

If this project helped you, consider giving it a star!
