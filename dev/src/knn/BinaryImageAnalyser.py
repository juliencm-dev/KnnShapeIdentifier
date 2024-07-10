import numpy as np


class BinaryImageAnalyser:

    # Lazy evaluation

    def __init__(self) -> None:
        self.__image = None
        self.__area_val = None
        self.__centroid_val = None
        self.__distance_max_val = None
        self.__distance_min_val = None
        self.__perimeter_val = None

    def setup(self, image):
        self.__image = image
        self.__area_val = None
        self.__centroid_val = None
        self.__distance_max_val = None
        self.__distance_min_val = None
        self.__perimeter_val = None

    @property
    def area(self):
        if not self.__area_val:
            self.__area_val = self.__calc_area()
        return self.__area_val

    @property
    def centroid(self):
        if not self.__centroid_val:
            self.__centroid_val = self.__calc_centroid()
        return self.__centroid_val

    @property
    def distance_max(self):
        if not self.__distance_max_val:
            self.__distance_max_val = self.__calc_distance_max()
        return self.__distance_max_val

    @property
    def distance_min(self):
        if not self.__distance_min_val:
            self.__distance_min_val = self.__calc_distance_min()
        return self.__distance_min_val

    @property
    def perimeter(self):
        if not self.__perimeter_val:
            self.__perimeter_val = self.__calc_perimeter()
        return self.__perimeter_val

    def __calc_area(self):
        return self.__image[self.__image == 0].size

    # def __calc_perimeter(self):
    #     core = self.__image[1:-1, 1:-1]
    #     core_mask = np.logical_or(
    #         np.logical_or(np.logical_and(core == 0, self.__image[0:-2, 1:-1] == 1), np.logical_and(core == 0, self.__image[2:, 1:-1] == 1)),
    #         np.logical_or(np.logical_and(core == 0, self.__image[1:-1, 0:-2] == 1), np.logical_and(core == 0, self.__image[1:-1, 2:] == 1)))
    #
    #     perimeter_image = core_mask.astype(np.int8)
    #
    #     perimeter_image = np.pad(perimeter_image, 1, 'constant', constant_values=0)
    #
    #     core = perimeter_image[1:-1, 1:-1]
    #     core_mask = np.logical_or(
    #         np.logical_and(np.logical_and(core == 1, perimeter_image[0:-2, 1:-1] == 1), np.logical_and(core == 1, perimeter_image[2:, 1:-1] == 1)),
    #         np.logical_and(np.logical_and(core == 1, perimeter_image[1:-1, 0:-2] == 1), np.logical_and(core == 1, perimeter_image[1:-1, 2:] == 1)))
    #
    #     diagonals = np.zeros(core_mask.shape, dtype=np.float32)
    #     diagonals[core_mask] = np.sqrt(2)
    #
    #     return np.sum(diagonals) + np.sum(perimeter_image) - np.count_nonzero(diagonals)

    def __calc_perimeter(self):
        return np.sum(np.logical_or(
                    np.logical_or(np.logical_and(self.__image[1:-1, 1:-1] == 0, self.__image[0:-2, 1:-1] == 1), np.logical_and(self.__image[1:-1, 1:-1] == 0, self.__image[2:, 1:-1] == 1)),
                    np.logical_or(np.logical_and(self.__image[1:-1, 1:-1] == 0, self.__image[1:-1, 0:-2] == 1),  np.logical_and(self.__image[1:-1, 1:-1] == 0, self.__image[1:-1, 2:] == 1))))

    def __calc_centroid(self):
        ix, iy = np.where(self.__image == 0)
        return (int(np.sum(ix) / self.area), int(np.sum(iy) / self.area))

    def __calc_distance_max(self) -> float:
        cx, cy = self.centroid
        x, y = np.where(self.__image == 0)
        distances = (x - cx) ** 2 + (y - cy) ** 2

        return np.max(distances)

    def __calc_distance_min(self) -> float:
        cx, cy = self.centroid

        if self.__image[cx, cy] == 0:
            x, y = np.where(self.__image == 1)
        else:
            x, y = np.where(self.__image == 0)

        distances = (x - cx) ** 2 + (y - cy) ** 2

        return np.min(distances)
