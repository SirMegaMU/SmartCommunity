#include <Arduino.h>
#include <ArduinoWebsockets.h>
#include <WiFi.h>
 
const char* ssid = "SirMegaMU"; //Enter SSID
const char* password = "1TurnKill"; //Enter Password
const char* websockets_server_host = "116.205.143.120"; //Enter server adress
const uint16_t websockets_server_port = 8080; // Enter server port
 
using namespace websockets;
 
void onMessageCallback(WebsocketsMessage message) {
    Serial.print("Got Message: ");
    Serial.println(message.data());
}
 
void onEventsCallback(WebsocketsEvent event, String data) {
    if(event == WebsocketsEvent::ConnectionOpened) {
        Serial.println("Connnection Opened");
    } else if(event == WebsocketsEvent::ConnectionClosed) {
        Serial.println("Connnection Closed");
    } else if(event == WebsocketsEvent::GotPing) {
        Serial.println("Got a Ping!");
    } else if(event == WebsocketsEvent::GotPong) {
        Serial.println("Got a Pong!");
    }
}
 
WebsocketsClient client;
void setup() {
    Serial.begin(115200);
    // Connect to wifi
    WiFi.begin(ssid, password);
 
    // Wait some time to connect to wifi
    for(int i = 0; i < 10 && WiFi.status() != WL_CONNECTED; i++) {
        Serial.print(".");
        delay(1000);
    }
    Serial.print("ESP Ready! Use 'http://");
    Serial.print(WiFi.localIP());
    Serial.print("/'");
    Serial.println("--------");
    
    // run callback when messages are received
    client.onMessage(onMessageCallback);
    
    // run callback when events are occuring
    client.onEvent(onEventsCallback);
 
    // Connect to server
    client.connect(websockets_server_host);        // no port (为什么？？？)
    // Send a message
    client.send("HELLO");
    Serial.println("send 'HELLO' ");
    // Send a ping
    client.ping();
}
 
void loop() {
    client.poll();
}
