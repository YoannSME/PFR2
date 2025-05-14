from datetime import datetime

class log:
    def __init__(self, log_file):
        self.log_file = log_file

    def write_log(self, message):
        with open(self.log_file, 'a') as f:
            f.write(datetime.now().strftime("[%d/%m/%y %H:%M:%S] ") + message + '\n')

    def read_log(self):
        with open(self.log_file, 'r') as f:
            return f.readlines()
    
    def clear_log(self):
        with open(self.log_file, 'w') as f:
            f.write('')
        

#EXEMPLE UTILISATION
"""if __name__ == "__main__":
    log_file = os.path.join(os.path.dirname(__file__), 'log.txt')
    logger = log(log_file)
    logger.write_log("This is a test log message.")
    print(logger.read_log())
    
    logger.write_log("This is another test log message.")"""