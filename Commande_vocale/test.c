#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef struct s_token
{
    char mots[256][512]; ///< Tableau stockant les mots extraits.
    int nbMots; ///< Nombre de mots stockés dans le tableau.
} token;
token creer_token()
{
    token token;
    token.nbMots = 0;
    return token;
}

int main(void){
   
    FILE* fichier = fopen("../Commande_vocale/dictComplexe.txt","r");

    char buffer[] = {"zigzag : avance recule"};
    char cle[1024];
    //while(fgets(buffer,2048,fichier) != NULL){
        char* line = strchr(buffer,':'); //
        if(line != NULL){
            int taille = line - buffer;
            strncpy(cle,buffer,taille);
            cle[taille] = '\0';
        }
        line++;
        printf("clé :  %s - valeur %s \n",cle,line);

        

    

}