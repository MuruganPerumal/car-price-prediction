
from flask import Flask, request, jsonify, make_response, render_template
from flask_cors import CORS
import json
# import base64
import pickle

UPLOAD_FOLDER = "D:\Flynava\EK\RawFileReading\\file"

print("model loaded successfully")
r_model = pickle.load(open("random_forest_regression_model.pkl","rb"))

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response
def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


def get_number_of_owner(owner):
    if owner == "one":
        second_owner = 0
        third_owner = 0
        four_above_owner = 0
    elif owner == "two":
        second_owner = 1
        third_owner = 0
        four_above_owner = 0
    elif owner == "three":
        second_owner = 0
        third_owner = 1
        four_above_owner = 0
    else:
        second_owner = 0
        third_owner = 0
        four_above_owner = 1

    return second_owner, third_owner, four_above_owner

def fuel_info(fuel):
    if fuel == "cng":
        Diesel = 0
        Electric = 0
        LPG = 0
        Petrol = 0
    elif fuel == "petrol":
        Diesel = 0
        Electric = 0
        LPG = 0
        Petrol = 1
    elif fuel == "diesel":
        Diesel = 1
        Electric = 0
        LPG = 0
        Petrol = 0
    elif fuel == "lpg":
        Diesel = 0
        Electric = 0
        LPG = 1
        Petrol = 0
        
    else:
        Diesel = 0
        Electric = 1
        LPG = 0
        Petrol = 0

    return Diesel, Electric, LPG, Petrol

def transmission_type(transmission):
    if transmission in "manual":
        manual = 1
    else:
        manual = 0

    return manual

@app.route("/predict", methods=["POST"])
def predict():
    print("-------------- Request started ------------------")
    if request.method == "POST":
        try:
            prediction = 0
            ### Gathering all the information
            # print(1)
            Brand = request.form['brand']
            car = request.form['car']
            model = request.form['model']
            owner = request.form['owner']
            transmission = request.form['transmission']
            fuel = request.form['fuel']
            economy = request.form['economy']
            engine = request.form['engine']
            Power = request.form['power']
            driven = request.form['driven']
            seats = request.form['seats']
            
            ### Transform reqested data into model understandable way
            driven = float(driven)
            economy= float(economy)
            engine= float(engine)
            Power= float(Power)
            seats = float(seats)
            
            print("Parameter transformation = Start")
            ## Get exactly how old is that carr
            model = 2020-int(model)
            print(" -1- Year difference - done")
            # For number of owner
            second_owner, third_owner, four_above_owner = get_number_of_owner(owner)
            print(" -2- no of owner - done")
            # Fuel
            Diesel, Electric, LPG, Petrol = fuel_info(fuel)
            print(" -3- fuel type - done")

            ## Transmission type
            manual = transmission_type(transmission)
            print(" -4- Transmission type - done")
            print("Parameter transform = Completed")
            
            print("Prediction start")
            ## A_Year	Kilometers_Driven	Mileage	Engine	Power	Seats	Fourth & Above	Second	Third	Diesel	Electric	LPG	Petrol	Manual
            prediction = r_model.predict([[model,	driven, economy,	engine,	Power,	seats, four_above_owner,	second_owner,	third_owner,	Diesel,	Electric,	LPG,	Petrol,	manual]])
            print('input data given by user is :')
            print('Brand = {}'.format(Brand))
            print('car = {}'.format(car))
            print('model = {}'.format(model))
            print('owner = {}'.format(owner))
            print('transmission = {}'.format(transmission))
            print('fuel = {}'.format(fuel))
            print('economy = {}'.format(economy))
            print('engine = {}'.format(engine))
            print('Power = {}'.format(Power))
            print('driven = {}'.format(driven))
            print('seats = {}'.format(seats))
            print('-------------------------Prediction----------------------')
            print("Predicted car price is {} Lakh".format(prediction))

        except Exception as e:
            print(e)

    return render_template('index.html', CarPrice = "{} Lakh".format(round(prediction[0], 2)
))

@app.route("/", methods=["GET"])
def home():
    return render_template('index.html')

if __name__ == "__main__":
    print("Server Started...")
    print("To stop the Server press CTRL+C")
    app.run()
