from backend.persistence.Model.ecowatch_creator import EcowatchCreator
from backend.persistence.Model.climatrack_model import ClimatrackModel

class ClimatrackCreator(EcowatchCreator):
    def donnerTypeEcowatchModel(self):
        return ClimatrackModel