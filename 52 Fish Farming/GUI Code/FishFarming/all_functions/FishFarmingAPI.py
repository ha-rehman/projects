import pickle


class FishFarmingEvaluation:

    def __init__(self, model_path):
        self.model = pickle.load(open(model_path, "rb"))

    def predict(self, Temperature, Tubidity, Dissolved_Oxygen, PH, Ammonia, Nitrate, Fish_Length, Fish_Weight):
        return \
            self.model.predict(
                [[Temperature, Tubidity, Dissolved_Oxygen, PH, Ammonia, Nitrate, Fish_Length, Fish_Weight]])[
                0]
