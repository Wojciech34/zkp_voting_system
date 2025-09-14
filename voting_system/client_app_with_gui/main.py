import sys
from PyQt5 import QtWidgets, QtCore
import backend

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wpisz wymagane dane aby zagłosować")
        self.setMinimumWidth(380)

        layout = QtWidgets.QVBoxLayout(self)

        self.input_token = QtWidgets.QLineEdit(placeholderText="Wpisz wartość tokena...")
        self.input_token.returnPressed.connect(self.on_click)
        layout.addWidget(self.input_token)

        self.input_token_hash = QtWidgets.QLineEdit(placeholderText="Wpisz hash tokena...")
        self.input_token_hash.returnPressed.connect(self.on_click)
        layout.addWidget(self.input_token_hash)

        self.input_vote = QtWidgets.QLineEdit(placeholderText="Wpisz głos...")
        self.input_vote.returnPressed.connect(self.on_click)
        layout.addWidget(self.input_vote)

        self.input_address_sc = QtWidgets.QLineEdit(placeholderText="Wpisz adres smart kontraktu...")
        self.input_address_sc.returnPressed.connect(self.on_click)
        layout.addWidget(self.input_address_sc)

        self.input_address = QtWidgets.QLineEdit(placeholderText="Wpisz adres konta...")
        self.input_address.returnPressed.connect(self.on_click)
        layout.addWidget(self.input_address)

        self.btn = QtWidgets.QPushButton("Zagłosuj")
        self.btn.clicked.connect(self.on_click)
        layout.addWidget(self.btn)

        self.btn_gr = QtWidgets.QPushButton("Pobierz wynik głosowania")
        self.btn_gr.clicked.connect(self.get_result)
        layout.addWidget(self.btn_gr)

        self.status = QtWidgets.QLabel("Gotowe.")
        self.status.setStyleSheet("color: gray;")
        layout.addWidget(self.status)

    @QtCore.pyqtSlot()
    def on_click(self):
        token = self.input_token.text()
        token_hash = self.input_token_hash.text()
        vote = self.input_vote.text()
        sc_address = self.input_address_sc.text()
        account_address = self.input_address.text()
        try:
            msg = backend.submit_vote(token, token_hash, vote, sc_address, account_address)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Błąd", str(e))
            return

        # self.input.clear()
        self.status.setText(msg)
        QtWidgets.QMessageBox.information(self, "Oddano głos", msg)

    @QtCore.pyqtSlot()
    def get_result(self):
        sc_address = self.input_address_sc.text()
        try:
            msg = backend.get_vote_status_(sc_address)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Błąd", str(e))
            return
        self.status.setText(msg)
        QtWidgets.QMessageBox.information(self, "Wynik:", msg)


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
