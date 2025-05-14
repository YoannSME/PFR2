# Nom de l'exécutable
EXEC = detection

# Répertoire de sortie des objets
OBJDIR = build

# Liste des fichiers source
SRCS = traiterImage.cpp Image/GestionTraitementImage.cpp Objet/Objet.cpp Objet/Couleur.cpp

# Fichiers objets dans build/ (respect de l'arborescence)
OBJS = $(SRCS:.cpp=.o)
OBJS := $(patsubst %.o,$(OBJDIR)/%.o,$(OBJS))

# Compilateur
CXX = g++

# Flags de compilation
CXXFLAGS = -Wall -std=c++17 -Iinclude `pkg-config --cflags opencv4`
LDFLAGS = `pkg-config --libs opencv4`

# Règle par défaut
all: $(EXEC)

ajouterCouleur :
	@echo "Ajouter une de la couleur..."
	$(CXX) $(CXXFLAGS) -o ajouterCouleur ajouterCouleur.cpp $(LDFLAGS)
	@echo "Ajout une couleur terminé."

# Construction de l'exécutable
$(EXEC): $(OBJS)
	@echo "Linking $(EXEC)..."
	$(CXX) -o $@ $^ $(LDFLAGS)
	@echo "Linking terminé."

# Compilation des .cpp en .o dans build/, en respectant les sous-dossiers
$(OBJDIR)/%.o: %.cpp
	@mkdir -p $(dir $@)
	@echo "Compiling $<..."
	$(CXX) $(CXXFLAGS) -c $< -o $@
	@echo "Compilation de $< terminée."

# Nettoyage des fichiers intermédiaires
clean:
	rm -rf $(OBJDIR) $(EXEC)

# Nettoyage complet
mrproper: clean
	rm -f *~

# Initialisation : télécharge json.hpp si besoin
init:
	mkdir -p include/nlohmann
	if [ ! -f include/nlohmann/json.hpp ]; then \
		wget -q https://raw.githubusercontent.com/nlohmann/json/develop/single_include/nlohmann/json.hpp -O include/nlohmann/json.hpp; \
		echo "nlohmann/json.hpp téléchargé."; \
	else \
		echo "json.hpp déjà présent."; \
	fi