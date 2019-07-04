from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QComboBox, QApplication, QWidget, QScrollArea, QVBoxLayout, QGroupBox, QLabel, QPushButton, QFormLayout
import sys
from db_connect import Database
from ui.ui import GnomeDialog
DB = Database()
from drivers.key_dict import key_dict
from ui.resource_to_exe import resource_path

class Ui_Dialog(QWidget):
    def __init__(self, main, spec):
        super().__init__()
        self.GnomeDialog = None
        main.hide()
        self.oldPos = self.pos()
        self.title = "Bind settings"
        self.resize(554, 535)
        self.bg = QLabel(self)
        self.bg.setGeometry(QtCore.QRect(0, 0, 581, 591))
        self.bg.setText("")
        self.bg.setPixmap(QtGui.QPixmap("ui/img/binds/binds_bg.png"))
        self.bg.setObjectName("bg")
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
        self.formLayout = QFormLayout()
        groupBox = QGroupBox("")
        self.widget_list = {}
        abilitys = DB.query(f"select * from {spec}")
        self.input_waiting = None
        for idx, spell in enumerate(abilitys, start=1):
            bind = QPushButton()
            #if abil[2] is not None: bind.addItem(abil[2])
            if spell[2] is None:
                bind.setText('CLICK TO BIND')
            else:
                bind.setText(spell[2])
            bind.setMinimumSize(QtCore.QSize(85, 28))
            bind.setStyleSheet("background-color: silver;")
            spell_label = QLabel(f'{spell[0]}*' if spell[3] else spell[0])
            spell_label.setFont(font)
            spell_label.setStyleSheet("color: silver;")
            spell_label.setMinimumSize(QtCore.QSize(0, 28))
            self.widget_list.update({spell_label: bind})
            self.widget_list[spell_label].setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.widget_list[spell_label].clicked.connect(lambda state, key=spell_label: self.key_input(key))
            self.formLayout.addRow(self.widget_list[spell_label], spell_label)
        groupBox.setLayout(self.formLayout)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        scroll.setFixedSize(480, 367)
        scroll.setStyleSheet("background-color:transparent;")
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        close_ = QLabel(self)
        close_.setGeometry(477, 39, 20, 20)
        close_.mousePressEvent = lambda event: self.close_(main)
        save = QLabel(self)
        save.setGeometry(150, 470, 201, 61)
        save.mousePressEvent = lambda event: self.save(main, spec)
        move_label = QLabel(self)
        move_label.mousePressEvent = lambda event: self.move_pressed(event)
        move_label.setGeometry(2, 36, 473, 41)
        self.m_label = False #  Флаг нажатия на Label для перемещения окна
        self.show()

    def key_input(self, spell_label):
        if self.input_waiting is None:
            self.input_waiting = spell_label
            self.widget_list[spell_label].setText('PRESS KEY')
            self.widget_list[spell_label].setStyleSheet("background-color: #606060;")
        elif self.input_waiting == spell_label:
            self.input_waiting = None
            self.widget_list[spell_label].setText('CLICK TO BIND')
            self.widget_list[spell_label].setStyleSheet("background-color: silver;")
        else:
            self.widget_list[self.input_waiting].setText('CLICK TO BIND')
            self.widget_list[self.input_waiting].setStyleSheet("background-color: silver;")
            self.input_waiting = spell_label
            self.widget_list[spell_label].setText('PRESS KEY')
            self.widget_list[spell_label].setStyleSheet("background-color: #606060;")

    def close_(self, main):
        main.show()
        self.close()

    def save(self, main, spec):
        try:
            DB.execute(f'UPDATE {spec} SET bind=Null')
            for spell, bind in self.widget_list.items():
                new_bind = self.widget_list[spell].text()
                DB.execute(f'UPDATE {spec} SET bind=? WHERE spell=?', (None if len(new_bind) > 3
                                                                       else new_bind,
                                                                       spell.text()[:-1] if '*' in spell.text()
                                                                       else spell.text()))
            DB.commit()
        except Exception as E:
            if 'UNIQUE' in repr(E).upper():
                if self.GnomeDialog:
                    self.GnomeDialog.close()
                self.GnomeDialog = GnomeDialog(14, "\n\n\nYou can't bind one button twice", True, self)
                self.GnomeDialog.show()
            print(E)
            return
        if self.GnomeDialog:
            self.close()
        main.show()
        self.close()

    def set_text(self, text):
        self.widget_list[self.input_waiting].setText(text)
        self.widget_list[self.input_waiting].setStyleSheet("background-color: silver;")
        self.input_waiting = None

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() in (16777216, 16777249, 16777251, 16777248):  # esc
            if self.input_waiting:
                self.set_text('CLICK TO BIND')
        elif len(str(QKeyEvent.key())) == 4 and str(QKeyEvent.key())[:2] == '10':
            if self.GnomeDialog:
                self.GnomeDialog.close()
            self.GnomeDialog = GnomeDialog(14, "\n\n\nYou must change your keyboard layout to ENG, my friend.", True, self)
            self.GnomeDialog.show()
            return
        if self.input_waiting:
            try:
                self.set_text(key_dict[QKeyEvent.key()])
            except Exception as E:
                print(E.args)
                if self.GnomeDialog:
                    self.GnomeDialog.close()
                self.GnomeDialog = GnomeDialog(14, "\n\n\nOops, i guess you can bind only 0-9, F1-F12, A-Z keys",
                                               True, self)
                self.GnomeDialog.show()
                self.set_text('CLICK TO BIND')
                return

    def move_pressed(self, event):
        self.oldPos = event.globalPos()
        self.m_label = True


    def mouseReleaseEvent(self, QMouseEvent):
        if self.input_waiting:
            self.set_text('CLICK TO BIND')
        self.m_label = False

    def mouseMoveEvent(self, event):
        if self.m_label:
            delta = QtCore.QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()