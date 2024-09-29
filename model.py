import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

important_features = [
    'amount', 
    'oldbalanceOrg', 
    'newbalanceOrig', 
    'oldbalanceDest', 
    'newbalanceDest'
]

def load_and_process_data(file_path):
    data = pd.read_csv(file_path)
    
    if 'isFraud' not in data.columns:
        raise ValueError("The dataset must contain an 'isFraud' column.")
    
    X = data[important_features].copy()
    y = data['isFraud']
    X.fillna(X.median(), inplace=True)

    return X, y

def train_fraud_detection_model(data_path):
    X, y = load_and_process_data(data_path)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    model_file = 'fraud_detection_model_optimized.pkl'
    joblib.dump(model, model_file)

    return f"Model trained and saved as {model_file}. Accuracy: {accuracy * 100:.2f}%\n\nReport:\n{report}"

def load_model(model_file):
    model = joblib.load(model_file)
    return model

def predict_fraud_probability(model, features):
    probabilities = model.predict_proba(features)
    return probabilities[0][1]

if __name__ == "__main__":
    data_path = 'sampled_fraud_dataset.csv'
    report = train_fraud_detection_model(data_path)
    print(report)
