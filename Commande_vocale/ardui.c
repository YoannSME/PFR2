#include <Arduino.h>

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

void setup() {
    // Initialisation de la communication série (pour le Bluetooth)
    Serial.begin(9600);
    while (!Serial); // Attendre que la connexion série soit prête
    Serial.println("Entrez les commandes sous forme : avancer(100) reculer(50) tourner(90)");
}

void loop() {
    static char ligne[1024]; // Stocke la ligne reçue
    static int index = 0;    // Indice pour la ligne

    // Vérifier si des données sont disponibles sur le port série (Bluetooth)
    if (Serial.available()) {
        char c = Serial.read();

        // Lire les caractères jusqu'à ce que l'on rencontre un retour à la ligne
        if (c != '\n' && index < sizeof(ligne) - 1) {
            ligne[index++] = c;  // Ajouter le caractère à la ligne
        } else if (c == '\n' || index >= sizeof(ligne) - 1) {
            ligne[index] = '\0';  // Terminer la ligne avec un caractère nul
            traiter_ligne_commandes(ligne);  // Traiter les commandes de la ligne
            index = 0;  // Réinitialiser l'indice pour la prochaine ligne
        }
    }
}
