// -------------------- Bibliotheques ------------------------

#include <AFMotor.h>
#include <string.h>

// ---------------- Définition des moteurs --------------------
AF_DCMotor moteurAvantGauche(4);
AF_DCMotor moteurAvantDroit(3);
AF_DCMotor moteurDerriereDroite(2);
AF_DCMotor moteurDerriereGauche(1);
// ------------------------------------------------------------

// --------- Définition de la variable locale d'état ----------
// --- Configuration des États ---
enum Etat {
  ETAT_ATTENTE,
  ETAT_AVANCER,
  ETAT_RECULER,
  ETAT_GAUCHE,
  ETAT_DROITE};

Etat etatPresent = ETAT_ATTENTE;
// ------------------------------------------------------------

// ------------ Définition des capteurs ultrasons -------------
const int trigPinGauche = 52;
const int echoPinGauche = 53;
const int trigPinAvant = 44;
const int echoPinAvant = 45;
const int trigPinDroite = 38;
const int echoPinDroite = 39;
// ------------------------------------------------------------

const int vitesse = 200;
const int seuilDetection = 30;

// ------------------------ Autom ----------------------------
bool ModeAutom = false;
char systemeArrete = '1';  //Pour acquitter l'arret du systeme à l'ordi
// char arretSysteme = '1';
// ------------------------------------------------------------

// ---------------------- Temporisateur -----------------------
unsigned long tpsDepart = 0;
unsigned long tpsCible = 0;
// ------------------------------------------------------------

bool interruption = false;
bool enCoursAvance = false;

// -------------------------- setUps ---------------------------
void setup() {
  Serial.begin(9600);
  setupBluetooth();
  setupMoteur();
  setupCapteurs();
}

void setupBluetooth() {
  while (!Serial);  // Attendre que la connexion série soit prête

  // Communication série pour le module Bluetooth (port série 1 ou un autre port)
  Serial1.begin(9600);
}

void setupMoteur() {
  // Réglage de la vitesse des moteurs
  setVitesse(vitesse);
  // Arrêt initial des moteurs
  stopMoteurs();
}

void setupCapteurs(){
  pinMode(trigPinGauche, OUTPUT);
  pinMode(echoPinGauche, INPUT);
  pinMode(trigPinAvant, OUTPUT);
  pinMode(echoPinAvant, INPUT);
  pinMode(trigPinDroite, OUTPUT);
  pinMode(echoPinDroite, INPUT);
}
// -------------------------------------------------------------

void loop() {
  //Serial1.write(arretSysteme);
  systemeArrete = '0';
  
  static int indexI = 0;
  static int indexC = 0;
  if(ModeAutom){
    if(Serial1.available()) {
      String commande = Serial1.readStringUntil('\n');
      if (commande == "Y") ModeAutom = false;
    }
    autonome();
  }
  else{
    if(Serial1.available()) {//ça remplit le tableau tant qu'on reçoit quelque chose par bluetooth
      String commande = Serial1.readStringUntil('\n');
      //Serial.print("commande recu : ");
      commande.trim();
      //Serial.println(commande);
      if(commande.length()==1){
        traiter_commande(commande.c_str());
      }
      else{
        char buffer[commande.length() + 1];
        commande.toCharArray(buffer, sizeof(buffer));
        char* actions = strtok(buffer," ");
        while(actions != NULL){
          traiter_commande(actions);
          actions = strtok(NULL," ");
        }
      }
    }
  }
  //"Acquittement" de fin de tache
  if(systemeArrete == '1'){
    Serial1.write(systemeArrete);
  }
}

// ----------------------  gerer les commandes vocales ou manette  -----------------------
void traiter_commande(char* commande) {
  char fonction[50];
  int parametre = 0;
  int lu = sscanf(commande, "%49[^()]%*c%d", fonction, &parametre);  // essaie de lire fonction et paramètre
  if (lu == 2) {
    if (strcmp(fonction, "F") == 0) {
      avancer(parametre);
    } else if (strcmp(fonction, "B") == 0) {
      reculer(parametre);
    } else if (strcmp(fonction, "R") == 0) {
      tournerDroite(parametre);
    } else if (strcmp(fonction, "L") == 0) {
      tournerGauche(parametre);
    }
  }
  else if (lu == 1) {
    if (strcmp(fonction, "Z") == 0){
      ModeAutom = true;
    }
    else if (strcmp(fonction, "F") == 0) {
      if (stopObstacle(trigPinAvant, echoPinAvant, seuilDetection)){
        setVitesse(vitesse);
        stopMoteurs();
      }
      else{
        setVitesse(vitesse);
        avancer();
      }
    } else if (strcmp(fonction, "B") == 0) {
        setVitesse(vitesse);
        reculer();
    } else if (strcmp(fonction, "R") == 0) {
        setVitesse(vitesse);
        tournerDroite();
      
    } else if (strcmp(fonction, "L") == 0) {
      setVitesse(vitesse);
      tournerGauche();

    } else if (strcmp(fonction, "P") == 0) { //Diagoale avant droite ***
        diagonaleAVD();
      
    } else if (strcmp(fonction, "N") == 0) { //Diagoale arriere droite ***
        diagonaleARD();
    
    }else if (strcmp(fonction, "A") == 0) { //Diagoale avant gauche ***
        diagonaleAVG();

    }else if (strcmp(fonction, "W") == 0) { //Diagoale arriere gauche ***
        diagonaleARG();

    } else if (strcmp(fonction, "S") == 0) {
      setVitesse(vitesse);
      stopMoteurs();
    }
  }
  else {
    setVitesse(vitesse);
    stopMoteurs();
  }
}


// Fonction pour analyser et traiter une ligne contenant plusieurs commandes
void traiter_ligne_commandes(char* ligne) {
  char* commande = strtok(ligne, " ");
  while (commande != NULL) {
    traiter_commande(commande);
    commande = strtok(NULL, " ");
  }
}
// ------------------------------ Fin traiter commande --------------------------------

bool checkArretUrgence(char commande) {
  bool arretUrgence = false;
  if (commande == 'A') {
    arretUrgence = true;
  }
  return arretUrgence;
}

// Fonction pour interrompre l'exécution si un obstacle est trop proche
bool stopObstacle(const int trigPin, const int echoPin, int seuilDetection) {  // Seuil de détection en cm
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

// ------------------ Convertion des distances/angles en temps ------------------

float conversionDistTemps(float distance){ //distance en cm
  int duree = (distance / 80)*1000 ; // Temps en millisecondes. 82 represente la vitesse du robot lorsque setVitesse est à 2OO.
  return duree;
}
float conversionAngleTemps(float angle){
  int duree = (angle * 4720) / 360 ;
  return duree;
}
// ------------------------------------------------------------------------------

// ---------------------------- Gestion des moteurs -----------------------------

void setVitesse(int vitesse) {
  moteurAvantGauche.setSpeed(vitesse);
  moteurAvantDroit.setSpeed(vitesse);
  moteurDerriereDroite.setSpeed(vitesse);
  moteurDerriereGauche.setSpeed(vitesse);
}

void stopMoteurs() {
  //arretSysteme = '1';
  moteurAvantGauche.run(RELEASE);
  moteurAvantDroit.run(RELEASE);
  moteurDerriereDroite.run(RELEASE);
  moteurDerriereGauche.run(RELEASE);
}

void reculer() {
  //arretSysteme = '0';
  moteurAvantGauche.run(FORWARD);
  moteurAvantDroit.run(FORWARD);
  moteurDerriereDroite.run(FORWARD);
  moteurDerriereGauche.run(FORWARD);
}

void avancer() {
  //arretSysteme = '0';
  moteurAvantGauche.run(BACKWARD);
  moteurAvantDroit.run(BACKWARD);
  moteurDerriereDroite.run(BACKWARD);
  moteurDerriereGauche.run(BACKWARD);
}

void tournerDroite() {
  //arretSysteme = '0';
  moteurAvantGauche.run(BACKWARD);
  moteurAvantDroit.run(FORWARD);
  moteurDerriereDroite.run(FORWARD);
  moteurDerriereGauche.run(BACKWARD);
}

void tournerGauche() {
  //arretSysteme = '0';
  moteurAvantGauche.run(FORWARD);
  moteurAvantDroit.run(BACKWARD);
  moteurDerriereDroite.run(BACKWARD);
  moteurDerriereGauche.run(FORWARD);
}

// Définir les fonctions de commandes
void avancer(float distance) {
  //arretSysteme = '0';
  unsigned long duree = conversionDistTemps(distance);
  tpsDepart = millis();
  tpsCible = tpsDepart+duree;
  while(millis()<tpsCible){
    if(!stopObstacle(trigPinAvant, echoPinAvant, seuilDetection)){
      avancer();
    }
    else{
      stopMoteurs();
      systemeArrete = '1';
      return;
    }
  }
  systemeArrete = '1';
}

void reculer(float distance) {
  //arretSysteme = '0';
  unsigned long duree = conversionDistTemps(distance);
  tpsDepart = millis();
  tpsCible = tpsDepart+duree;
  while(millis()<tpsCible){
    reculer();
  }
  systemeArrete = '1';
}


void tournerDroite(float angle) {
  //arretSysteme = '0';
  unsigned long duree = conversionAngleTemps(angle);
  tpsDepart = millis();
  tpsCible = tpsDepart+duree;
  while(millis()<tpsCible){
    tournerDroite();
  }
  systemeArrete = '1';
}

void tournerGauche(float angle){
  //arretSysteme = '0';
  unsigned long duree = conversionAngleTemps(angle);
  tpsDepart = millis();
  tpsCible = tpsDepart+duree;
  while(millis()<tpsCible){
    tournerGauche();
  }
  systemeArrete = '1';

}

void diagonaleAVD(){
  moteurAvantGauche.setSpeed(0);
        moteurAvantDroit.setSpeed(255);
        moteurDerriereDroite.setSpeed(255);
        moteurDerriereGauche.setSpeed(0);
        avancer();
}

void diagonaleARD(){
  moteurAvantGauche.setSpeed(0);
        moteurAvantDroit.setSpeed(255);
        moteurDerriereDroite.setSpeed(255);
        moteurDerriereGauche.setSpeed(0);
        reculer();
}

void diagonaleAVG(){
  moteurAvantGauche.setSpeed(255);
        moteurAvantDroit.setSpeed(0);
        moteurDerriereDroite.setSpeed(0);
        moteurDerriereGauche.setSpeed(255);
        avancer();
}

void diagonaleARG(){
  moteurAvantGauche.setSpeed(255);
        moteurAvantDroit.setSpeed(0);
        moteurDerriereDroite.setSpeed(0);
        moteurDerriereGauche.setSpeed(255);
        reculer();
}
// ------------------------- Fin gestion des moteurs --------------------------

// --------------------------------- Autonome ---------------------------------


void autonome(){
  setVitesse(200);
  if(ModeAutom && !interruption){
    // --- Transition d’état ---
    switch(etatPresent){
      case ETAT_ATTENTE:
        if(!stopObstacle(trigPinAvant, echoPinAvant, seuilDetection*1.5)){
          etatPresent = ETAT_AVANCER;
        }
        else if(stopObstacle(trigPinAvant, echoPinAvant, seuilDetection) && 
          stopObstacle(trigPinDroite, echoPinDroite, seuilDetection) && 
          !stopObstacle(trigPinGauche, echoPinGauche, seuilDetection))
        {
          etatPresent = ETAT_GAUCHE;
        }
        else if(stopObstacle(trigPinAvant, echoPinAvant, seuilDetection) && 
          !stopObstacle(trigPinDroite, echoPinDroite, seuilDetection))
        {
          etatPresent = ETAT_DROITE;
        }
        else if(stopObstacle(trigPinAvant, echoPinAvant, seuilDetection) && 
          stopObstacle(trigPinDroite, echoPinDroite, seuilDetection) && 
          stopObstacle(trigPinGauche, echoPinGauche, seuilDetection))
        {
          etatPresent = ETAT_RECULER;
        }
        break;

      case ETAT_AVANCER:
        etatPresent = ETAT_ATTENTE;
        break;
      
      case ETAT_GAUCHE:
        etatPresent = ETAT_ATTENTE;
        break;
      
      case ETAT_DROITE:
        etatPresent = ETAT_ATTENTE;
        break;
      
      case ETAT_RECULER:
        etatPresent = ETAT_ATTENTE;
        break;

      default:
        etatPresent = ETAT_ATTENTE;
        break;
    }
  
    // --- Action selon l’état ---

    switch(etatPresent){
      case ETAT_ATTENTE:
        stopMoteurs();
        break;

      case ETAT_AVANCER:
        avancer(25);
        break;
      
      case ETAT_GAUCHE:
        reculer(25);
        tournerGauche(160);
        break;
      
      case ETAT_DROITE:
        reculer(25);
        tournerDroite(160);
        break;
      
      case ETAT_RECULER:
        reculer(25);
        break;
      
      default:
        stopMoteurs();
        break;
    }
  }
}