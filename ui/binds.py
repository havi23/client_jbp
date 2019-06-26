from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QComboBox, QApplication, QWidget, QScrollArea, QVBoxLayout, QGroupBox, QLabel, QPushButton, QFormLayout
import sys
from db_connect import Database
DB = Database()

class Ui_Dialog(QWidget):
    def __init__(self, main, spec):
        super().__init__()
        main.hide()
        self.oldPos = self.pos()
        self.title = "Bind settings"
        self.resize(554, 535)
        self.bg = QLabel(self)
        self.bg.setGeometry(QtCore.QRect(0, 0, 581, 591))
        self.bg.setText("")
        self.bg.setPixmap(QtGui.QPixmap("ui/img/binds/binds_bg.png"))
        self.bg.setObjectName("bg")
        #self.setWindowIcon(QtGui.QIcon("icon.png"))
        #self.setWindowTitle(self.title)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        font = QtGui.QFont()
        font.setFamily("Futura-Normal")
        font.setPointSize(22)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        #self.setGeometry(self.left, self.top, self.width, self.height)
        self.formLayout = QFormLayout()
        groupBox = QGroupBox("")
        widget_list = {}
        bind_list = ['', 'F1', 'F2'] #  TODO ЗАПОЛНИТЬ
        abils = DB.query(f"select * from {spec}")
        for idx, abil in enumerate(abils, start=1):
            bind = QComboBox()
            if abil[2] is not None: bind.addItem(abil[2])
            bind.addItems(bind_list)
            bind.setMinimumSize(QtCore.QSize(0, 28))
            bind.setStyleSheet("background-color: silver; color: black;")
            spell = QLabel(f'{abil[0]}*' if abil[3] else abil[0])
            spell.setFont(font)
            spell.setStyleSheet("color: silver;")
            spell.setMinimumSize(QtCore.QSize(0, 28))
            widget_list.update({spell: bind})
            self.formLayout.addRow(widget_list[spell], spell)
        #for spell, bind in widget_list.items():

        groupBox.setLayout(self.formLayout)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        scroll.setFixedSize(480, 367)
        scroll.setStyleSheet("background-color:transparent;")
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        save = QLabel(self)
        save.setGeometry(150, 470, 201, 61)
        save.mousePressEvent = lambda event: self.save(main, spec, widget_list)
        self.show()

    def save(self, main, spec, widget_list):
        try:
            for spell, bind in widget_list.items():
                new_bind = widget_list[spell].currentText()
                DB.execute(f'UPDATE {spec} SET bind=? WHERE spell=?', (None if new_bind == '' else new_bind,
                                                                       spell.text()))
            DB.commit()
        except Exception as E:
            print('Проблема с уникальностью, либо: ')
            print(E)
            # TODO GNOME!!!
        main.show()
        self.close()

    '''
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
    '''