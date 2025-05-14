from Interface.InputClass import Manette, Keyboard
from Interface.TraductionClass import Traduction
from Configuration.ConfigurationClass import Configuration
from Communication.CommunicationClass import Bluetooth, FlaskClient
from GestionRequest.GestionRequestClass import GestionRequest
from Lidar.CartographieClass import Cartographie

class Utils():
    def __init__(self, debug=False):
        
        # Config/traduc ---------------------------------------------------------------------------
        self.configuration = Configuration("Configuration/ConfigurationFile.json", "Configuration/ConfigurationValue.json")
        self.traduction = Traduction(langue=self.configuration.get("langue"))
        # -----------------------------------------------------------------------------------------
        
        # Input -----------------------------------------------------------------------------------
        self.manette = Manette()
        self.keyboard = Keyboard()
        # -----------------------------------------------------------------------------------------
        
        
        # Comunication ----------------------------------------------------------------------------
        if not debug :
            self.bt = Bluetooth(self.configuration.get("bt_port"), self.configuration.get("bt_baud"))
            self.rasp = FlaskClient(self.configuration.get("serveur_ip"))
        else :
            self.bt = None
            self.rasp = None
        # -----------------------------------------------------------------------------------------
        
        # Traitement ------------------------------------------------------------------------------
        self.cartographie = Cartographie()
        self.image = None
        self.gestionRequest = GestionRequest(self.configuration.get("vocal_request_path"), 
                                             self.configuration.get("vocal_dico_path"),
                                             self.bt,
                                             self.rasp)
        # -----------------------------------------------------------------------------------------        
    