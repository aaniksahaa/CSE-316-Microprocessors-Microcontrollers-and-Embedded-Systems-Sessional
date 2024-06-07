#include <WiFi.h>
#include <WebServer.h>
#include <WebSocketsServer.h>

#define LED 2

#define PWMA 13
#define AIN2 12
#define AIN1 14
#define STBY 27
#define BIN1 26
#define BIN2 25
#define PWMB 33

const char *ssid = "Aula_416";
const char *password = "sanaance";

WebServer server(80);
WebSocketsServer webSocket = WebSocketsServer(81);

boolean LEDonoff = false;
String JSONtxt;

#include "html_page.h"

void setup() {
  Serial.begin(115200);

  pinMode(LED, OUTPUT);

  pinMode(AIN1, OUTPUT);
  pinMode(AIN2, OUTPUT);
  pinMode(BIN1, OUTPUT);
  pinMode(BIN2, OUTPUT);
  pinMode(STBY, OUTPUT);
  pinMode(PWMA, OUTPUT);
  pinMode(PWMB, OUTPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  WiFi.mode(WIFI_STA);
  Serial.println();
  Serial.print("Local IP: ");
  Serial.println(WiFi.localIP());

  digitalWrite(LED, HIGH);

  server.on("/", webpage);

  server.begin();
  webSocket.begin();
  webSocket.onEvent(webSocketEvent);
}

void motorPower(int l, int r) {
  digitalWrite(STBY, 1);

  digitalWrite(AIN1, l < 0 ? 0 : 1);
  digitalWrite(AIN2, l < 0 ? 1 : 0);
  digitalWrite(BIN1, r < 0 ? 0 : 1);
  digitalWrite(BIN2, r < 0 ? 1 : 0);

  analogWrite(PWMA, abs(l));
  analogWrite(PWMB, abs(r));
}

void webpage() {
  server.send(200, "text/html", webpageCode);
}

int left = 0;
int right = 0;

void webSocketEvent(uint8_t num, WStype_t type, uint8_t *payload, size_t welength) {
  String payloadString = (const char *)payload;
  Serial.print("payloadString = ");
  Serial.println(payloadString);
  if (payloadString.startsWith("spd")) {
  
    int spaceIndex1 = payloadString.indexOf(' ');  
    int spaceIndex2 = payloadString.indexOf(' ', spaceIndex1 + 1);

    String num1String = payloadString.substring(spaceIndex1 + 1, spaceIndex2);
    String num2String = payloadString.substring(spaceIndex2 + 1);

    int value1 = atoi(num1String.c_str());
    int value2 = atoi(num2String.c_str());
    motorPower(value1, value2);
  }
  else if (payloadString == "w") motorPower(250, 250);
  else if (payloadString == "s") motorPower(-250, -250);
  else if (payloadString == "a") motorPower(-250, 250);
  else if (payloadString == "d") motorPower(250, -250);
  else if (payloadString == "") motorPower(0, 0);
}

void loop() {
  // motorPower(25, 25);
  // delay(1000);
  // motorPower(250, 250);
  // delay(1000);

  webSocket.loop();
  server.handleClient();



  // if (LEDonoff == false) digitalWrite(LED, LOW);
  // else digitalWrite(LED, HIGH);

  // String LEDstatus = "OFF";
  // if (LEDonoff == true) LEDstatus = "ON";
  // JSONtxt = "{\"LEDonoff\":\"" + LEDstatus + "\"}";
  // webSocket.broadcastTXT(JSONtxt);
}
