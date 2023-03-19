import sys
from PyQt5.QtWidgets import QApplication
from Forms.mp3OpenFile import Mp3OpenFile

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Mp3OpenFile()
    window.show()
    sys.exit(app.exec_())
