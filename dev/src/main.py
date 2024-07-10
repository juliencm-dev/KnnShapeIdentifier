from sys import argv, exit
from PySide6.QtWidgets import QApplication, QMainWindow
from widget.QKnnApp import QKnnApp


from __feature__ import snake_case, true_property

def main():
    app = QApplication(argv)
    app_widget = QKnnApp()
    
    window = QMainWindow()
    window.resize(1450, 800)
    window.set_central_widget(app_widget)
    window.show()

    exit(app.exec())
    

if __name__ == '__main__':
    main()