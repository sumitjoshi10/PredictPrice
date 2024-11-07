from flask import Flask, request, jsonify, render_template

from src.pipelines.prediction import Prediction,CustomeData


prediction = Prediction()
app = Flask(__name__)

@app.route("/")
def index():
    return "Hi"

@app.route("/get_location_names")
def get_location_names():
    response = jsonify({
        "location":prediction.get_location()
    })
    response.headers.add("Access-Control-Allow-Origin","*")
    
    return response

@app.route("/predict",methods = ["POST"])
def predict():
    data = CustomeData(
        location=request.form.get("location"),
        total_sqft=request.form.get("total_sqft"),
        bath=request.form.get("bath"),
        bhk=request.form.get("bhk")
    )
    
    data_df = data.get_data_as_data_frame()
    print(data_df)
    
    prediction = Prediction()
    response = jsonify({
        "Estimated Price" : prediction.predict(features=data_df)
    })
    response.headers.add("Access-Control-Allow-Origin","*")
    
    return response
    

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)