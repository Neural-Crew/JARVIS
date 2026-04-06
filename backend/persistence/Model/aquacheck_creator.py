from backend.persistence.Model.aquacheck_model import AquacheckModel
from backend.persistence.Model.ecowatch_creator import EcowatchCreator

class AquacheckCreator(EcowatchCreator):
    def donnerTypeEcowatchModel(self):
        return AquacheckModel