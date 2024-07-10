from db.db_credential import PostgreSQLCredential
from prof_utils.klustr_dao import PostgreSQLKlustRDAO
from prof_utils.klustr_utils import qimage_argb32_from_png_decoding
from prof_utils.klustr_utils import ndarray_from_qimage_argb32
from PySide6.QtGui import QImage

class DataBaseManager():

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataBaseManager, cls).__new__(cls)
            cls._instance.__init()
        return cls._instance

    def __init(self) -> None:
        self.__credential = PostgreSQLCredential(host='localhost', 
                                               port=5432,
                                               database='postgres', 
                                               user='postgres', 
                                               password='Idem181289')
        self.__klustr_dao = PostgreSQLKlustRDAO(self.__credential)

    # set up choix dans box categorie
    def get_items_possibility_categorie(self) -> list[str]:
        if not self.__klustr_dao.is_available:
            print("La connexion à la base de données a échoué. Vérifiez les informations de connexion.")
            return None

        datasets = self.__klustr_dao.available_datasets
        results = []
        for dataset in datasets:
            results.append(dataset[1])

        return results
    
    # recuperer les infos de la bonne categorie
    def get_dataset_infos(self, dataset_name:str) -> list[dict]:
        if not self.__klustr_dao.is_available:
            print("La connexion à la base de données a échoué. Vérifiez les informations de connexion.")
            return None

        datasets = self.__klustr_dao.available_datasets
        results = []
        for dataset in datasets:
            if dataset[1] == dataset_name:
                results = [
                    {'Category count': int(dataset[5]), 'Training image count': int(dataset[6]), 'Test image count': int(dataset[7]), 'Total image count': int(dataset[8])},
                    {'Translated': int(dataset[2]), 'Rotated': int(dataset[3]), 'Scaled': int(dataset[4])}
                ]
                return results
            
        return None
        
    # retourner les images et les valeur du training dataset selectionné
    def get_training_data(self, dataset_name:str):
        if not self.__klustr_dao.is_available:
            print("La connexion à la base de données a échoué. Vérifiez les informations de connexion.")
            return None

        datasets = self.__klustr_dao.image_from_dataset(dataset_name, True)
        images_data = []
        images_type = []
        
        for dataset in datasets:
            # dataset[1] = type      # dataset[6] = image
            images_type.append(dataset[1])
            images_data.append(qimage_argb32_from_png_decoding(dataset[6]))
        
        return (images_data, images_type)  


    # set up choix dans box image
    def get_items_possibility_img(self, dataset_name:str="ABC") -> list[str]:
        if not self.__klustr_dao.is_available:
            print("La connexion à la base de données a échoué. Vérifiez les informations de connexion.")
            return None

        datasets = self.__klustr_dao.image_from_dataset(dataset_name, False)
        results = []
        for dataset in datasets:
            results.append(dataset[3])

        return results

    # recuperer l'image de la bonne categorie avec le bon index
    def get_image_from_index(self, idx=0, dataset_name="ABC") -> QImage:
        # Vérifiez si la connexion à la base de données est réussie
        if not self.__klustr_dao.is_available:
            print("La connexion à la base de données a échoué. Vérifiez les informations de connexion.")
            return

        datasets = self.__klustr_dao.image_from_dataset(dataset_name, False)  #  true = training

        for i, dataset in enumerate(datasets):
            if i == idx:
                return qimage_argb32_from_png_decoding(dataset[6])
            
        return None   
    
    