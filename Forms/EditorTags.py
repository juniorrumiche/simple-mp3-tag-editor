import io
import os

from PIL import Image
import music_tag
from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QMessageBox, QPushButton, QStyle, QFileDialog


class Mp3EditorTags(QDialog):
    pick_image_path = None

    def __init__(self, parent=None, path: str = None):
        super(Mp3EditorTags, self).__init__(parent)
        self.path = path  # mp3 full path
        self.setWindowTitle("MP3 Tag Editor")
        self.setFixedSize(490, 350)
        self.setStyleSheet("QLineEdit{\n"
                           "border: 1px solid gray;\n"
                           "border-radius: 8px;\n"
                           "padding: 0px 5px;\n"
                           "    font: 10pt \"MS Shell Dlg 2\";\n"
                           "\n"
                           "}\n"
                           "QPushButton{\n"
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
                           "QLabel{\n"
                           "font: 75 10pt \"MS Shell Dlg 2\";\n"
                           "\n"
                           "}")
        self.label_filename = QLabel(self)
        self.label_filename.setGeometry(QtCore.QRect(10, 5, 450, 13))
        QLabel("Title: ", self).setGeometry(QtCore.QRect(235, 30, 47, 13))
        QLabel("Artist: ", self).setGeometry(QtCore.QRect(235, 77, 47, 13))
        QLabel("Album: ", self).setGeometry(QtCore.QRect(235, 124, 47, 13))
        QLabel("Genre: ", self).setGeometry(QtCore.QRect(235, 172, 47, 13))
        QLabel("Year: ", self).setGeometry(QtCore.QRect(235, 222, 47, 13))

        self.mp3_title = QLineEdit(self)
        self.mp3_title.setGeometry(QtCore.QRect(285, 26, 191, 23))

        self.mp3_artist = QLineEdit(self)
        self.mp3_artist.setGeometry(QtCore.QRect(285, 73, 191, 23))

        self.mp3_album = QLineEdit(self)
        self.mp3_album.setGeometry(QtCore.QRect(285, 120, 191, 23))

        self.mp3_genre = QLineEdit(self)
        self.mp3_genre.setGeometry(QtCore.QRect(285, 168, 191, 23))

        self.mp3_artwork = QLabel(self)
        self.mp3_artwork.setGeometry(QtCore.QRect(10, 30, 210, 210))
        self.mp3_artwork.setStyleSheet("padding: 0px;\n"
                                       "border-radius: 5px;\n"
                                       "border: 2px solid gray;\n")
        self.mp3_artwork.setAlignment(QtCore.Qt.AlignCenter)

        self.btn_pick_image = QPushButton("", self)
        self.btn_pick_image.setGeometry(QtCore.QRect(180, 33, 35, 30))
        self.btn_pick_image.setToolTip("Change Image ")
        self.btn_pick_image.setIcon(self.style().standardIcon(QStyle.SP_FileDialogNewFolder))
        self.btn_pick_image.clicked.connect(self.open_pick_image)

        self.mp3_year = QLineEdit(self)
        self.mp3_year.setGeometry(QtCore.QRect(285, 218, 191, 23))

        self.btn_save = QPushButton("Guardar", self)
        self.btn_save.setGeometry(QtCore.QRect(320, 260, 125, 33))
        self.btn_save.clicked.connect(self.save_tags)
        self.get_artist()

    def pil2pixmap(self, img):
        im = img.resize((210, 210))
        if im.mode == "RGB":
            r, g, b = im.split()
            im = Image.merge("RGB", (b, g, r))
        elif im.mode == "RGBA":
            r, g, b, a = im.split()
            im = Image.merge("RGBA", (b, g, r, a))
        elif im.mode == "L":
            im = im.convert("RGBA")
        # Bild in RGBA konvertieren, falls nicht bereits passiert
        im2 = im.convert("RGBA")
        data = im2.tobytes("raw", "RGBA")
        qim = QImage(data, im.size[0], im.size[1], QImage.Format_ARGB32)
        pixmap = QPixmap.fromImage(qim)
        return pixmap

    def get_artist(self):
        f = music_tag.load_file(self.path)
        if f['artwork'].first is not None:
            image = Image.open(io.BytesIO(f['artwork'].first.data))
            self.mp3_artwork.setPixmap(self.pil2pixmap(image))
        self.mp3_title.setText(f['title'].value)
        self.mp3_artist.setText(f['artist'].value)
        self.mp3_album.setText(f['album'].value)
        self.mp3_genre.setText(f['genre'].value)
        self.mp3_year.setText(str(f['year']))
        self.label_filename.setText(f"Archivo: {self.path}")

    def rename_file(self, title: str, artist: str):
        filename = f"{title.title()} - {artist.title()}.mp3"
        path = self.path.split('/')
        del path[-1]
        new_path = ''
        for p in path:
            new_path += f"{p}/"
        filename = f"{new_path}{filename}"
        try:
            os.rename(self.path, filename)
            self.path = filename
        except Exception as e:
            print(str(e))

    def save_tags(self):

        f = music_tag.load_file(self.path)
        f['year'] = None
        if self.pick_image_path is not None:
            with open(self.pick_image_path, "rb") as img_pick:
                f['artwork'] = img_pick.read()
        if self.mp3_year.text().isnumeric():
            f['year'] = self.mp3_year.text()

        f['title'] = self.mp3_title.text().title()
        f['artist'] = self.mp3_artist.text().title()
        f['album'] = self.mp3_album.text().title()
        f['genre'] = self.mp3_genre.text().title()
        self.msg = QMessageBox()
        try:
            f.save()
            self.rename_file(self.mp3_title.text(), self.mp3_artist.text())
            self.msg.setText("Metadatos Actualizados con exito")
            self.msg.setWindowTitle("Exito")
            self.get_artist()
        except Exception as e:
            self.msg.setText(f" ha Ocurrido un error {str(e)}")
            self.msg.setWindowTitle("Error")
        finally:
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.show()

    def open_pick_image(self):
        options = QFileDialog().options()
        filename, _ = QFileDialog.getOpenFileName(self, "Abrir Archivo", "", "Image Files (*.jpg);;(*.png)",
                                                  options=options)
        if filename:
            self.pick_image_path = filename
        else:
            self.pick_image_path = None
