#include <WiFi.h>
#include <IOXhop_FirebaseESP32.h>
#include <WiFiClientSecure.h>
#include <DFRobot_MAX30102.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// Definir credenciais de Wi-Fi
#define WIFI_SSID "YOUR_WIFI_SSID"  // Substitua pelo seu SSID do Wi-Fi
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"  // Substitua pela sua senha do Wi-Fi

// Definir informações do Firebase
#define FIREBASE_HOST "YOUR-FIREBASE-HOST.firebaseio.com"  // Substitua pelo seu host do Firebase
#define FIREBASE_AUTH "YOUR-FIREBASE-AUTH"  // Substitua pela sua chave de autenticação do Firebase

// Definir chave de API do Google Geolocation
const char* GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY";  // Substitua pela sua chave de API do Google Geolocation
const char* googleApiHost = "YOUR-GOOGLE-API-HOST";  // Substitua pelo host da API do Google Geolocation
const int httpsPort = 443;  // Porta HTTPS

// Inicializar os sensores e outros componentes
DFRobot_MAX30102 particleSensor;
OneWire oneWire(17);  // Pino do DS18B20
DallasTemperature DS18B20(&oneWire);

WiFiClientSecure client;
const int buzzerPin = 12;
float tempC;

#define BUTTON_PIN 33

void connectToWiFi() {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

void setup() {
  Serial.begin(115200);
  
  // Conectar ao Wi-Fi
  connectToWiFi();
  
  // Inicializar Firebase e sensores
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  DS18B20.begin();
  
  // Inicializar o sensor MAX30102
  if (!particleSensor.begin()) {
    Serial.println("Erro ao inicializar o sensor MAX30102");
  }
  
  particleSensor.sensorConfiguration(50, SAMPLEAVG_4, MODE_MULTILED, SAMPLERATE_100, PULSEWIDTH_411, ADCRANGE_16384);
  pinMode(buzzerPin, OUTPUT);
  digitalWrite(buzzerPin, LOW);

  pinMode(BUTTON_PIN, INPUT_PULLUP);
  
  client.setInsecure();
}

void sendLocationToFirebase(String lat, String lng) {
  Firebase.setString("/X_caminho/lat", lat);
  Firebase.setString("/X_caminho/lng", lng);
}

void getGeolocation() {
  int numNetworks = WiFi.scanNetworks();
  
  if (numNetworks > 0) {
    String postData = "{\"wifiAccessPoints\": [";

    for (int i = 0; i < numNetworks; i++) {
      postData += "{\"macAddress\": \"" + WiFi.BSSIDstr(i) + "\", \"signalStrength\": " + String(WiFi.RSSI(i)) + "}";
      if (i < numNetworks - 1) {
        postData += ",";
      }
    }
    postData += "]}";

    if (!client.connect(googleApiHost, httpsPort)) {
      return;
    }

    // Enviar a requisição para a API de Geolocalização do Google
    client.println("POST /geolocation/v1/geolocate?key=" + String(GOOGLE_API_KEY) + " HTTP/1.1");
    client.println("Host: " + String(googleApiHost));
    client.println("Content-Type: application/json");
    client.println("Connection: close");
    client.print("Content-Length: ");
    client.println(postData.length());
    client.println();
    client.println(postData);

    while (client.connected()) {
      String line = client.readStringUntil('\n');
      if (line == "\r") {
        break;
      }
    }

    String response = client.readString();
    int latIndex = response.indexOf("\"lat\":");
    int lngIndex = response.indexOf("\"lng\":");

    if (latIndex != -1 && lngIndex != -1) {
      String lat = response.substring(latIndex + 6, response.indexOf(',', latIndex));
      String lng = response.substring(lngIndex + 6, response.indexOf('}', lngIndex));
      
      // Enviar coordenadas para o Firebase
      sendLocationToFirebase(lat, lng);
    }

    client.stop();
  }
}

void loop() {
  // Verificar conexão Wi-Fi e atualizar sensores
  bool wifiConnected = (WiFi.status() == WL_CONNECTED);
  int32_t SPO2, heartRate;
  int8_t SPO2Valid, heartRateValid;

  particleSensor.heartrateAndOxygenSaturation(&SPO2, &SPO2Valid, &heartRate, &heartRateValid);
  DS18B20.requestTemperatures();
  tempC = DS18B20.getTempCByIndex(0);
  
  Firebase.setFloat("/X_caminho/temperatura", tempC);
  Firebase.setInt("/X_caminho/cardiaca", heartRate);
  Firebase.setInt("/X_caminho/oxigenacao", SPO2);

  if (wifiConnected) {
    getGeolocation();
  } else {
    digitalWrite(buzzerPin, HIGH);
    delay(500);
    digitalWrite(buzzerPin, LOW);
  }

  // Verificar estado do botão de pânico
  if (digitalRead(BUTTON_PIN) == LOW) {
    Firebase.setBool("/X_caminho/botton", true);  // Enviar dado do botão ao Firebase
    while (digitalRead(BUTTON_PIN) == LOW);  // Esperar soltar o botão
  }
  delay(500);
}

