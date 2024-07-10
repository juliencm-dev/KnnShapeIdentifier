import numpy as np
from collections import OrderedDict
from copy import deepcopy


class Knn:
    def __init__(self, k: int = 1, distance_max: float = 0.5) -> None:
        self.__k: int = k

        # Lazy evaluation
        self.__k_max: int = None
        self.__k_recommended = None

        self.__distance_max: float = distance_max
        self.__distance_max_sqrt: float = distance_max ** 2

        self.__training_data: np.uint8 = None
        self.__training_value_type: np.uint8 = None
        self.__class_names: list = None

    @property
    def class_names(self) -> list:
        return self.__class_names

    @class_names.setter
    def class_names(self, value: list) -> None:
        self.__class_names = np.array(value)

    @property
    def k_max(self):
        if not self.__k_max:
            self.__k_max = np.bincount(self.__training_value_type).min()
        return self.__k_max

    @property
    def k_recommended(self):
        if not self.__k_recommended:
            self.__k_recommended = int(np.sqrt(self.__training_data.size) / self.__class_names.size)
        return self.__k_recommended

    @property
    def training_data(self) -> np.uint8:
        return deepcopy(self.__training_data)

    @training_data.setter
    def training_data(self, training_data: list[tuple, any]) -> None:
        self.__reset_parameters()
        data_list, data_type_list = self.__validate_training_data(training_data)

        self.__training_data = np.array(data_list)
        self.__class_names = self.__unique_class_list(data_type_list)
        self.__training_value_type = self.__convert_classes_to_int(data_type_list, self.__class_names)

    @property
    def training_value_type(self) -> np.uint8:
        return self.__training_value_type

    @property
    def k(self) -> int:
        return self.__k

    @k.setter
    def k(self, k: int) -> None:
        self.__k = int(k)

    @property
    def distance_max(self) -> float:
        return self.__distance_max

    @distance_max.setter
    def distance_max(self, distance_max: float) -> None:
        self.__distance_max = distance_max
        self.__distance_max_sqrt = distance_max ** 2

    def set_training_data_single(self, training_data: tuple):
        self.__reset_parameters()

        if not self.__training_data:
            self.__training_data = np.array()
            self.__training_value_type = np.array()

        temp_data = np.concatenate(self.__training_data, np.array(training_data[0]))
        temp_values = np.concatenate(self.__unique_class_list, np.array(training_data[1]))

        self.__data_validation(temp_data, temp_values)

        self.__training_data = temp_data
        self.__class_names = np.array(self.__unique_class_list(temp_values))
        self.__training_value_type = self.__convert_classes_to_int(self.__training_data, self.__class_names)

    def set_training_data_chunk(self, training_data: list[tuple, any]):
        self.__reset_parameters()

        if not self.__training_data:
            self.__training_data = np.array()
            self.__training_value_type = np.array()

        data_list, data_type_list = self.__validate_training_data(training_data)

        temp_data = np.concatenate(self.__training_data, np.array(data_list))
        temp_values = np.concatenate(self.__unique_class_list, np.array(data_type_list))

        self.__training_data = temp_data
        self.__class_names = np.array(self.__unique_class_list(temp_values))
        self.__training_value_type = self.__convert_classes_to_int(self.__training_data, self.__class_names)

    def __distance(self, p_unkwown: tuple) -> float:
        unknown = np.array(p_unkwown)
        return np.sum((self.__training_data - unknown) ** 2, axis=1)

    def prediction(self, p_unkwown: tuple) -> int:
        distances = self.__distance(p_unkwown)

        # Si la distance min est plus grande que la distance max on retourne 0 = non classifié, unknown.
        if np.min(distances) > self.__distance_max_sqrt: return "Unkown"

        # retourne les index des distances triées par ordre croissant
        sorted_distances = np.argsort(distances)
        k_nearest_type = self.__training_value_type[sorted_distances[:self.k]]

        if k_nearest_type.size < self.k: return "Unkown"

        # retourne les k premières valeurs de training_value_type enfonction des index dans sorted_distances
        type_counts = np.bincount(k_nearest_type)
        max_count = type_counts.max()

        if np.sum(type_counts == max_count) > 1:
            avg = []
            avg_type = []

            k_nearest_distances = distances[sorted_distances[:self.k]]
            tied_types = np.where(type_counts == max_count)[0]

            for type in tied_types:
                avg.append(np.mean(k_nearest_distances[k_nearest_type == type]))
                avg_type.append(type)

            # comme ca en cas d'égalité on retourne la valeur avec la moyenne la plus petite.
            return self.__class_names[avg_type[avg.index(min(avg))]]

        return self.__class_names[type_counts.argmax()]

    def __reset_parameters(self):
        self.__k_max = None
        self.__k_recommended = None

    # convertir le training_value_type en int
    def __convert_classes_to_int(self, list_of_names, classes):
        converted_list: int = []
        for name in list_of_names:
            for i, classe in enumerate(classes):
                if name == classe:
                    converted_list.append(i)

        return np.array(converted_list)

    # retourner une liste de classe unique
    def __unique_class_list(self, list_of_class):
        temp_list = deepcopy(list_of_class)
        unique_ordered_dict = OrderedDict.fromkeys(temp_list)
        return np.array(list(unique_ordered_dict))

    def __validate_training_data(self, training_data: list[tuple, any]):
        data_list = []
        data_type_list = []

        for data in training_data:
            data_list.append(data[0])
            data_type_list.append(data[1])

        self.__data_validation(data_list, data_type_list)

        return (data_list, data_type_list)

    def __data_validation(self, data_list: list, data_type_list: list) -> None:
        if len(data_list) != len(data_type_list):
            raise "The shape of the provided data is not coherent."

        try:
            np.array(data_type_list)
        except:
            raise "The Data type provided is not concistent."
