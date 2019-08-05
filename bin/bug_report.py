from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from bin.Qt.bug_report_Qt import Ui_Dialog as Ui_BugReportDialog
import os
from bin.gnome import GnomeDialog
import shutil

#  pyuic5 bug_report.ui -o bug_report_Qt.py

class BugReportDialog(QtWidgets.QDialog):
    def __init__(self, main, parent=None):
        super(BugReportDialog, self).__init__(parent)
        from db_connect import Database
        self.DB = Database()
        self.main = main
        self.main.hide()
        self.oldPos = self.pos()
        self.ui = Ui_BugReportDialog()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground | QtCore.Qt.WA_TranslucentBackground)
        self.ui.close_.mousePressEvent = lambda event: self._exit(main)
        self.ui.choose_screen.clicked.connect(self.scr_attach)
        self.ui.send.clicked.connect(self.send)
        self.ui.text.textChanged.connect(self.len_handler)
        self.attachments = list()
        self.system = list()
        self.binds = list()
        font = QtGui.QFont()
        font.setFamily("Futura-Normal")
        font.setPointSize(8)
        self.ui.len_limit.setFont(font)

    def send(self):
        # Не отправлять пустоту
        if len(self.ui.text.toPlainText()) == 0 and self.ui.scr_count.intValue() == 0:
            return
        # Создание временной папки
        appdata = os.path.join(os.environ['APPDATA'], 'ApplicationData')
        folder_path = os.path.join(appdata, 'bug_report')
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        else:
            shutil.rmtree(folder_path)
            os.makedirs(folder_path)
        # Добавление объектов в папку
        # Загрузка скриншотов
        for idx, bytes_ in enumerate(self.attachments):
            with open(os.path.join(folder_path, f'{idx}.jpg'), 'wb') as file:
                file.write(bytes_)
        try:  # В случае, если проблема с базой данных
            # TODO Загрузка логов
            # Загрузка системных файлов
            self.system = self.DB.query('select * from system')
            with open(os.path.join(folder_path, 'system.txt'), 'w') as system_file:
                # Форматирование с переносом строки для наглядности
                system_file.write('\n'.join(str(x) for x in self.system))
            # Загрузка биндов
            spec = self.DB.query('select data from system where variable="spec"')[0][0]
            self.binds = self.DB.query(f'select * from {spec}')
            with open(os.path.join(folder_path, 'binds.txt'), 'w') as binds_file:
                # Форматирование с переносом строки для наглядности
                binds_file.write('\n'.join(str(x) for x in self.binds))
        except Exception as E:  # Создание файла с текстом исключения
            with open(os.path.join(folder_path, 'exception.txt'), 'w') as exception_file:
                exception_file.write(repr(E))
        # Загрузка введенного текста проблемы
        with open(os.path.join(folder_path, 'problem.txt'), 'w') as text_file:
            text_file.write(self.ui.text.toPlainText())
        # Создание архива, перенос туда папки
        archive_path = os.path.join(appdata, 'bug_report_archive')
        shutil.make_archive(archive_path, 'zip', folder_path)
        # Удаление временной папки bug_report
        shutil.rmtree(folder_path)
        # Запись архива в биты
        # При создании архива не указывается расширение в пути, но оно необходимо при чтении
        with open(f'{archive_path}.zip', 'rb') as archive:
            archive_bytes = archive.read()
        status_code = self.main.server.bug_report(archive_bytes)
        print(f'File sent: {status_code}')
        self._exit()

    def scr_attach(self):
        count = self.ui.scr_count.intValue()
        if count < 9:
            scr_path = QtWidgets.QFileDialog.getOpenFileName(
                parent=self,
                caption='Attach an image',
                filter="Image Files(*.png *.jpg *.kek)")[0]
            q_file = QtCore.QFile(scr_path)
            if q_file.exists():
                if scr_path[-3:] == 'kek':
                    site_name = self.DB.query('select data from system where variable="site_name"')[0][0]
                    current_text = self.ui.text.toPlainText()
                    gift = 'AF63D1C-03D712-D12734'#  TODO Gift post
                    self.ui.text.setText(f'{gift}'
                                         f'\n/\ This is your gift promo code for a 20% discount on {site_name}'
                                         f'\n\n{current_text}')
                else:
                    if (os.path.getsize(scr_path) / 1024 / 1024) > 5:
                        if not self.main.GnomeDialog:
                            self.main.GnomeDialog = True
                            self.GnomeDialog = GnomeDialog(14, '\n\nSorry, my friend, but\n'
                                                               'file size must not exceed 6 megabytes',
                                                           button=1,
                                                           main=self.main)
                            self.GnomeDialog.show()
                        return
                with open(scr_path, mode='rb') as file:
                    self.attachments.append(file.read()) #  Добавление файла(битами) в массив
                if count == 8: #  9 - ограничитель
                    self.ui.scr_count.setStyleSheet('background-color: red;')
                    self.ui.choose_screen.setVisible(0)
                    self.ui.label_tooltip.setText('It is maximum.')
                self.ui.scr_count.display(count + 1)


    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            event.ignore()
        elif event.key() == QtCore.Qt.Key_Enter:
            self.send()

    def len_handler(self):
        current_length = len(self.ui.text.toPlainText())
        self.ui.len_limit.setText(f'{current_length}/2000')
        if current_length > 2000:
            old_text = self.ui.text.toPlainText()[:2000]
            self.ui.text.setText(old_text)
            cursor = self.ui.text.textCursor()
            cursor.setPosition(2000)
            self.ui.text.setTextCursor(cursor)

    @pyqtSlot()
    def _exit(self):
        if self.main:
            self.main.BugReport = None
            self.main.show()
        self.close()
