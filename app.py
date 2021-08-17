from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
model = pickle.load(open('./ml_model.pkl', 'rb'))


@app.route('/', methods=['GET'])
def Home():
    return render_template('home.html')


standard_to = StandardScaler()


@app.route("/predict", methods=['POST'])
def predict():
    CURRENT_YEAR = 2021
    Fuel_Type_Diesel = 0

    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        Kms_Driven2 = np.log(Kms_Driven)
        Owner = int(request.form['Owner'])
        Fuel_Type_Petrol = request.form['Fuel_Type_Petrol']
        Seller_Type_Individual = request.form['Seller_Type_Individual']
        Transmission_Mannual = request.form['Transmission_Mannual']

        car_details = {
            'year': Year,
            'price': Present_Price,
            'kms': Kms_Driven,
            'owner': Owner,
            'fuel_type': Fuel_Type_Petrol,
            'seller': Seller_Type_Individual,
            'trans': Transmission_Mannual,
        }

        if (Fuel_Type_Petrol == 'Petrol'):
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1

        if (Seller_Type_Individual == 'Individual'):
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0

        if (Transmission_Mannual == 'Mannual'):
            Transmission_Mannual = 1
        else:
            Transmission_Mannual = 0

        Year = CURRENT_YEAR - Year

        prediction = model.predict([[Present_Price, Kms_Driven2, Owner, Year, Fuel_Type_Diesel, Fuel_Type_Petrol,
                                     Seller_Type_Individual, Transmission_Mannual]])
        output = round(prediction[0], 2)

        if output < 0:
            return render_template('home.html', prediction_texts="Sorry, we cannot predict the price.")
        else:
            return render_template('home.html', prediction_text="Selling Price: {}".format(output),
                                   car_details=car_details)
    else:
        return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=False)
