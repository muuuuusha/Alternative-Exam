from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QDialog

from src.Requests import LOGIN
from src.ClientSocket.Sender import Sender
from src.RegisterDialog import RegisterDialog

class LoginDialog(Sender, QDialog):
    def __init__(self, serverIP: str, serverPort: int):
        Sender.__init__(self, serverIP, serverPort)
        QDialog.__init__(self)
        
        uic.loadUi('./src/ui/LoginDialog.ui', self)
        self.setWindowIcon(QtGui.QIcon('./src/ui/ico/AB_icon.ico'))
        
        self.serverIP = serverIP
        self.serverPort = serverPort
        
        passwordValidator = QtGui.QRegExpValidator(QtCore.QRegExp(r'^[a-zA-Z0-9]{4,}$'))
        usernameValidator = QtGui.QRegExpValidator(QtCore.QRegExp(r'^[a-zA-Z0-9]{4,}$'))
        
        self.nickname.setValidator(usernameValidator)
        
        self.password.setValidator(passwordValidator)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        
        self.acceptButton.clicked.connect(self.login)
        self.registerButton.clicked.connect(self.register) 


    def register(self):
        registerDialog = RegisterDialog(self.serverIP, self.serverPort)
        self.hide()
        if (registerDialog.exec_()):
            self.username = registerDialog.nickname.text()
            self.userID = registerDialog.userID
            self.accept()
        else:
            self.errorMessage.setText('Registration canceled')

        
    def login(self):
        response = self.send(LOGIN(self.nickname.text(), 
                                   self.password.text()))
        
        if not response['code']:
            self.username = self.nickname.text()
            self.userID = response['userID']
            self.accept()
        else:
            self.errorMessage.setText(response['code'])