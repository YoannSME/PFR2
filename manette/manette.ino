#include <AFMotor.h>

// Définition des moteurs avec l'Adafruit Motor Shield
AF_DCMotor moteurAvantGauche(4); 
AF_DCMotor moteurAvantDroit(3); 
AF_DCMotor moteurDerriereDroite(2); 
AF_DCMotor moteurDerriereGauche(1);

void setup() {
  Serial.begin(9600);  // Communication série pour le moniteur série (port USB)
  Serial.println("Initialisation des moteurs...");
  
  // Communication série pour le module Bluetooth (port série 1 ou un autre port)
  Serial1.begin(9600);  // Utilisation de Serial1 pour la communication Bluetooth

  // Réglage de la vitesse des moteurs
  setVitesse(255);

  // Arrêt initial des moteurs
  stopMoteurs();
}

void loop() {
  if (Serial1.available() > 0) {  // Lire la commande envoyée par Bluetooth
    char commande = Serial1.read();  // Lire la commande envoyée par le module Bluetooth
    Serial.println(commande);
    if (!stopObstacle() && commande == 'F') {
      Serial.println("Forward");
      // Avancer
      avancer();
    } 
    else if (!stopObstacle() && commande == 'B') {
      Serial.println("Backward");
      // Reculer
      reculer();
    } 
    else if (!stopObstacle() && commande == 'L') {
      Serial.println("Left");
      // Tourner à gauche
      tournerGauche();
    }
    else if (!stopObstacle() && commande == 'R') {
      Serial.println("Right");
      // Tourner à droite
      tournerDroite();
    } 
    else if(!stopObstacle() && commande == 'S'){
      stopMoteurs();
    }

  }
}
// Fonction pour interrompre execution si obstacle
void stopObstacle(){


}

// Fonction pour avancer
void avancer() {
  moteurAvantGauche.run(FORWARD);
  moteurAvantDroit.run(FORWARD);
  moteurDerriereDroite.run(FORWARD);
  moteurDerriereGauche.run(FORWARD);
}

// Fonction pour reculer
void reculer() {
  moteurAvantGauche.run(BACKWARD);
  moteurAvantDroit.run(BACKWARD);
  moteurDerriereDroite.run(BACKWARD);
  moteurDerriereGauche.run(BACKWARD);
}

// Fonction pour tourner à gauche
void tournerGauche() {
  moteurAvantGauche.run(BACKWARD);
  moteurAvantDroit.run(FORWARD);
  moteurDerriereDroite.run(FORWARD);
  moteurDerriereGauche.run(BACKWARD);
}

// Fonction pour tourner à droite
void tournerDroite() {
  moteurAvantGauche.run(FORWARD);
  moteurAvantDroit.run(BACKWARD);
  moteurDerriereDroite.run(BACKWARD);
  moteurDerriereGauche.run(FORWARD);
}

// Fonction pour régler la vitesse des moteurs
void setVitesse(int vitesse) {
  moteurAvantGauche.setSpeed(vitesse);
  moteurAvantDroit.setSpeed(vitesse);
  moteurDerriereDroite.setSpeed(vitesse);
  moteurDerriereGauche.setSpeed(vitesse);
}

// Fonction pour arrêter les moteurs
void stopMoteurs() {
  moteurAvantGauche.run(RELEASE);
  moteurAvantDroit.run(RELEASE);
  moteurDerriereDroite.run(RELEASE);
  moteurDerriereGauche.run(RELEASE);
}