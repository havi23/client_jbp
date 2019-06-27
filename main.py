from ui.ui import MainDialog
import sys
from PyQt5 import QtWidgets
import os

import os


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    main = MainDialog()
    main.show()
    sys.exit(app.exec())
