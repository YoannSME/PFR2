#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "traitement_vocal.h"

token dict_avancer;
token dict_reculer;
token dict_droite;
token dict_gauche;
token dict_cles_complexes;
token dict_negations;
token dict_arguments;

token_complexe dictCPX;

char instructions_a_executer[MAX_BUFFER_SIZE];

void init_dictionnaires()
{
    dict_avancer = recuperer_dictionnaire("../Commande_vocale/dictAvancer.txt");
    dict_reculer = recuperer_dictionnaire("../Commande_vocale/dictReculer.txt");
    dict_droite = recuperer_dictionnaire("../Commande_vocale/dictDroite.txt");
    dict_gauche = recuperer_dictionnaire("../Commande_vocale/dictGauche.txt");
    dict_cles_complexes = recuperer_dictionnaire("../Commande_vocale/dictComplexe.txt");
    dict_negations = recuperer_dictionnaire("../Commande_vocale/dictNegation.txt");
    dict_arguments = recuperer_dictionnaire("../Commande_vocale/dictArgument.txt");

    dictCPX = recuperer_dictionnaire_complexe("../Commande_vocale/dictComplexe.txt");
}
token creer_token()
{
    token token;
    token.nbMots = 0;
    return token;
}
token_complexe creer_token_complexe()
{
    token_complexe tokenCPX;
    tokenCPX.nbcles = 0; // Initialisation de nbcles pour éviter des valeurs indéfinies
    for (int i = 0; i < TAILLE_MAX_DICT; i++)
    {
        tokenCPX.valeur[i] = creer_token();
    }
    return tokenCPX;
}

FILE *ouvrir_fichier(char filename[], char *mode)
{
    FILE *file = fopen(filename, mode);
    if (file == NULL)
    {
        fprintf(stderr, "Erreur ouverture du fichier %s\n", filename);
        exit(1);
    }
    return file;
}

char *recuperer_commande_vocale()
{
    FILE *fichier = ouvrir_fichier("../Commande_vocale/transcription.txt", "r");

    if (fgets(instructions_a_executer, MAX_BUFFER_SIZE, fichier) == NULL)
    {
        fclose(fichier);
        return NULL;
    }

    instructions_a_executer[strcspn(instructions_a_executer, "\n")] = '\0';
    fclose(fichier);
    return instructions_a_executer;
}
token tokeniser_phrase_courante(char buffer[MAX_BUFFER_SIZE])
{
    init_dictionnaires();
    token phraseTokenise = creer_token();
    phraseTokenise.nbMots = 0;
    int i = 0;
    while (buffer[i] != '\0')
    {
        if (buffer[i] == ' ' || buffer[i] == '\'')
            i++;
        else
        {
            int j = 0;
            while (buffer[i] != ' ' && buffer[i] != '\0' && buffer[i] != '\'')
            {
                phraseTokenise.mots[phraseTokenise.nbMots][j] = buffer[i];
                i++;
                j++;
            }
            phraseTokenise.mots[phraseTokenise.nbMots][j] = '\0';

            phraseTokenise.nbMots += 1;
        }
    }
    instructions_a_executer[strcspn(instructions_a_executer, "\n")] = '\0';
    return phraseTokenise;
}

int contientNegation(token chaine_triee)
{
    int distance = 0;
    for (int i = 0; i < chaine_triee.nbMots; i++)
    {
        if (est_dans_dictionnaire(chaine_triee.mots[i], dict_negations))
        {
            return distance;
        }
        distance++;
    }
    return 0;
}
int extraireNombre(char *chaine)
{
    int nombre = 0;
    int estDansUnNombre = 0;

    while (*chaine)
    {
        if (*chaine >= '0' && *chaine <= '9')
        {
            nombre = nombre * 10 + (*chaine - '0');
            estDansUnNombre = 1;
        }
        else if (estDansUnNombre)
        {
            break;
        }
        chaine++;
    }

    return estDansUnNombre ? nombre : -1;
}

token recuperer_dictionnaire(char *filename)
{
    FILE *fichierDictionnaire = ouvrir_fichier(filename, "r");
    token motsDictionnaire = creer_token();
    while (fgets(motsDictionnaire.mots[motsDictionnaire.nbMots], MAX_BUFFER_SIZE, fichierDictionnaire) != NULL)
    {
        motsDictionnaire.mots[motsDictionnaire.nbMots][strcspn(motsDictionnaire.mots[motsDictionnaire.nbMots], "\n")] = '\0';
        char *pos = strchr(motsDictionnaire.mots[motsDictionnaire.nbMots], ':');
        if (pos != NULL)
        {
            *pos = '\0';
        }
        int len = strlen(motsDictionnaire.mots[motsDictionnaire.nbMots]);
        while (len > 0 && motsDictionnaire.mots[motsDictionnaire.nbMots][len - 1] == ' ')
        {
            motsDictionnaire.mots[motsDictionnaire.nbMots][--len] = '\0';
        }
        motsDictionnaire.nbMots++;
    }
    fclose(fichierDictionnaire);
    return motsDictionnaire;
}

int est_dans_dictionnaire(char *mot, token motsDictionnaire)
{
    for (int i = 0; i < motsDictionnaire.nbMots; i++)
    {
        if (strcmp(mot, motsDictionnaire.mots[i]) == 0)
            return 1;
    }
    return 0;
}

token_complexe recuperer_dictionnaire_complexe(char *filename)
{
    FILE *fichierDictionnaire = ouvrir_fichier(filename, "r");

    char buffer[MAX_BUFFER_SIZE];
    token_complexe dictionnaire = creer_token_complexe();

    while (fgets(buffer, MAX_BUFFER_SIZE, fichierDictionnaire) != NULL)
    {
        char *pos = strchr(buffer, ':');
        if (pos != NULL)
        {
            char *start = buffer;
            while (*start == ' ')
            {
                start++;
            }
            memmove(buffer, start, strlen(start) + 1);
            pos = strchr(buffer, ':');
            if (pos != NULL)
            {
                *pos = '\0';
                int len = strlen(buffer);
                while (len > 0 && buffer[len - 1] == ' ')
                {
                    buffer[len - 1] = '\0';
                    len--;
                }
                strncpy(dictionnaire.cles[dictionnaire.nbcles], buffer, MAX_BUFFER_SIZE - 1);
                dictionnaire.cles[dictionnaire.nbcles][MAX_BUFFER_SIZE - 1] = '\0';
                char *reste = pos + 1;
                while (*reste == ' ')
                {
                    reste++;
                }
                dictionnaire.valeur[dictionnaire.nbcles].nbMots = 0;
                char *token = strtok(reste, " \n");
                while (token != NULL)
                {
                    strncpy(dictionnaire.valeur[dictionnaire.nbcles].mots[dictionnaire.valeur[dictionnaire.nbcles].nbMots],
                            token,
                            MAX_BUFFER_SIZE - 1);
                    dictionnaire.valeur[dictionnaire.nbcles].mots[dictionnaire.valeur[dictionnaire.nbcles].nbMots][MAX_BUFFER_SIZE - 1] = '\0';
                    dictionnaire.valeur[dictionnaire.nbcles].nbMots++;

                    token = strtok(NULL, " \n");
                }
                dictionnaire.nbcles++;
            }
        }
    }

    fclose(fichierDictionnaire);
    return dictionnaire;
}

token filtrer_mots(token requeteTexte)
{
    token texte_filtre = creer_token();
    char nb_char[12];
    int taille_requete = requeteTexte.nbMots;
    for (int i = 0; i < taille_requete; i++)
    {
        char *mot_courant = requeteTexte.mots[i];

        if (est_dans_dictionnaire(mot_courant, dict_avancer)        ||
            est_dans_dictionnaire(mot_courant, dict_reculer)        ||
            est_dans_dictionnaire(mot_courant, dict_droite)         ||
            est_dans_dictionnaire(mot_courant, dict_gauche)         ||
            est_dans_dictionnaire(mot_courant, dict_cles_complexes) ||
            est_dans_dictionnaire(mot_courant, dict_arguments))
        {
            strcpy(texte_filtre.mots[texte_filtre.nbMots], mot_courant);
            texte_filtre.nbMots++;
        }

        else
        {
            int nb = extraireNombre(mot_courant);
            if (nb != -1)
            {
                snprintf(nb_char, sizeof(nb_char), "%d", nb);
                strcpy(texte_filtre.mots[texte_filtre.nbMots], nb_char);
                texte_filtre.nbMots++;
            }
        }
    }

    return texte_filtre;
}

token transformation_requete_commande(token requeteTexte)
{
    init_dictionnaires();
    token requete_commande = creer_token();
    int distance_defaut = 100;
    int angle_defaut = 90;
    int taille_requete = requeteTexte.nbMots;
    for (int i = 0; i < taille_requete; i++)
    {
        char *mot_courant = requeteTexte.mots[i];
        printf("mot courant (%s)\n", mot_courant);
        int distance;
        if (est_dans_dictionnaire(mot_courant, dict_avancer))
        {

            if ((i + 1) < taille_requete && (sscanf(requeteTexte.mots[i + 1], "%d", &distance) == 1))
            {

                snprintf(requete_commande.mots[requete_commande.nbMots], MAX_BUFFER_SIZE, "forward(%d)", distance);
            }
            else
            {
                snprintf(requete_commande.mots[requete_commande.nbMots], MAX_BUFFER_SIZE, "forward(%d)", distance_defaut);
            }
            requete_commande.nbMots += 1;
        }
        else if (est_dans_dictionnaire(mot_courant, dict_reculer))
        {
            if ((i + 1) < taille_requete && (sscanf(requeteTexte.mots[i + 1], "%d", &distance) == 1))
            {

                snprintf(requete_commande.mots[requete_commande.nbMots], MAX_BUFFER_SIZE, "backward(%d)", distance);
            }
            else
            {
                snprintf(requete_commande.mots[requete_commande.nbMots], MAX_BUFFER_SIZE, "backward(%d)", distance_defaut);
            }
            requete_commande.nbMots += 1;
        }
        else if (est_dans_dictionnaire(mot_courant, dict_droite))
        {
            if ((i + 1) < taille_requete && (sscanf(requeteTexte.mots[i + 1], "%d", &distance) == 1))
            {

                snprintf(requete_commande.mots[requete_commande.nbMots], MAX_BUFFER_SIZE, "right(%d)", distance);
            }
            else
            {
                snprintf(requete_commande.mots[requete_commande.nbMots], MAX_BUFFER_SIZE, "right(%d)", angle_defaut);
            }
            requete_commande.nbMots += 1;
        }
        else if (est_dans_dictionnaire(mot_courant, dict_gauche))
        {
            if ((i + 1) < taille_requete && (sscanf(requeteTexte.mots[i + 1], "%d", &distance) == 1))
            {

                snprintf(requete_commande.mots[requete_commande.nbMots], MAX_BUFFER_SIZE, "left(%d)", distance);
            }
            else
            {
                snprintf(requete_commande.mots[requete_commande.nbMots], MAX_BUFFER_SIZE, "left(%d)", angle_defaut);
            }
            requete_commande.nbMots += 1;
        }
        else if (est_dans_dictionnaire(mot_courant, dict_cles_complexes))
        {
            printf("cpx\n");
            token commande = recuperer_commande(mot_courant, dictCPX);
            for (int i = 0; i < commande.nbMots; i++)
            {
                printf("mot courant : %s\n", commande.mots[i]);
                snprintf(requete_commande.mots[requete_commande.nbMots], MAX_BUFFER_SIZE, "%s", commande.mots[i]);
                requete_commande.nbMots++;
            }
        }
        else if(est_dans_dictionnaire(mot_courant,dict_arguments)){
            printf("arg\n");
            snprintf(requete_commande.mots[requete_commande.nbMots], MAX_BUFFER_SIZE, "%s", mot_courant);
            requete_commande.nbMots++;
        }
    }
    return requete_commande;
}

token recuperer_commande(char *cle, token_complexe dictCPX)
{
    token retour = creer_token();
    for (int i = 0; i < dictCPX.nbcles; i++)
    {
        if (strcmp(dictCPX.cles[i], cle) == 0)
        {
            return dictCPX.valeur[i];
        }
    }
    return retour;
}

void envoyer_au_robot(token requete_commande)
{
    FILE *fichier = ouvrir_fichier("../Commande_vocale/requete_commande.txt", "w");
    for (int i = 0; i < requete_commande.nbMots; i++)
    {
        fprintf(fichier, "%s ", requete_commande.mots[i]);
    }
    fclose(fichier);
}

void appeler_pilotage_manuel()
{
    init_dictionnaires();
    printf("Instructions à donner au robot : ");
    char instructions_a_effectuer[MAX_BUFFER_SIZE];

    if (fgets(instructions_a_effectuer, MAX_BUFFER_SIZE, stdin) == NULL)
    {
        fprintf(stderr, "Commande %s invalide", instructions_a_effectuer);
        exit(1);
    }
    instructions_a_effectuer[strcspn(instructions_a_effectuer, "\n")] = '\0';

    token phrase = tokeniser_phrase_courante(instructions_a_effectuer);
    for (int i = 0; i < phrase.nbMots; i++)
    {
        printf("%s \n", phrase.mots[i]);
    }
    printf("\n");
    token mots_filtrees = filtrer_mots(phrase);
    token requete = transformation_requete_commande(mots_filtrees);
    envoyer_au_robot(requete);
    printf("Requete commande générée : ");
    for (int i = 0; i < requete.nbMots; i++)
    {
        printf("%s ", requete.mots[i]);
    }
    printf("\n");
}

void appeler_pilotage_vocal()
{
    if (system("python3 ../Commande_vocale/speech_to_text.py") == -1)
    {
        perror("system STT");
        exit(1);
    }
    token phrase = tokeniser_phrase_courante(recuperer_commande_vocale());
    token mots_filtrees = filtrer_mots(phrase);
    token requete = transformation_requete_commande(mots_filtrees);
    envoyer_au_robot(requete);
    for (int i = 0; i < requete.nbMots; i++)
    {
        printf("%s ", requete.mots[i]);
    }
    printf("\n");
}

int main()
{
    /*// int nbLignes = 0;
    printf("debut\n");
    char *filename = "../Commande_vocale/dictComplexe.txt";
    printf("debut2\n");
    token_complexe tst = recuperer_dictionnaire_complexe(filename);
    for (int i = 0; i < tst.nbcles; i++)
    {
        printf("clé (%s) - \n", tst.cles[i]);
        for (int j = 0; j < tst.valeur[i].nbMots; j++)
        {
            printf(" valeur   (%s) ", tst.valeur[i].mots[j]);
        }
        printf("\n");
    }

    printf("zigzag\n");
    char cle[] = "zigzag";
    printf("cle = (%s)\n", cle);
    token retour = recuperer_commande(cle, tst);
    for (int i = 0; i < retour.nbMots; i++)
    {
        printf("%s ", retour.mots[i]);
    }

    return 0;*/

    appeler_pilotage_manuel();
}
