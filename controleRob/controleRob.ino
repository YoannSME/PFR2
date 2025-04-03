#include <AFMotor.h>
#include <string.h>

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
  Serial.begin(9600);
  setupBluetooth();
  setupMoteur();
}

void setupBluetooth(){
  while (!Serial); // Attendre que la connexion série soit prête
  Serial.println("Entrez les commandes sous forme : avancer(100) reculer(50) tourner(90)");
  
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

void loop() {
  static char statutRob = 'S';
  /*
  if (Serial1.available() > 0) {  // Lire la commande envoyée par Bluetooth
    char commande = Serial1.read();
    Serial.println(commande);
    */
    static char ligne[1024]; // Stocke la ligne reçue
    static int index = 0;    // Indice pour la ligne

    // Vérifier si des données sont disponibles sur le port série (Bluetooth)
    char commande = Serial.read();
    if (Serial1.available()) {
      Serial.print("Reçu: ");
      Serial.println(commande);

      // Lire les caractères jusqu'à ce que l'on rencontre un retour à la ligne
      if (commande != '\n' && index < sizeof(ligne) - 1) {
          ligne[index++] = commande;  // Ajouter le caractère à la ligne
        } 
      else if (commande == '\n' || index >= sizeof(ligne) - 1) {
          ligne[index] = '\0';  // Terminer la ligne avec un caractère nul
          traiter_ligne_commandes(ligne);  // Traiter les commandes de la ligne
          index = 0;  // Réinitialiser l'indice pour la prochaine ligne
        }
      }

    
    bool arretUrgence = checkArretUrgence(commande);
    if(!arretUrgence){ 
      
      if (commande == 'F') {
        
        if (stopObstacle(trigPinAvant, echoPinAvant, seuilDetection)){
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

// Fonction pour avancer
void reculer() {
  moteurAvantGauche.run(FORWARD);
  moteurAvantDroit.run(FORWARD);
  moteurDerriereDroite.run(FORWARD);
  moteurDerriereGauche.run(FORWARD);
}

// Fonction pour reculer
void avancer() {
   Serial.println("avancer");
  moteurAvantGauche.run(BACKWARD);
  moteurAvantDroit.run(BACKWARD);
  moteurDerriereDroite.run(BACKWARD);
  moteurDerriereGauche.run(BACKWARD);
}

// Fonction pour tourner à gauche
void tournerDroite() {
  Serial.println("droite");
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

// Définir les fonctions de commandes
void avancer(int taille) {
    Serial.print("Avancer de ");
    Serial.print(taille);
    Serial.println(" unités");
}

void reculer(int taille) {
    Serial.print("Reculer de ");
    Serial.print(taille);
    Serial.println(" unités");
}

void tourner(int angle) {
    Serial.print("Tourner de ");
    Serial.print(angle);
    Serial.println(" degrés");
}

// Fonction pour traiter chaque commande (extraction de la fonction et du paramètre)
void traiter_commande(char* commande) {
    char fonction[50];
    int parametre;

    // Analyser la commande pour extraire la fonction et l'argument
    if (sscanf(commande, "%49[^()]%*c%d", fonction, &parametre) == 2) {
        if (strcmp(fonction, "avancer") == 0) {
            avancer(parametre);
        } else if (strcmp(fonction, "reculer") == 0) {
            reculer(parametre);
        } else if (strcmp(fonction, "tourner") == 0) {
            tourner(parametre);
        } else {
            Serial.print("Commande inconnue : ");
            Serial.println(fonction);
        }
    } else {
        Serial.print("Commande mal formatée : ");
        Serial.println(commande);
    }
}

// Fonction pour analyser et traiter une ligne contenant plusieurs commandes
void traiter_ligne_commandes(char* ligne) {
    char* commande = strtok(ligne, " ");  // Séparer les commandes par espace

    // Traiter chaque commande séparée
    while (commande != NULL) {
        traiter_commande(commande);  // Traiter la commande
        commande = strtok(NULL, " ");  // Passer à la commande suivante
    }
}
