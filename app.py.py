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
        "transaction": transaction_data, "prediction": "fraud" if prediction else "not fraud"
    })

    if prediction:
        send_alert(transaction_data)

    return jsonify({"prediction": "fraud" if prediction else "not fraud"})


def predict_fraud(transaction_data):
    processed_data = preprocess(transaction_data)
    fraud_probability = model.predict_proba(processed_data)[0][1]
    # For example, return True if fraud is detected, False otherwise
    return fraud_probability > 0.5  # Replace with actual model call

def preprocess(transaction_data):
    # Add logic to preprocess transaction data before feeding it to the model
    # Example: return a list of features extracted from transaction_data
    return [
        transaction_data['amount'], 
        transaction_data['transaction_type'], 
        transaction_data['location']
    ]


def send_alert(transaction_data):
    # Send an email or webhook alert when fraud is detected
    if transaction_data["prediction"] == "fraud":
        print('ALERT: Fraudulent transaction detected!', transaction_data)
        return 'Caution: FRAUD'
        





def 
if __name__ == "__main__":
    app.run(debug=True)

