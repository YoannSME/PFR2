#include <SoftwareSerial.h>

SoftwareSerial BTserial(10, 11); // RX, TX

long baudRates[] = {1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200};
int totalBauds = sizeof(baudRates) / sizeof(baudRates[0]);
bool baudFound = false;

void setup() {
  Serial.begin(115200);
  BTserial.begin(9600);
  Serial.println("Début du test des baud rates...");

  // for (int i = 0; i < totalBauds; i++) {
  //   long baud = baudRates[i];

  //   Serial.print("Test à "); 
  //   Serial.print(baud);
  //   Serial.println(" bauds...");

  //   BTserial.begin(baud);
  //   delay(1500);  // Attente pour stabiliser la communication

  //   BTserial.println("AT");  // Envoi de la commande AT
  //   delay(1000);  // Délai pour permettre au module de répondre

  //   if (BTserial.available()) {  
  //     String response = BTserial.readString();  
  //     Serial.print("Réponse reçue : "); 
  //     Serial.println(response);

  //     if (response.indexOf("OK") != -1) {
  //       Serial.print("Baud rate correct trouvé : "); 
  //       Serial.println(baud);
  //       baudFound = true;
  //       break;  // Arrêter le test dès qu'on trouve le bon baud rate
  //     }
  //   }

  //   BTserial.end();  // Fermer la communication avant de tester un autre baud rate
  // }

  // if (!baudFound) {
  //   Serial.println("Aucune réponse du module BT. Vérifiez les connexions !");
  // } else {
  //   Serial.println("Test terminé !");
  // }
}

void loop() {
  if (BTserial.available()) {  
      String response = BTserial.readString();  
      Serial.println(response);
  }
}
