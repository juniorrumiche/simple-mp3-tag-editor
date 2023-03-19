from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QApplication, QFileDialog, QMessageBox, QStyle
from PyQt5 import QtCore
from Forms.EditorTags import Mp3EditorTags


class Mp3OpenFile(QDialog):
    def __init__(self, parent=None):
        super(Mp3OpenFile, self).__init__(parent)
        self.setWindowTitle("MP3 Open File")
        self.setFixedSize(478, 104)
        self.setStyleSheet("QPushButton{\n"
                           "    border: 1px solid gray;\n"
                           "    border-radius: 10px;\n"
                           "    background-color: #00897b;\n"
                           "    color: white;\n"
                           "    font: 75 10pt \"MS Shell Dlg 2\";\n"
                           "}\n"
                           "QPushButton:hover{\n"
                           "background-color:#005b4f;\n"
                           "    \n"
                           "}\n"
                           "QPushButton:pressed{\n"
                           "background-color:#4ebaaa;\n"
                           "\n"
                           "}\n"
                           "\n"
                           "QLineEdit{\n"
                           "    border: 1px solid gray;\n"
                           "    border-radius: 10px;\n"
                           "    color:gray;\n"
                           "}\n"
                           "")
        self.full_path = QLineEdit(self)
        self.full_path.setGeometry(QtCore.QRect(20, 30, 346, 36))
        self.full_path.setReadOnly(True)
        self.btn_open_file = QPushButton(" Abrir", self)
        self.btn_open_file.setIcon(self.style().standardIcon(QStyle.SP_DirIcon))
        self.btn_open_file.setGeometry(QtCore.QRect(376, 30, 80, 36))
        self.btn_open_file.clicked.connect(self.open_mp3_file)

    def open_mp3_file(self):
        options = QFileDialog().options()
        filename, _ = QFileDialog.getOpenFileName(self, "Abrir Archivo", "", "Mp3 File (*.mp3)",
                                                  options=options)
        if filename:
            self.dialog = Mp3EditorTags(self, filename)
            self.full_path.setText(filename)
            self.dialog.show()
        else:
            self.full_path.setText(filename)
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText('Debes seleccionar un archivo')
            self.msg.show()
            self.msg.setWindowTitle("Error")
