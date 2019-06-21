from ui.ui import MainDialog
import sys
from PyQt5 import QtWidgets

app = QtWidgets.QApplication([])
main = MainDialog()
main.show()
sys.exit(app.exec())
