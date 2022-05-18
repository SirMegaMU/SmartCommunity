#include <esp32cam.h>
#include <WebServer.h>
#include <WiFi.h>

const char* WIFI_SSID = "SirMegaMU";
const char* WIFI_PASS = "1TurnKill";

const uint16_t port = 3389;
const char * host = "116.205.143.120";
 
WebServer server(80);
WiFiClient client;

static auto loRes = esp32cam::Resolution::find(800, 600);
static auto hiRes = esp32cam::Resolution::find(1600, 1200);

void serveJpg()
{
  auto frame = esp32cam::capture();
  if (frame == nullptr) {
    Serial.println("CAPTURE FAIL");
    server.send(503, "", "");
    return;
  }
  Serial.printf("CAPTURE OK %dx%d %db\n", frame->getWidth(), frame->getHeight(),
                static_cast<int>(frame->size()));

  server.setContentLength(frame->size());
  client.setContentLength(frame->size());
  server.send(200, "image/jpeg");
  WiFiClient wificlient = server.client();
  frame->writeTo(wificlient);
  frame->writeTo(client);
}

void handleJpgHi()
{
  if (!esp32cam::Camera.changeResolution(hiRes)) {
    Serial.println("SET-HI-RES FAIL");
  }
  serveJpg();
}

void setup()
{
  Serial.begin(115200);
  Serial.println();

  {
    using namespace esp32cam;
    Config cfg;
    cfg.setPins(pins::AiThinker);
    cfg.setResolution(hiRes);
    cfg.setBufferCount(2);
    cfg.setJpeg(80);

    bool ok = Camera.begin(cfg);
    Serial.println(ok ? "CAMERA OK" : "CAMERA FAIL");
  }
  WiFi.persistent(false);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  Serial.print("http://");
  Serial.println(WiFi.localIP());
  Serial.println("/cam-hi.jpg");
  
  while (!client.connect(host, port)) {
    Serial.println("Connection to host failed");
    delay(1000);
  }
  Serial.println("Connected to server successful!");
  client.print("http://");
  client.println(WiFi.localIP());
  
  server.on("/cam-hi.jpg", handleJpgHi);
  server.begin();
}

void loop()
{
  server.handleClient(); 
}
