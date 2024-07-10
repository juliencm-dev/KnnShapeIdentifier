from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import (QLabel, QPushButton, 
                               QVBoxLayout, QComboBox, QGroupBox) 

from PySide6.QtGui import QPixmap, QImage

from __feature__ import snake_case, true_property


class QPreview(QGroupBox):

    indexChanged = Signal(int)
    eventTriggered = Signal()

    def __init__(self, title: str, action: str, parent = None) -> None:
        super().__init__(title, parent)

        self.__combo_box = QComboBox(self)
        self.__image_display = QLabel(self)
        
        self.__action_btn = QPushButton(self)
        self.__action_result = QLabel(self)

        self.__combo_box.minimum_width = 200
        self.__combo_box.currentIndexChanged.connect(self.__index_changed)

        self.__action_btn.text = action
        self.__action_btn.clicked.connect(self.__event_trigger)
    

        layout = QVBoxLayout(self)
        layout.add_widget(self.__combo_box)
        layout.add_widget(self.__image_display, alignment=Qt.AlignCenter)
        layout.add_widget(self.__action_btn)
        layout.add_widget(self.__action_result, alignment=Qt.AlignCenter)


    @property
    def action_result(self) -> str:
        return self.__action_result.text
    @action_result.setter
    def action_result(self, value: str) -> None:
        self.__action_result.text = value

    ##################################

    #TODO: PARLER AU PROF
    @property
    def item(self) -> str:
        return self.__combo_box.current_text
    @item.setter
    def item(self, value: str) -> None:
        self.__combo_box.add_item(value)
        
    @property
    def items(self) -> str:
        raise "Cannot Read Property Value"
    @item.setter
    def items(self, values: list[str]) -> None:
        self.__combo_box.clear()
        self.__combo_box.add_items(values)

    ##################################

    def set_image(self, image: QImage) -> None:
        if image is not None:
            pixmap = QPixmap(image)
            self.__image_display.pixmap = pixmap

    @Slot()
    def __index_changed(self, idx) -> None:
        self.indexChanged.emit(idx)

    @Slot()
    def __event_trigger(self) -> None:
        self.eventTriggered.emit()
