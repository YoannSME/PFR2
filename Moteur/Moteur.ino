#include <AFMotor.h>
#include <stdio.h>

AF_DCMotor moteurAvantGauche(4); 
AF_DCMotor moteurAvantDroit(3); 
AF_DCMotor moteurDerriereDroite(2); 
AF_DCMotor moteurDerriereGauche(1);

void setup() {
  Serial.begin(9600);
  Serial.println("Initialisation des moteurs...");

  // Réglage de la vitesse des moteurs
  setVitesse(200);

  // Arrêt initial des moteurs
  stopMoteurs();
}

void loop() {
  //Serial.print("teste");
  //avancer(400);
  //delay(200);
  //zigzag(300, 50, 50); // entree : distance à parcourir, angle, pas du zigzag
  //carre(100);
  right(90);
  delay(200);

}

// Fonction pour régler la vitesse de tous les moteurs
void setVitesse(int vitesse) {
  moteurAvantGauche.setSpeed(vitesse);
  moteurAvantDroit.setSpeed(vitesse);
  moteurDerriereDroite.setSpeed(vitesse);
  moteurDerriereGauche.setSpeed(vitesse);
}

// Fonction pour arrêter tous les moteurs
void stopMoteurs() {
  moteurAvantGauche.run(RELEASE);
  moteurAvantDroit.run(RELEASE);
  moteurDerriereDroite.run(RELEASE);
  moteurDerriereGauche.run(RELEASE);
}

float conversionDistTemps(float distance){
  int duree = (distance / 80)*1000 ; // Temps en millisecondes. 82 represente la vitesse du robot lorsque setVitesse est à 2OO.
  /*
  Serial.print("Temps calculé : ");
  Serial.print(duree);
  Serial.println(" ms");
  */
  return duree;
}

float conversionAngleTemps(float angle){
  int duree = (angle * 4720) / 360 ;
  return duree;
}

// NOTE: Les fonctions forward() et backward() sont inversées à cause du branchement des moteurs.
// Faire reculer le robot
void backward(float distance){
  Serial.print("Le robot avance de ");
  Serial.print(distance);
  Serial.println(" cm");
  
  // Activation des moteurs en avant
  moteurAvantGauche.run(FORWARD);
  moteurAvantDroit.run(FORWARD);
  moteurDerriereDroite.run(FORWARD);
  moteurDerriereGauche.run(FORWARD); 
  
  delay(conversionDistTemps(distance));
  stopMoteurs();
}

// Faire avancer le robot
void forward(float distance) {
  Serial.print("Le robot recule de ");
  Serial.print(distance);
  Serial.println(" cm");

  // Activation des moteurs en arrière
  moteurAvantGauche.run(BACKWARD);
  moteurAvantDroit.run(BACKWARD);
  moteurDerriereDroite.run(BACKWARD);
  moteurDerriereGauche.run(BACKWARD);
  
  delay(conversionDistTemps(distance));
  stopMoteurs();

}

// Fonction pour tourner à droite
void left(float angle) {
  Serial.print("Le robot tourne à droite de ");
  Serial.print(angle);
  Serial.println(" degrés");

  moteurAvantGauche.run(FORWARD);
  moteurDerriereGauche.run(FORWARD);
  moteurAvantDroit.run(BACKWARD);
  moteurDerriereDroite.run(BACKWARD);

  delay(conversionAngleTemps(angle));
  stopMoteurs();
}

// Fonction pour tourner à gauche
void right(float angle) {
  Serial.print("Le robot tourne à gauche de ");
  Serial.print(angle);
  Serial.println(" degrés");

  moteurAvantGauche.run(BACKWARD);
  moteurDerriereGauche.run(BACKWARD);
  moteurAvantDroit.run(FORWARD);
  moteurDerriereDroite.run(FORWARD);

  delay(conversionAngleTemps(angle));
  stopMoteurs();
}

void demiTour() {
  Serial.println("Demi-tour...");
  right(180);
}

void zigzag(float distanceTotale, float angle, float pas) { // entree : distance à parcourir, angle, pas du zigzag
  Serial.println("Début du zig-zag...");
  
  float distanceParcourue = 0;
  bool direction = true; // true = gauche, false = droite

  while (distanceParcourue < distanceTotale) {
    forward(pas);  // Avancer d'un pas
    distanceParcourue += pas;

    if (direction) {
      left(angle);  // Tourner à gauche
    } else {
      right(angle); // Tourner à droite
    }

    direction = !direction; // Inverser la direction pour le prochain zigzag
  }

  Serial.println("Fin du zig-zag.");
}

void carre(float longueur) {
  for (int i = 0; i < 4; i++) {
    forward(longueur);
    right(90);
  }
}
