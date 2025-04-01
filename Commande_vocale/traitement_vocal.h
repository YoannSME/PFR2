/**
 * @file traitement_vocal.h
 * @brief Définition des structures et fonctions pour le traitement vocal.
 *
 * Ce fichier contient les déclarations des structures et des fonctions utilisées
 * pour traiter les commandes vocales et les convertir en instructions pour le robot.
 */

#ifndef TRAITEMENT_VOCAL_H
#define TRAITEMENT_VOCAL_H

#define MAX_BUFFER_SIZE 128  ///< Taille maximale du buffer pour le traitement des commandes vocales.
#define PATH_DICT_AVANCER "dictAvancer.txt" ///< Chemin du fichier contenant les commandes pour avancer.

/**
 * @struct s_token
 * @brief Structure représentant un ensemble de mots tokenisés.
 */

#define TAILLE_MAX_DICT 30
typedef struct s_token
{
    char mots[MAX_BUFFER_SIZE][MAX_BUFFER_SIZE]; ///< Tableau stockant les mots extraits.
    int nbMots; ///< Nombre de mots stockés dans le tableau.
} token;

typedef struct s_token_complexe{
    char cles[MAX_BUFFER_SIZE][MAX_BUFFER_SIZE];
    token valeur[TAILLE_MAX_DICT];
    int nbcles;
}token_complexe;
/**
 * @brief Dictionnaires de mots-clés associés aux commandes du robot.
 */
extern token dict_avancer; ///< Dictionnaire des commandes pour avancer.
extern token dict_reculer; ///< Dictionnaire des commandes pour reculer.
extern token dict_droite; ///< Dictionnaire des commandes pour tourner à droite.
extern token dict_gauche; ///< Dictionnaire des commandes pour tourner à gauche.

extern char instructions_a_executer[MAX_BUFFER_SIZE]; ///< Buffer contenant les instructions à exécuter.

extern int nb_dict; ///< Nombre total de dictionnaires chargés.

/**
 * @brief Récupère un dictionnaire de mots-clés à partir d'un fichier.
 * @param filename Nom du fichier contenant les mots-clés.
 * @return Le dictionnaire sous forme d'une structure token.
 */
token recuperer_dictionnaire(char *filename);
token recuperer_commande(char *cle,token_complexe dictCPX);

token_complexe recuperer_dictionnaire_complexe(char *filename);

/**
 * @brief Extrait un nombre d'une chaîne de caractères.
 * @param chaine La chaîne de caractères contenant le nombre.
 * @return Le nombre extrait.
 */
int extraireNombre(char *chaine);

/**
 * @brief Vérifie si un mot appartient à un dictionnaire.
 * @param mot Le mot à rechercher.
 * @param motsDictionnaire Le dictionnaire dans lequel rechercher.
 * @return 1 si le mot est dans le dictionnaire, 0 sinon.
 */
int est_dans_dictionnaire(char *mot, token motsDictionnaire);

/**
 * @brief Envoie une commande au robot après analyse vocale.
 * @param requete_commande La requête contenant la commande à exécuter.
 */
void envoyer_au_robot(token requete_commande);

/**
 * @brief Filtre les mots inutiles d'une requête textuelle.
 * @param requeteTexte La requête textuelle à filtrer.
 * @return Une requête contenant uniquement les mots utiles.
 */
token filtrer_mots(token requeteTexte);

/**
 * @brief Transforme une requête textuelle en commande exécutable par le robot.
 * @param requeteTexte La requête textuelle à transformer.
 * @return La commande correspondante sous forme de token.
 */
token transformation_requete_commande(token requeteTexte);

/**
 * @brief Crée une structure token vide.
 * @return Une structure token initialisée.
 */
token creer_token();

/**
 * @brief Initialise les dictionnaires de mots-clés.
 */
void init_dictionnaires();

/**
 * @brief Tokenise une phrase en extrayant les mots significatifs.
 * @param buffer La phrase à tokeniser.
 * @return Un token contenant les mots extraits.
 */
token tokeniser_phrase_courante(char buffer[MAX_BUFFER_SIZE]);

/**
 * @brief Récupère une commande vocale.
 * @return La commande vocale sous forme de chaîne de caractères.
 */
char* recuperer_commande_vocale();

/**
 * @brief Démarre le mode de pilotage vocal.
 */
void appeler_pilotage_vocal();

/**
 * @brief Démarre le mode de pilotage manuel.
 */
void appeler_pilotage_manuel();

#endif // TRAITEMENT_VOCAL_H
