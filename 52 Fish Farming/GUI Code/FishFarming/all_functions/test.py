import pickle

dt_model = pickle.load(open("Dt.pickle", "rb"))

def predict_label(Temperature, Tubidity, Dissolved_Oxygen, PH, Ammonia, Nitrate, Fish_Length, Fish_Weight):
    prediction = dt_model.predict([[Temperature, Tubidity, Dissolved_Oxygen, PH, Ammonia, Nitrate, Fish_Length, Fish_Weight]])[0]
    return prediction

Temperature = -120
Tubidity = 500
Dissolved_Oxygen = 4.5
PH = 8.4
Ammonia = 100
Nitrate = 193
Fish_Length = 7.1
Fish_Weight = 100

prediction = predict_label(Temperature, Tubidity, Dissolved_Oxygen, PH, Ammonia, Nitrate, Fish_Length, Fish_Weight)
print("Status: ", prediction)