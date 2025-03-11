#include <AFMotor.h>
#include <Arduino.h>

// ------------ Définition de la classe pour les capteurs ultrasons ----------------
class CapteurUltrason {
private:
    int capteurProche;        // Numéro du capteur le plus proche (1, 2, 3) ou 0 si aucun
    float distanceMin;
    float distanceGauche;
    float distanceAvant;
    float distanceDroite;

public:
    CapteurUltrason()
        : capteurProche(0), distanceMin(0), distanceGauche(0), distanceAvant(0), distanceDroite(0) {}
    CapteurUltrason(int c, float d)
        : capteurProche(c), distanceMin(d), distanceGauche(0), distanceAvant(0), distanceDroite(0) {}

    int getCapteurProche() const { return capteurProche; }
    float getDistanceMin() const { return distanceMin; }
    float getDistanceGauche() const { return distanceGauche; }
    float getDistanceAvant() const { return distanceAvant; }
    float getDistanceDroite() const { return distanceDroite; }
    
    void setCapteurProche(int c) { capteurProche = c; }
    void setDistanceMin(float d) { distanceMin = d; }
    void setDistanceGauche(float d) { distanceGauche = d; }
    void setDistanceAvant(float d) { distanceAvant = d; }
    void setDistanceDroite(float d) { distanceDroite = d; }
};

// ------------ Définition des moteurs ----------------
AF_DCMotor moteurAvantGauche(4);
AF_DCMotor moteurAvantDroit(3);
AF_DCMotor moteurArriereDroit(2);
AF_DCMotor moteurArriereGauche(1);

void setVitesse(int vitesse) {
    moteurAvantGauche.setSpeed(vitesse);
    moteurAvantDroit.setSpeed(vitesse);
    moteurArriereDroit.setSpeed(vitesse);
    moteurArriereGauche.setSpeed(vitesse);
}

void stopMoteurs() {
    moteurAvantGauche.run(RELEASE);
    moteurAvantDroit.run(RELEASE);
    moteurArriereDroit.run(RELEASE);
    moteurArriereGauche.run(RELEASE);
}

float conversionDistTemps(float distance) {
    return (distance / 80) * 1000;
}

float conversionAngleTemps(float angle) {
    return (angle * 4720) / 360;
}

void avancer(float distance) {
    moteurAvantGauche.run(BACKWARD);
    moteurAvantDroit.run(BACKWARD);
    moteurArriereDroit.run(BACKWARD);
    moteurArriereGauche.run(BACKWARD);
    delay(conversionDistTemps(distance));
    stopMoteurs();
}

void reculer(float distance) {
    moteurAvantGauche.run(FORWARD);
    moteurAvantDroit.run(FORWARD);
    moteurArriereDroit.run(FORWARD);
    moteurArriereGauche.run(FORWARD);
    delay(conversionDistTemps(distance));
    stopMoteurs();
}

void avancerContinu() {
    moteurAvantGauche.run(BACKWARD);
    moteurAvantDroit.run(BACKWARD);
    moteurArriereDroit.run(BACKWARD);
    moteurArriereGauche.run(BACKWARD);
}

void tournerGauche(float angle) {
    setVitesse(200);
    moteurAvantGauche.run(FORWARD);
    moteurArriereGauche.run(FORWARD);
    moteurAvantDroit.run(BACKWARD);
    moteurArriereDroit.run(BACKWARD);
    delay(conversionAngleTemps(angle));
    stopMoteurs();
    setVitesse(175);
}

void tournerDroite(float angle) {
    setVitesse(200);
    moteurAvantGauche.run(BACKWARD);
    moteurArriereGauche.run(BACKWARD);
    moteurAvantDroit.run(FORWARD);
    moteurArriereDroit.run(FORWARD);
    delay(conversionAngleTemps(angle));
    stopMoteurs();
    setVitesse(175);
}

// ------------ Définition des capteurs ultrasons ----------------
const int trigPinGauche = 52;
const int echoPinGauche = 53;
const int trigPinAvant = 44;
const int echoPinAvant = 45;
const int trigPinDroite = 38;
const int echoPinDroite = 39;

long getDistance(int trigPin, int echoPin) {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    long duration = pulseIn(echoPin, HIGH, 30000);
    return (duration > 0) ? (duration * 0.034 / 2) : 400;
}

CapteurUltrason detecterObstacle() {
    int distanceGauche = getDistance(trigPinGauche, echoPinGauche);
    int distanceAvant = getDistance(trigPinAvant, echoPinAvant);
    int distanceDroite = getDistance(trigPinDroite, echoPinDroite);
    int detectionMin = 25;

    int distanceMin = distanceGauche;
    int capteur = 1;

    if (distanceAvant < distanceMin) {
        distanceMin = distanceAvant;
        capteur = 2;
    }
    if (distanceDroite < distanceMin) {
        distanceMin = distanceDroite;
        capteur = 3;
    }
    if (distanceMin > detectionMin) {
        capteur = 0;
    }
    return CapteurUltrason(capteur, distanceMin);
}

void setup() {
    Serial.begin(9600);
    pinMode(trigPinGauche, OUTPUT);
    pinMode(echoPinGauche, INPUT);
    pinMode(trigPinAvant, OUTPUT);
    pinMode(echoPinAvant, INPUT);
    pinMode(trigPinDroite, OUTPUT);
    pinMode(echoPinDroite, INPUT);
    setVitesse(175);
    stopMoteurs();
}

void loop() {
    int degresRotationObstacle = 45;
    CapteurUltrason obstacle = detecterObstacle();
    int capteurProche = obstacle.getCapteurProche();
    Serial.println(capteurProche);

    if (capteurProche == 2) {
        stopMoteurs();
        reculer(50);
        delay(500);
        tournerDroite(degresRotationObstacle);
        delay(500);
        avancerContinu();
    } else if (capteurProche == 1) {
        stopMoteurs();
        tournerDroite(degresRotationObstacle);
        delay(500);
        avancerContinu();
    } else if (capteurProche == 3) {
        stopMoteurs();
        tournerGauche(degresRotationObstacle);
        delay(500);
        avancerContinu();
    } else {
        avancerContinu();
    }
}
