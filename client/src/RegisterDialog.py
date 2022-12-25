from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QDialog 

from src.Requests import REGISTER
from src.ClientSocket.Sender import Sender
from src.Requests import *

class RegisterDialog(Sender, QDialog):
    def __init__(self, serverIP, serverPort):
        Sender.__init__(self, serverIP, serverPort)
        QDialog.__init__(self)
        
        uic.loadUi('./src/ui/RegisterDialog.ui', self)
        self.setWindowIcon(QtGui.QIcon('./src/ui/ico/AB_icon.ico'))
        
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordRepeat.setEchoMode(QtWidgets.QLineEdit.Password)

        passwordRegexp: QtCore.QRegExp = QtCore.QRegExp(r'^[a-zA-Z0-9]{4,}$')
        usernameRegexp: QtCore.QRegExp = QtCore.QRegExp(r'^[a-zA-Z0-9]{4,}$')
        
        usernameValidator = QtGui.QRegExpValidator(usernameRegexp)
        passwordValidator = QtGui.QRegExpValidator(passwordRegexp)
        
        self.nickname.setValidator(usernameValidator)
        
        self.password.setValidator(passwordValidator)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

        self.passwordRepeat.setValidator(passwordValidator)
        self.passwordRepeat.setEchoMode(QtWidgets.QLineEdit.Password)
        
        self.acceptButton.clicked.connect(self.register)
        
        
    def register(self):
        if self.password.text() != self.passwordRepeat.text():
            response = {'code': 'Passwords do not match'}
        else:
            response = self.send(REGISTER(self.nickname.text(), 
                                          self.password.text()))
        
        if not response['code']:
            self.username = self.nickname.text()
            self.userID = response['userID']
            self.accept()
        else:
            self.errorMessage.setText(response['code'])
            