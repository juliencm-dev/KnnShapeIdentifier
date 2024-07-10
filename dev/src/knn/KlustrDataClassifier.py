import numpy as np
from prof_utils.klustr_utils import ndarray_from_qimage_argb32
from knn.BinaryImageAnalyser import BinaryImageAnalyser


class KlustrDataClassifier:
    img_analysis = BinaryImageAnalyser()

    @staticmethod
    def classify(image=None) -> tuple:
        # image is a QImage
        if image:
            array_img = ndarray_from_qimage_argb32(image)
            KlustrDataClassifier.img_analysis.setup(array_img)

        return ((KlustrDataClassifier.__1_isoperimetric_quotient(), KlustrDataClassifier.__2_centroid_area_ratio(),
                 KlustrDataClassifier.__3_ratio_min_max_radius()))

    @staticmethod
    def train(images: list, types: list) -> list:
        training_data = []

        for image, type in zip(images, types):
            array_img = ndarray_from_qimage_argb32(image)
            KlustrDataClassifier.img_analysis.setup(array_img)
            training_data.append((KlustrDataClassifier.classify(), type))

        return training_data

    # __1_isoperimetric_quotient : 4pi * Aire / Perimetre^2 -> cercle = 1

    @staticmethod
    def __1_isoperimetric_quotient() -> float:
        result = (4 * np.pi * KlustrDataClassifier.img_analysis.area) / (
                    KlustrDataClassifier.img_analysis.perimeter ** 2)

        # if result > 1: return 1

        return result

    @staticmethod
    # __2_centroid_area_ratio : Aire Cercle - Aire Shape / Aire Cercle -> cercle = 0
    def __2_centroid_area_ratio() -> float:
        radius = KlustrDataClassifier.img_analysis.distance_max
        centroid_circle_area = np.pi * radius

        return (centroid_circle_area - KlustrDataClassifier.img_analysis.area) / centroid_circle_area

    @staticmethod
    # __3_ratio_min_max_radius : radius_diff(max-min) / radius_max -> full shape = roughly 1
    def __3_ratio_min_max_radius() -> float:
        radius_max = KlustrDataClassifier.img_analysis.distance_max
        radius_min = KlustrDataClassifier.img_analysis.distance_min

        radius_diff = radius_max - radius_min
        radius_ratio = radius_diff / radius_max

        return radius_ratio
