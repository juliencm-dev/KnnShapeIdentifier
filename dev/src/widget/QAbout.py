from PySide6.QtWidgets import QWidget, QPushButton, QMessageBox, QVBoxLayout
import os

class QAbout(QWidget):
    def __init__(self):
        super().__init__()

        # Créer un bouton
        btn = QPushButton('About', self)
        btn.clicked.connect(self.__show_message_box)

        # Définir la disposition
        layout = QVBoxLayout(self)
        layout.addWidget(btn)

        # Définir la disposition principale du widget
        self.setLayout(layout)
    

    def __show_message_box(self) -> None:
        # Lire le contenu du fichier texte
        image_path = 'about.txt'
        try:
            script_directory = os.path.dirname(os.path.realpath(__file__))
            image_full_path = os.path.join(script_directory, image_path)
            with open(image_full_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            content = 'Fichier introuvable.'

        # Afficher un QMessageBox avec le contenu du fichier
        QMessageBox.about(self, 'Contenu du fichier', content)

