from ServeurClass import Server

if __name__ == '__main__':
    # Création et démarrage du serveur Flask
    server = Server()
    print(f"Serveur démarré sur {server.host}:{server.port}")
    server.run()
    