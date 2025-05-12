#include <AFMotor.h>
#include <string.h>

// ---------------- Définition des moteurs --------------------
AF_DCMotor moteurAvantGauche(4); 
AF_DCMotor moteurAvantDroit(3); 
AF_DCMotor moteurDerriereDroite(2); 
AF_DCMotor moteurDerriereGauche(1);
// ------------------------------------------------------------

// ------------ Définition des capteurs ultrasons -------------
const int trigPinGauche = 52;
const int echoPinGauche = 53;
const int trigPinAvant = 44;
const int echoPinAvant = 45;
const int trigPinDroite = 38;
const int echoPinDroite = 39;
// ------------------------------------------------------------

// --------------------- Initialisation -----------------------
static unsigned long timeStamp = 0;
char etatSysteme = 'S';
bool interruption = false;
const int seuilDetection = 20;
// -------------------------------------------------------------

void setup() {
  Serial.begin(9600);
  setupBluetooth();
  setupMoteur();
  setupCapteurs();
}
// ---------------------- Creation des setup() -----------------------
void setupBluetooth(){
  while (!Serial); // Attendre que la connexion série soit prête
  Serial.println("Connexion au bluetooth...");
  // Communication série pour le module Bluetooth (port série 1 ou un autre port)
  Serial1.begin(9600); 
}

void setupMoteur(){
  Serial.println("Initialisation des moteurs...");
  // Réglage de la vitesse des moteurs
  setVitesse(200);
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
// --------------------------------------------------------------------

void loop() {
  static char ligne[1024];
  static int index = 0;
  
  if (Serial1.available()) {
    char commande = Serial1.read();
    interruption = commande == 'S';
    if (commande != '\n' && index < sizeof(ligne) - 1) {
      ligne[index++] = commande;
    } else if (commande == '\n' || index >= sizeof(ligne) - 1) {
      ligne[index] = '\0';
      traiter_commande(ligne);  //lancerCommande
      index = 0;
    }
  }
}

// ----------------------  gerer les commandes vocales ou manette -----------------------
void traiter_commande(char* commande) {
  char fonction[50];
  int parametre;
  int lu = sscanf(commande, "%49[^()]%*c%d", fonction, &parametre);  // essaie de lire fonction et paramètre
  if (lu == 2) {
    if (strcmp(fonction, "F") == 0) {
      etatSysteme = 'F';
      if (stopObstacle(trigPinAvant, echoPinAvant, seuilDetection))
        stopMoteurs();
      else
        avancer(parametre);
    } else if (strcmp(fonction, "B") == 0) {
      etatSysteme = 'B';
      reculer(parametre);
    } else if (strcmp(fonction, "R") == 0) {
      if (!stopObstacle(trigPinDroite, echoPinDroite, seuilDetection)) {
        etatSysteme = 'R';
        tournerDroite(parametre);
      }
    } else if (strcmp(fonction, "L") == 0) {
      if (!stopObstacle(trigPinGauche, echoPinGauche, seuilDetection)) {
        etatSysteme = 'L';
        tournerGauche(parametre);
      }
    }
    else if (strcmp(fonction, "A") == 0) {
      autonome(commande);
    }
  }
  else if (lu == 1) {
    if (strcmp(fonction, "F") == 0) {
      etatSysteme = 'F';
      if (stopObstacle(trigPinAvant, echoPinAvant, seuilDetection))
        stopMoteurs();
      else
        avancer();  // <- appel sans paramètre
    } else if (strcmp(fonction, "B") == 0) {
      etatSysteme = 'B';
      reculer();
    } else if (strcmp(fonction, "R") == 0) {
      if (!stopObstacle(trigPinDroite, echoPinDroite, seuilDetection)) {
        etatSysteme = 'R';
        tournerDroite();
      }
    } else if (strcmp(fonction, "L") == 0) {
      if (!stopObstacle(trigPinGauche, echoPinGauche, seuilDetection)) {
        etatSysteme = 'L';
        tournerGauche();
      }
    } else if (strcmp(fonction, "S") == 0) {
      etatSysteme = 'S';
      stopMoteurs();
    }
  }
  else {
    Serial.println("Commande invalide !");
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

bool checkArretUrgence(char commande){
  bool arretUrgence = false;
  if(commande == 'A'){
    arretUrgence = true;
  }
  return arretUrgence;
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

// ------------------ Convertion des distances/angles en temps ------------------
float conversionDistTemps(float distance){ //distance en cm
  int duree = (distance / 80)*1000 ; // Temps en millisecondes. 
  //80 represente la vitesse en cm/s du robot lorsque setVitesse est à 2OO.
  return duree;
}

float conversionAngleTemps(float angle){
  int duree = (angle * 4720) / 360 ;
  return duree;
}
// ------------------------------------------------------------------------------

// ---------------------------- Gestion des moteurs -----------------------------
void reculer() {
  moteurAvantGauche.run(FORWARD);
  moteurAvantDroit.run(FORWARD);
  moteurDerriereDroite.run(FORWARD);
  moteurDerriereGauche.run(FORWARD);
}

void avancer() {
  moteurAvantGauche.run(BACKWARD);
  moteurAvantDroit.run(BACKWARD);
  moteurDerriereDroite.run(BACKWARD);
  moteurDerriereGauche.run(BACKWARD);
}

void tournerDroite() {
  moteurAvantGauche.run(BACKWARD);
  moteurAvantDroit.run(FORWARD);
  moteurDerriereDroite.run(FORWARD);
  moteurDerriereGauche.run(BACKWARD);
}

void tournerGauche() {
  moteurAvantGauche.run(FORWARD);
  moteurAvantDroit.run(BACKWARD);
  moteurDerriereDroite.run(BACKWARD);
  moteurDerriereGauche.run(FORWARD);
}

void reculer(float distance) {

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

void avancer(float distance) {
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

void tournerDroite(float angle) {
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

void tournerGauche(float angle) {
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
// ------------------------- Fin gestion des moteurs --------------------------

// --------------------------------- Autonome ---------------------------------

// --- Configuration des États ---
enum Etat {
  ETAT_ATTENTE,
  ETAT_AVANCER,
  ETAT_RECULER,
  ETAT_GAUCHE,
  ETAT_DROITE};

Etat etatPresent = ETAT_ATTENTE;


// stopObstacle(const int trigPin, const int echoPin, int seuilDetection)

// trigPinGauche
// echoPinGauche

// trigPinAvant
// echoPinAvant

// trigPinDroite
// echoPinDroite


void autonome(char* commande){
  while(commande == 'A'){
    
    switch(etatPresent){
      case ETAT_ATTENTE:
        if(stopObstacle(trigPinAvant, echoPinGauche, seuilDetection)){
          etatPresent = ETAT_AVANCER;
        }
        else if(stopObstacle(trigPinAvant, echoPinAvant, seuilDetection) && 
          stopObstacle(trigPinDroite, echoPinDroite, seuilDetection) && 
          !stopObstacle(trigPinGauche, echoPinGauche, seuilDetection))
        {
          etatPresent = ETAT_GAUCHE;
        }
        else if(stopObstacle(trigPinAvant, echoPinAvant, seuilDetection) && 
          !stopObstacle(trigPinDroite, echoPinDroite, seuilDetection) && 
          stopObstacle(trigPinGauche, echoPinGauche, seuilDetection))
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
        ETAT_ATTENTE;
        break;
        }
    }
  }
}




