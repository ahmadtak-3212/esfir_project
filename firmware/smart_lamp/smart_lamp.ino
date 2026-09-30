#include <SPI.h>
#include <WiFi.h>

const uint16_t RESPONSE_TIMEOUT = 6000;
const uint16_t IN_BUFFER_SIZE = 3500; //size of buffer to hold HTTP request
const uint16_t OUT_BUFFER_SIZE = 1000; //size of buffer to hold HTTP response
const uint16_t JSON_BODY_SIZE = 3000;
char request[IN_BUFFER_SIZE];
char response[OUT_BUFFER_SIZE]; //char array buffer to hold HTTP request


const int PWM_R_PIN = 2;
const int PWM_G_PIN = 3;
const int PWM_B_PIN = 4;
const int PWM_FREQ = 10000;
const int pwm_r_channel = 0;
const int pwm_g_channel = 1;
const int pwm_b_channel = 2;
const int RESPONSE_INTERVAL = 5000;

const char NETWORK[] = "StataCenter";
const char PASSWORD[] = "";

uint8_t channel = 1; //network channel on 2.4 GHz
byte bssid[] = {0x04, 0x95, 0xE6, 0xAE, 0xDB, 0x41}; //6 byte MAC address of AP you're targeting.

int colors[3];
int response_timer;

void initWIFI() {
  //if using regular connection use line below:
  WiFi.begin(NETWORK, PASSWORD);
  //if using channel/mac specification for crowded bands use the following:
  //WiFi.begin(network, password, channel, bssid);

  uint8_t count = 0; //count used for Wifi check times
  Serial.print("Attempting to connect to ");
  Serial.println(NETWORK);
  while (WiFi.status() != WL_CONNECTED && count < 12) {
    delay(500);
    Serial.print(".");
    count++;
  }
  delay(2000);
  if (WiFi.isConnected()) { //if we connected then print our IP, Mac, and SSID we're on
    Serial.println("CONNECTED!");
    Serial.printf("%d:%d:%d:%d (%s) (%s)\n", WiFi.localIP()[3], WiFi.localIP()[2],
                  WiFi.localIP()[1], WiFi.localIP()[0],
                  WiFi.macAddress().c_str() , WiFi.SSID().c_str());
    delay(500);
  } else { //if we failed to connect just Try again.
    Serial.println("Failed to Connect :/  Going to restart");
    Serial.println(WiFi.status());
    ESP.restart(); // restart the ESP (proper way)
  }
}

void getColors() {
  request[0] = '\0'; //set 0th byte to null
  int offset = 0; //reset offset variable for sprintf-ing
  offset += sprintf(request + offset, "GET http://608dev-2.net/sandbox/sc/ahmadtak/server/server.py  HTTP/1.1\r\n");
  offset += sprintf(request + offset, "Host: 608dev-2.net\r\n");
  offset += sprintf(request + offset, "\r\n");
  do_http_request("608dev-2.net", request, response, OUT_BUFFER_SIZE, RESPONSE_TIMEOUT, false);
  Serial.printf("\nRESPONSE: %s", response);
  char * pch;
  int i = 0;
  pch = strtok(response, ",");
  while (pch != NULL) {
    colors[i] = atoi(pch);
    i++;
    pch = strtok (NULL, ",");
  }
}
void setColor(int red, int green, int blue) {
  
  ledcWrite(pwm_r_channel, (255 - red));
  ledcWrite(pwm_g_channel, (int) (0.90*(255 - green)));
  ledcWrite(pwm_b_channel, 255 - blue);
}

void setup() {
  Serial.begin(115200);           // Set up serial port
  delay(100);
  initWIFI();
  pinMode(PWM_R_PIN, OUTPUT);
  pinMode(PWM_G_PIN, OUTPUT);
  pinMode(PWM_B_PIN, OUTPUT);
  ledcSetup(pwm_r_channel, PWM_FREQ, 8);
  ledcAttachPin(PWM_R_PIN, pwm_r_channel);

  ledcSetup(pwm_g_channel, PWM_FREQ, 8);
  ledcAttachPin(PWM_G_PIN, pwm_g_channel);

  ledcSetup(pwm_b_channel, PWM_FREQ, 8);
  ledcAttachPin(PWM_B_PIN, pwm_b_channel);
  response_timer = millis();
}

void loop() {
  if (millis() - response_timer > RESPONSE_INTERVAL) {
    // put your main code here, to run repeatedly:
    getColors();
    Serial.printf("\n(%d, %d, %d)",  colors[0],colors[1], colors[2] );
    setColor(colors[0], colors[1], colors[2]);
    response_timer = millis();
  }
}
