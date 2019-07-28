#define SSID_NAME ""
#define SSID_PASSWORD ""
#define URL "http://192.168.0.10/capture"
#define API_URL "http://192.168.0.8/cozmomidi"
#define SLACK_URL "slack.com"
const String json = "{\"channel\":\"#m5stackxcozmo\",\"text\":\"say 皆さんこんにちは。僕はコズモです。本日はお忙しい中お集り頂きましてありがとうございます。僕も頑張りますので皆さま最後までお付き合いよろしくお願い致します。\"}";
const String json2 = "{\"channel\":\"#m5stackxcozmo\",\"text\":\"say 写真を撮影して写真から作った曲で僕が歌うよ。\"}";
const char* ca = "-----BEGIN CERTIFICATE-----\n" \
"MIIDrzCCApegAwIBAgIQCDvgVpBCRrGhdWrJWZHHSjANBgkqhkiG9w0BAQUFADBh\n" \
"MQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3\n" \
"d3cuZGlnaWNlcnQuY29tMSAwHgYDVQQDExdEaWdpQ2VydCBHbG9iYWwgUm9vdCBD\n" \
"QTAeFw0wNjExMTAwMDAwMDBaFw0zMTExMTAwMDAwMDBaMGExCzAJBgNVBAYTAlVT\n" \
"MRUwEwYDVQQKEwxEaWdpQ2VydCBJbmMxGTAXBgNVBAsTEHd3dy5kaWdpY2VydC5j\n" \
"b20xIDAeBgNVBAMTF0RpZ2lDZXJ0IEdsb2JhbCBSb290IENBMIIBIjANBgkqhkiG\n" \
"9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4jvhEXLeqKTTo1eqUKKPC3eQyaKl7hLOllsB\n" \
"CSDMAZOnTjC3U/dDxGkAV53ijSLdhwZAAIEJzs4bg7/fzTtxRuLWZscFs3YnFo97\n" \
"nh6Vfe63SKMI2tavegw5BmV/Sl0fvBf4q77uKNd0f3p4mVmFaG5cIzJLv07A6Fpt\n" \
"43C/dxC//AH2hdmoRBBYMql1GNXRor5H4idq9Joz+EkIYIvUX7Q6hL+hqkpMfT7P\n" \
"T19sdl6gSzeRntwi5m3OFBqOasv+zbMUZBfHWymeMr/y7vrTC0LUq7dBMtoM1O/4\n" \
"gdW7jVg/tRvoSSiicNoxBN33shbyTApOB6jtSj1etX+jkMOvJwIDAQABo2MwYTAO\n" \
"BgNVHQ8BAf8EBAMCAYYwDwYDVR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQUA95QNVbR\n" \
"TLtm8KPiGxvDl7I90VUwHwYDVR0jBBgwFoAUA95QNVbRTLtm8KPiGxvDl7I90VUw\n" \
"DQYJKoZIhvcNAQEFBQADggEBAMucN6pIExIK+t1EnE9SsPTfrgT1eXkIoyQY/Esr\n" \
"hMAtudXH/vTBH1jLuG2cenTnmCmrEbXjcKChzUyImZOMkXDiqw8cvpOp/2PV5Adg\n" \
"06O/nVsJ8dWO41P0jmP6P6fbtGbfYmbW0W5BjfIttep3Sp+dWOIrWcBAI+0tKIJF\n" \
"PnlUkiaY4IBIqDfv8NZ5YBberOgOzW6sRBc4L0na4UU+Krk2U886UAb3LujEV0ls\n" \
"YSEY1QSteDwsOoBrp+uvFRTp2InBuThs4pFsiv9kuXclVzDAGySj4dzp30d8tbQk\n" \
"CAUw7C29C79Fv1C5qfPrmAESrciIxpg0X40KPMbp1ZWVbd4=\n" \
"-----END CERTIFICATE-----\n";

#include <M5Stack.h>
#include <WiFi.h>
#include <HTTPClient.h>
// The setup() function runs once each time the micro-controller starts
void setup() {
  M5.begin();
  M5.Lcd.setBrightness(255);
  WiFi.begin(SSID_NAME, SSID_PASSWORD);
  M5.Lcd.print("Please WiFiConnect Press A button");
}
uint8_t buff[64 * 1024] = { 0 }; // 追加
// Add the main program code into the continuous loop() function
void loop() {
  M5.update();
  // if you want to use Releasefor("was released for"), use .wasReleasefor(int time) below
  if (M5.BtnA.wasReleased()) {
    slack(json);
  } else if (M5.BtnB.wasReleased()) {
    slack(json2);
    cam();
    HTTPClient http2;
    http2.begin(API_URL);
    int httpCode2 = http2.GET();
    Serial.printf("[HTTP2] GET... coode: %d\n", httpCode2);
    if (httpCode2 <= 0) {
        Serial.printf("[HTTP2]　GET... failed, error: %s\n",http2.errorToString(httpCode2).c_str());
    } else {
        if (httpCode2 != HTTP_CODE_OK) {
            Serial.printf("[HTTP2] Not OK!\n");
        }
    }
    http2.end();
  } else if (M5.BtnC.wasReleased()) {
    cam();
  } else if (M5.BtnB.wasReleasefor(700)) {
    M5.Lcd.clear(BLACK);
    M5.Lcd.setCursor(0, 0);
  }
}

void slack(const String message) {
    HTTPClient https;
    Serial.printf("[HTTPS] POST Start Slack\n");
    https.begin(SLACK_URL, 443, "/api/chat.postMessage", ca);
    https.addHeader("Content-Type", "application/json");
    https.addHeader("Authorization", "");
    int httpsCode = https.POST(message);
    Serial.printf("[HTTPS] POST END Slack\n");
    Serial.printf("[HTTPS] GET... coode: %d\n", httpsCode);
    if (httpsCode <= 0) {
        Serial.printf("[HTTPS]　GET... failed, error: %s\n",https.errorToString(httpsCode).c_str());
    } else {
        if (httpsCode != HTTP_CODE_OK) {
            Serial.printf("[HTTPS] Not OK!\n");
        }
    }
    https.end();
}

void cam() {
    HTTPClient http;
    Serial.print("[HTTP] begin...\n");
    http.begin(URL);
    Serial.print("[HTTP] GET...\n");
    int httpCode = http.GET();
    Serial.printf("[HTTP] GET... code: %d\n", httpCode);
    // HTTP header has been send and Server response header has been handled
    if (httpCode <= 0) {
      Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
    } else {
      if (httpCode != HTTP_CODE_OK) {
        Serial.printf("[HTTP] Not OK!\n");
      } else {
        // get lenght of document (is -1 when Server sends no Content-Length header)
        int len = http.getSize();
        Serial.printf("[HTTP] size: %d\n", len);
        if (len <= 0) {
          Serial.printf("[HTTP] Unknow content size: %d\n", len);
        } else {
          // create buffer for read
          uint8_t buff[len] = { 0 };
          // get tcp stream
          WiFiClient * stream = http.getStreamPtr();
          // read all data from server
          uint8_t* p = buff;
          int l = len;
          while (http.connected() && (l > 0 || len == -1)) {
            // get available data size
            size_t size = stream->available();

            if (size) {
              int s = ((size > sizeof(buff)) ? sizeof(buff) : size);
              int c = stream->readBytes(p, s);
              p += c;

              Serial.printf("[HTTP] read: %d\n", c);

              if (l > 0) {
                l -= c;
              }
            }
          }
          Serial.println();
          Serial.print("[HTTP] connection closed.\n");
          M5.Lcd.drawJpg(buff, len);
        }
      }
    }
    http.end();
}
