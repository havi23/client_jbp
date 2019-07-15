from bin.main_window import MainDialog
import sys
import PyQt5
import os




if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication([])
    main = MainDialog()
    main.show()
    sys.exit(app.exec())
