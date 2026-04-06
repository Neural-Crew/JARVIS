from backend.persistence.Model.climatrack_model import ClimatrackModel
from backend.persistence.Model.aquacheck_model import AquacheckModel

class EcowatchCreator:
    @staticmethod
    def getTypeEcowatchModel(table):
        class_name = table.capitalize() + 'Model'
        ALLOWED_CLASSES = { "ClimatrackModel", "AquacheckModel" }
        if class_name in ALLOWED_CLASSES:
            return globals()[class_name]
        else: 
            raise Exception(f'class not allowed : {class_name}')
        