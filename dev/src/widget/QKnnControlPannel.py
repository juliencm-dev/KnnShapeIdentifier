from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget
from PySide6.QtGui import QColor
from prof_utils.scatter_3d_viewer import QColorSequence
from widget.QInfoPannel import QInfoPannel
from widget.QParameter import QParameter
from widget.QPreview import QPreview
from widget.QAbout import QAbout
from db.DataBaseManager import DataBaseManager
from knn.Knn import Knn
from knn.KlustrDataClassifier import KlustrDataClassifier
import numpy as np


from __feature__ import snake_case, true_property


class QKnnControlPannel(QWidget):
    def __init__(self, knn_scatter_3d, parent = None) -> None:
        super().__init__(parent)

        self.__scatter_3d = knn_scatter_3d
        self.__db_manager = DataBaseManager()
        self.__knn = Knn()

        info_data = [
            {'title': 'Included in dataset', 'is_bool': False, 'data_titles': ['Category count', 'Training image count', 'Test image count', 'Total image count']},
            {'title': 'Transformation', 'is_bool': True, 'data_titles': ['Translated', 'Rotated', 'Scaled']}
        ]

        parameters_data = [{'title': 'Knn', 'range': (0, 100), 'sb_start_value': 3, 'is_decimal': False},
                        {'title': 'distance', 'range': (0, 2), 'sb_start_value': 0.5, 'is_decimal': True}
        ]

        self.__knn_info_pannel = QInfoPannel('Dataset', info_data)
        self.__knn_info_pannel.items = self.__db_manager.get_items_possibility_categorie()


        self.__knn_image_preview = QPreview('Single test', 'Classify')
        self.__knn_image_preview.items = self.__db_manager.get_items_possibility_img()
        self.__knn_image_preview.set_image(self.__db_manager.get_image_from_index())
        self.__current_img_selected = 0
        self.__knn_image_preview.action_result = 'Not classified'

        self.__knn_parameters = QParameter('Knn parameters', parameters_data)
        self.__knn_about = QAbout()

        # Signal connections
        self.__knn_info_pannel.eventTriggered.connect(self.__on_box_categories_changed)
        self.__knn_image_preview.indexChanged.connect(self.__on_box_img_changed)
        self.__knn_image_preview.eventTriggered.connect(self.__classify_image)
        self.__knn_parameters.parameters[0].eventTriggered.connect(self.__set_knn_k)
        self.__knn_parameters.parameters[1].eventTriggered.connect(self.__set_knn_distance)

        self.__set_info_values()
        self.__set_training_data()
        
        knn_controls = QVBoxLayout(self)
        knn_controls.add_widget(self.__knn_info_pannel)
        knn_controls.add_widget(self.__knn_image_preview)
        knn_controls.add_stretch()
        knn_controls.add_widget(self.__knn_parameters)
        knn_controls.add_widget(self.__knn_about)

    @Slot()
    def __on_box_categories_changed(self) -> None:
        selected_dataset = self.__knn_info_pannel.item
        selected_dataset_images = self.__db_manager.get_items_possibility_img(selected_dataset)
        self.__set_info_values(selected_dataset)
        self.__set_training_data(selected_dataset)
        self.__knn_image_preview.items = selected_dataset_images
        

    @Slot(int)
    def __on_box_img_changed(self, idx:int = 0) -> None:
        self.__current_img_selected = idx
        self.__knn_image_preview.set_image(self.__db_manager.get_image_from_index(idx, self.__knn_info_pannel.item))
        self.__knn_image_preview.action_result = 'Not classified'

    @Slot()
    def __classify_image(self) -> None:
        image = self.__db_manager.get_image_from_index(self.__current_img_selected, self.__knn_info_pannel.item)
        img_classification_data = KlustrDataClassifier.classify(image)
           
        prediction = self.__knn.prediction(img_classification_data) 
        
        self.__knn_image_preview.action_result = prediction
        self.__scatter_3d.remove_serie('Last classified point') 
        if prediction: 
            temp = []
            x, y, z = img_classification_data
            for i in range(31):    
                temp.append((x - ((i - 15) * 0.005), y, z)) 
                temp.append((x, y - ((i - 15) * 0.005), z)) 
                temp.append((x, y, z - ((i - 15) * 0.005))) 
                            
            self.__scatter_3d.add_serie(np.array(temp), QColor(Qt.black),'Last classified point', 0.05)

    @Slot(int)
    def __set_knn_k(self, value:int) -> None:
        self.__knn.k = value

    @Slot(float)
    def __set_knn_distance(self, value:float) -> None:
        self.__knn.distance_max = value
    
    def __set_info_values(self, dataset_name:str = 'ABC') -> None:
        information_data = self.__db_manager.get_dataset_infos(dataset_name)
        self.__knn_info_pannel.items[0].set_values(information_data[0])
        self.__knn_info_pannel.items[1].set_values(information_data[1])

    # get le training data from db with selected_dataset
    def __set_training_data(self, selected_dataset:str = 'ABC') -> None:
        training_images , training_types = self.__db_manager.get_training_data(selected_dataset)
        self.__knn.training_data = KlustrDataClassifier.train(training_images, training_types)
        
        self.__scatter_3d.clear()
        training_data_by_type = self.__split_training_data_by_type(self.__knn.training_data, self.__knn.training_value_type, self.__knn.class_names)
        for i, training_data in enumerate(training_data_by_type):
            self.__scatter_3d.add_serie(np.array(training_data), QColorSequence.next(), self.__knn.class_names[i], 0.1)
            
        self.__knn_parameters.parameters[0].set_new_range((1, self.__knn.k_max))
        self.__knn_parameters.parameters[0].set_recommenced(self.__knn.k_recommended)
   

    def __split_training_data_by_type(self, training_data, training_value_type, classes):
        amount_of_classes = len(classes)

        training_data_by_type = [[] for _ in range(amount_of_classes)]

        for i, value in enumerate(training_value_type):
            training_data_by_type[value].append(training_data[i])

        return training_data_by_type
    


        