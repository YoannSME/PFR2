#include <AFMotor.h>

// Définition des moteurs avec l'Adafruit Motor Shield
AF_DCMotor moteurAvantGauche(4); 
AF_DCMotor moteurAvantDroit(3); 
AF_DCMotor moteurDerriereDroite(2); 
AF_DCMotor moteurDerriereGauche(1);

// Définition des capteurs ultrasons
const int trigPinGauche = 52;
const int echoPinGauche = 53;
const int trigPinAvant = 44;
const int echoPinAvant = 45;
const int trigPinDroite = 38;
const int echoPinDroite = 39;

const int seuilDetection = 20;

void setup() {
  Serial.begin(9600);  // Communication série pour le moniteur série (port USB)
  Serial.println("Initialisation des moteurs...");
  
  // Communication série pour le module Bluetooth (port série 1 ou un autre port)
  Serial1.begin(9600);  // Utilisation de Serial1 pour la communication Bluetooth

  // Configuration des broches des capteurs
  pinMode(trigPinGauche, OUTPUT);
  pinMode(echoPinGauche, INPUT);
  pinMode(trigPinAvant, OUTPUT);
  pinMode(echoPinAvant, INPUT);
  pinMode(trigPinDroite, OUTPUT);
  pinMode(echoPinDroite, INPUT);

  // Réglage de la vitesse des moteurs
  setVitesse(200);

  // Arrêt initial des moteurs
  stopMoteurs();
}


void loop() {
  static char statutRob = 'S';
  if (Serial1.available() > 0) {  // Lire la commande envoyée par Bluetooth
    char commande = Serial1.read();
    Serial.println(commande);

    
    if (commande == 'F') {
      if (stopObstacle(trigPinAvant, echoPinAvant, seuilDetection)) {
      stopMoteurs();
    }
    else{
      avancer();
    }
    }
    else if (commande == 'B') { // voir pour arreter avec stopObstacle()
      statutRob = 'B';
      reculer();
    }
    else if (!stopObstacle(trigPinGauche, echoPinGauche, seuilDetection) && commande == 'L') {
      statutRob = 'L';
      tournerGauche();
    }
    else if (!stopObstacle(trigPinDroite, echoPinDroite, seuilDetection) && commande == 'R') {
      statutRob = 'R';
      tournerDroite();
    } 
    else if (commande == 'S') {
      statutRob = 'S';
      stopMoteurs();
    }
  }
}

// Fonction pour interrompre l'exécution si un obstacle est trop proche
bool stopObstacle(const int trigPin, const int echoPin, int seuilDetection) {// Seuil de détection en cm
  int distance = getDistance(trigPin, echoPin);

  // Si un obstacle est détecté devant ou sur les côtés, on stoppe
  return (distance < seuilDetection);
}

// Fonction pour mesurer la distance avec un capteur ultrason
long getDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  long duration = pulseIn(echoPin, HIGH, 30000);
  return (duration > 0) ? (duration * 0.034 / 2) : 400;
}

// Fonction pour avancer
void reculer() {
  moteurAvantGauche.run(FORWARD);
  moteurAvantDroit.run(FORWARD);
  moteurDerriereDroite.run(FORWARD);
  moteurDerriereGauche.run(FORWARD);
}

// Fonction pour reculer
void avancer() {
  moteurAvantGauche.run(BACKWARD);
  moteurAvantDroit.run(BACKWARD);
  moteurDerriereDroite.run(BACKWARD);
  moteurDerriereGauche.run(BACKWARD);
}

// Fonction pour tourner à gauche
void tournerDroite() {
  moteurAvantGauche.run(BACKWARD);
  moteurAvantDroit.run(FORWARD);
  moteurDerriereDroite.run(FORWARD);
  moteurDerriereGauche.run(BACKWARD);
}

// Fonction pour tourner à droite
void tournerGauche() {
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