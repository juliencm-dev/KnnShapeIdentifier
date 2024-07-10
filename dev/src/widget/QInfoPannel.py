from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import (QLabel, QWidget, 
                               QVBoxLayout, QHBoxLayout, QComboBox, QGroupBox)

from __feature__ import snake_case, true_property


class QLabelledParameter(QWidget):
    def __init__(self, title, parent = None) -> None:
        super().__init__(parent)
        self.__title = title

        self.__title_label = QLabel()
        self.__title_label.text = f'{title} :'
        self.__title_label.minimum_width = 115
        self.__title_label.alignment = Qt.AlignLeft

        self.__value_label = QLabel()
        self.__value_label.text = 'NULL'
        self.__value_label.minimum_width = 50
        self.__value_label.alignment = Qt.AlignCenter

        layout = QHBoxLayout(self)
        layout.add_widget(self.__title_label)
        layout.add_widget(self.__value_label)

    @property
    def value(self) -> str:
        return self.__value_label.text
    @value.setter
    def value(self, value: str) -> None:
        self.__value_label.text = value

    @property
    def title(self) -> str:
        return self.__title
    
    # def sizeHint(self) -> QSize:
    #     # Calculate preferred size based on content
    #     return QSize(440, self.__title_label.height() + self.__value_label.height())


class QInfoBox(QGroupBox):

    def __init__(self, title:str, is_bool: bool, label_name: list[str], parent = None) -> None:
        super().__init__(title, parent)

        self.__parameters = []
        self.__is_bool = is_bool

        for parameter in label_name:
            self.__parameters.append(QLabelledParameter(parameter))

        layout = QVBoxLayout(self)
        for parameter in self.__parameters:
            layout.add_widget(parameter)

    
    def set_values(self, data: dict) -> None:
        for parameter in self.__parameters:
            if self.__is_bool:
                parameter.value = 'True' if data[parameter.title] else 'False'
            else:
                parameter.value = str(data[parameter.title])



class QInfoPannel(QGroupBox):

    eventTriggered = Signal()
    ACCEPTABLE_KEY_VALUE = ('title', 'is_bool', 'data_titles')

    def __init__(self, title: str, *args, parent = None) -> None:
        super().__init__(title, parent)

        self.__info_boxes = []

        self.__combo_box = QComboBox()
        self.__combo_box.currentIndexChanged.connect(self.__event_trigger)

        self.__combo_box.minimum_width = 440

        for arg in args:
            for item in arg:
                if not all(key in QInfoPannel.ACCEPTABLE_KEY_VALUE for key in item.keys()):
                    raise ValueError(f'Unacceptable key value in keys: {item.keys()}')
                else:
                    self.__info_boxes.append(QInfoBox(item['title'], item['is_bool'], item['data_titles']))
        
        info_box_layout = QHBoxLayout()
        for  info_box in self.__info_boxes:
            info_box_layout.add_widget(info_box)

        layout = QVBoxLayout(self)
        layout.add_widget(self.__combo_box)
        layout.add_layout(info_box_layout)
        
    ##################################
    
    #TODO: PARLER AU PROF
    @property
    def item(self) -> str:
        return self.__combo_box.current_text
    @item.setter
    def item(self, value: str) -> None:
        self.__combo_box.add_item(value)
    
    @property
    def items(self) -> list[QInfoBox]:
        return self.__info_boxes
    @items.setter
    def items(self, values: list[str]) -> None:
        self.__combo_box.clear()
        self.__combo_box.add_items(values)

    ##################################

    @Slot()
    def __event_trigger(self) -> None:
        self.eventTriggered.emit()


    

    