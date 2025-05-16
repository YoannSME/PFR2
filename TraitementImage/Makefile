
EXEC = detection

OBJDIR = build

SRCS = traiterImage.cpp Image/GestionTraitementImage.cpp Objet/Objet.cpp Objet/Couleur.cpp

OBJS = $(SRCS:.cpp=.o)
OBJS := $(patsubst %.o,$(OBJDIR)/%.o,$(OBJS))

CXX = g++

CXXFLAGS = -Wall -std=c++17 -Iinclude `pkg-config --cflags opencv4`
LDFLAGS = `pkg-config --libs opencv4`

all: $(EXEC)

ajouterCouleur :
	@echo "Ajouter une de la couleur..."
	$(CXX) $(CXXFLAGS) -o ajouterCouleur ajouterCouleur.cpp $(LDFLAGS)
	@echo "Ajout une couleur terminé."
$(EXEC): $(OBJS)
	@echo "Linking $(EXEC)..."
	$(CXX) -o $@ $^ $(LDFLAGS)
	@echo "Linking terminé."

$(OBJDIR)/%.o: %.cpp
	@mkdir -p $(dir $@)
	@echo "Compiling $<..."
	$(CXX) $(CXXFLAGS) -c $< -o $@
	@echo "Compilation de $< terminée."

clean:
	rm -rf $(OBJDIR) $(EXEC)

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