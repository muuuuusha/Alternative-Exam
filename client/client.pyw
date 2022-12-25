
import sys
from PyQt5.QtWidgets import QApplication, QDialog
from src.MainWindow import MainWindow
from src.LoginDialog import LoginDialog

SERVER_IP = 'localhost'
SERVER_PORT = 3000

if __name__ == '__main__':
    app = QApplication([])
    
    loginWindow = LoginDialog(SERVER_IP, SERVER_PORT)
    
    if loginWindow.exec_() == QDialog.Accepted:
        print(f'Logged in as {loginWindow.nickname.text()}')
        window = MainWindow(SERVER_IP, 
                            SERVER_PORT, 
                            loginWindow.username,
                            loginWindow.userID)
        window.show()
        try:
            sys.exit(app.exec_())
        except KeyboardInterrupt:
            print('Exiting')
            sys.exit(0)
        except Exception as e:
            print(e)
            sys.exit(1)