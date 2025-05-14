from Interface.GlobalInterfaceClass import InterfaceGlobale
from Utils.UtilsClass import Utils

if __name__ == "__main__":
    interfaceUtils = Utils(debug=False)
    interface = InterfaceGlobale(width=1920, height=1080, utils=interfaceUtils)
    interface.run()