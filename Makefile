# Nom de l'exécutable
EXEC = detection

# Répertoire de sortie des objets
OBJDIR = build

# Liste des fichiers source
SRCS = testWrite.cpp GestionTraitementImage.cpp Objet.cpp Couleur.cpp

# Fichiers objets dans build/
OBJS = $(SRCS:.cpp=.o)
OBJS := $(addprefix $(OBJDIR)/, $(OBJS))

# Compilateur
CXX = g++

# Flags de compilation
CXXFLAGS = -Wall -std=c++17 -Iinclude `pkg-config --cflags opencv4`
LDFLAGS = `pkg-config --libs opencv4`

# Règle par défaut
all: $(EXEC)

# Construction de l'exécutable
$(EXEC): $(OBJS)
	@echo "Linking $(EXEC)..."
	$(CXX) -o $@ $^ $(LDFLAGS)
	@echo "Linking terminé."

# Compilation des .cpp en .o dans build/
$(OBJDIR)/%.o: %.cpp
	@mkdir -p $(OBJDIR)
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
