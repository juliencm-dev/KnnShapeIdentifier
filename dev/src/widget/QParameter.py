from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import (QLabel, QWidget, 
                               QVBoxLayout, QHBoxLayout, QScrollBar, QGroupBox, QSizePolicy) 

from __feature__ import snake_case, true_property


class QLabelledSlider(QWidget):

    eventTriggered = Signal(float or int)

    def __init__(self, title:str, range:tuple, sb_start_value:int, is_decimal:bool) -> None:
        super().__init__()

        self.__is_decimal = is_decimal
        self.__sb_value = sb_start_value
        self.__widget_title = title

        self.__label = QLabel(self)
        self.__label.size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.__label.text = f'{self.widget_title} = {self.sb_value}'
        self.__label.alignment = Qt.AlignCenter
        self.__label.minimum_width = 100
        
        self.__scrollbar = QScrollBar(self)
        self.__scrollbar.size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.__scrollbar.orientation = Qt.Horizontal

        if self.__is_decimal:
            min, max = range
            self.__scrollbar.set_range(min, max * 100)
            self.__scrollbar.value = sb_start_value * 100
        else:
            self.__scrollbar.set_range(*range)
            self.__scrollbar.value = sb_start_value

        self.__scrollbar.minimum_width = 200

        self.__scrollbar.valueChanged.connect(self.__update_value)

        layout = QHBoxLayout(self)
        layout.add_widget(self.__label)
        layout.add_widget(self.__scrollbar)

    @property
    def sb_value(self) -> float:
        return self.__sb_value
    @sb_value.setter
    def sb_value(self, value) -> None:
        self.__sb_value = value

    @property
    def widget_title(self) -> str:
        return self.__widget_title
    
    def set_new_range(self, range:tuple) -> None:
        self.__scrollbar.set_range(*range)
        
    def set_recommenced(self, value:int) -> None:
        self.__scrollbar.value = value

    @Slot()
    def __update_value(self) -> None:
        if self.__is_decimal:
            self.__label.text = f'{self.widget_title} = {self.__scrollbar.value / 100}'
            self.sb_value = self.__scrollbar.value / 100
        else:
            self.__label.text = f'{self.widget_title} = {self.__scrollbar.value}'
            self.sb_value = self.__scrollbar.value

        self.eventTriggered.emit(self.sb_value)


class QParameter(QGroupBox):
    # Pass a list of dictionaries as arguments    
    ACCEPTABLE_KEY_VALUE = ('title', 'range', 'sb_start_value', 'is_decimal')

    def __init__(self, title:str, *args, parent = None) -> None:
        super().__init__(title, parent)
        self.__parameters = []

        for arg in args:
            for item in arg:
                if not all(key in QParameter.ACCEPTABLE_KEY_VALUE for key in item.keys()):
                    raise ValueError(f'Unacceptable key value in keys: {item.keys()}')
                else:
                    self.__parameters.append(QLabelledSlider(item['title'], item['range'], item['sb_start_value'], item['is_decimal']))
        
        layout = QVBoxLayout(self)

        for parameter in self.__parameters:
            layout.add_widget(parameter)

    
    @property
    def parameters(self) -> list[QLabelledSlider]:
        return self.__parameters
