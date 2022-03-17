import Main_form
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #main_form = Main_form.Main_Form()
    Logo_form = Main_form.Logo_Form()
    app.exec_()
    