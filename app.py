from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from your_model import predict_fraud

app = Flask(__name__)
app.config["MONGO_URI"] = "insert: my mongo url"
mongo = PyMongo(app)


@app.route('/predict', methods=['POST'])
def predict():
    transaction_data = request.json

    #log transaction data
    mongo.db.transactions.insert_one(transaction_data)

    #call AI model here
    prediction = predict_fraud(transaction_data)

    #Log prediction results
    mongo.db.predictions.insert_one({
        "transaction": transaction_data, "prediction": prediction
    })

    return jsonify({"prediction": prediction})


def predict_fraud(transaction_data):
    # Implement your model logic here
    # For example, return True if fraud is detected, False otherwise
    return model.predict(transaction_data)  # Replace with actual model call




def 
if __name__ == "__main__":
    app.run(debug=True)

