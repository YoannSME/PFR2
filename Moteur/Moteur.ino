#include <AFMotor.h>
#include <stdio.h>

AF_DCMotor moteurAvantGauche(4); 
AF_DCMotor moteurAvantDroit(3); 
AF_DCMotor moteurDerriereDroite(2); 
AF_DCMotor moteurDerriereGauche(1);

//Définition de la variable globale de mesure du temps
static unsigned long timeStamp = 0;

//Définition de la variable globale de definition de la fonction en utilisation
char etatSysteme ='S';

uint8_t vitesseReelle = 0;
uint8_t vitessePMW = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("Initialisation des moteurs...");

  // Réglage de la vitesse des moteurs
  setVitesse(vitessePMW);

  // Arrêt initial des moteurs
  stopMoteurs();

  // Initialisation du chrono
  timeStamp = millis();
}

void loop() {
  forward(150);
  right(90);

}

int vitesseToPMW(float vitesse) {  //Prend en entrée une vitesse en m/s et retourne la vitesse en pmw (de 0 à 255)
    float vmax = 1.26; // Vitesse max en m/s
    int pwm_max = 255;

    if (vitesse <= 0) return 0;
    if (vitesse >= vmax) return pwm_max;

    return (int)(vitesse / vmax * pwm_max);
}

// Fonction pour régler la vitesse de tous les moteurs
void setVitesse(int vitesse) {
  moteurAvantGauche.setSpeed(vitesse);
  moteurAvantDroit.setSpeed(vitesse);
  moteurDerriereDroite.setSpeed(vitesse);
  moteurDerriereGauche.setSpeed(vitesse);
}

void definirVitesse (float vitessePhysique){
  vitesseReelle = vitessePhysique;
  vitessePMW = vitesseToPMW(vitesseReelle);
}

// Fonction pour arrêter tous les moteurs
void stopMoteurs() {
  for (int i = vitessePMW; i>0; i-- ){ // Arret progressif des moteurs
    setVitesse(i);
  }
  moteurAvantGauche.run(RELEASE);
  moteurAvantDroit.run(RELEASE);
  moteurDerriereDroite.run(RELEASE);
  moteurDerriereGauche.run(RELEASE);
}

void arretUrgence() {
  vitessePMW = 0;
  vitesseReelle = 0;
  setVitesse(0);
  moteurAvantGauche.run(RELEASE);
  moteurAvantDroit.run(RELEASE);
  moteurDerriereDroite.run(RELEASE);
  moteurDerriereGauche.run(RELEASE);
}

float conversionDistTemps(float distance) { // distance en cm
  // Convertir la vitesse réelle de m/s en cm/ms pour faciliter le calcul
  float vitesseCmMs = vitesseReelle * 100 / 1000; // Conversion de m/s en cm/ms
  
  if (vitesseCmMs <= 0) {
    return 0; // Éviter la division par zéro si le robot est à l'arrêt
  }
  
  float duree = distance / vitesseCmMs; // Temps en millisecondes
  return duree;
}

float conversionAngleTemps(float angle){
  int duree = (angle * 4720) / 360 ;
  return duree;
}

// NOTE: Les fonctions forward() et backward() sont inversées à cause du branchement des moteurs.
// Faire reculer le robot
void backward(float distance) {

  //Si aucune autre fonction n'est en cours, on définit le temps correspondant au parcours effectué
  if((timeStamp<=0) && (etatSysteme == 'S')){
    timeStamp = millis() + conversionDistTemps(distance);
    etatSysteme = 'B';
  }

  if ((timeStamp > 0) && (etatSysteme == 'B')){
    // Activation des moteurs en avant
    moteurAvantGauche.run(FORWARD);
    moteurAvantDroit.run(FORWARD);
    moteurDerriereDroite.run(FORWARD);
    moteurDerriereGauche.run(FORWARD);
    
    //Si le temps d'execution correspond au temps de parcours, on arrête
    if(millis() >= timeStamp){
      stopMoteurs();
      timeStamp = 0;
      etatSysteme = 'S';
    }
  }
}

// Faire avancer le robot
void forward(float distance) {

  //Si aucune autre fonction n'est en cours, on définit le temps correspondant au parcours effectué
  if((timeStamp<=0) && (etatSysteme == 'S')){
    timeStamp = millis() + conversionDistTemps(distance);
    etatSysteme = 'F';
  }

  if ((timeStamp > 0) && (etatSysteme == 'F')){
    // Activation des moteurs en arrière
    moteurAvantGauche.run(BACKWARD);
    moteurAvantDroit.run(BACKWARD);
    moteurDerriereDroite.run(BACKWARD);
    moteurDerriereGauche.run(BACKWARD);
    
    //Si le temps d'execution correspond au temps de parcours, on arrête
    if(millis() >= timeStamp){
      stopMoteurs();
      timeStamp = 0;
      etatSysteme = 'S';
    }
  }
}

// Fonction pour tourner à gauche
void right(float angle) {

  //Si aucune autre fonction n'est en cours, on définit le temps correspondant au parcours effectué
  if((timeStamp<=0) && (etatSysteme == 'S')){
    timeStamp = millis() + conversionAngleTemps(angle);
    etatSysteme = 'R';
  }
  if ((timeStamp >= 0) && (etatSysteme == 'R')){
    moteurAvantGauche.run(BACKWARD);
    moteurDerriereGauche.run(BACKWARD);
    moteurAvantDroit.run(FORWARD);
    moteurDerriereDroite.run(FORWARD);

    //Si le temps d'execution correspond au temps de parcours, on arrête
    if(millis() >= timeStamp){
      stopMoteurs();
      timeStamp = 0;
      etatSysteme = 'S';
    }
  }
}


// Fonction pour tourner à droite
void left(float angle) {

  //Si aucune autre fonction n'est en cours, on définit le temps correspondant au parcours effectué
  if((timeStamp<=0) && (etatSysteme == 'S')){
    timeStamp = millis() + conversionAngleTemps(angle);
    etatSysteme = 'L';
  }
  if ((timeStamp >= 0) && (etatSysteme == 'L')){
    moteurAvantGauche.run(FORWARD);
    moteurDerriereGauche.run(FORWARD);
    moteurAvantDroit.run(BACKWARD);
    moteurDerriereDroite.run(BACKWARD);

    //Si le temps d'execution correspond au temps de parcours, on arrête
    if(millis() >= timeStamp){
      stopMoteurs();
      timeStamp = 0;
      etatSysteme = 'S';
    }
  }
}

void demiTour() {
  right(180);
}

void zigzag(float distanceTotale, float angle, float pas) { // entree : distance à parcourir, angle, pas du zigzag
 
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
}

void carre(float longueur) {
  for (int i = 0; i < 4; i++) {
    forward(longueur);
    right(90);
  }
}
