import os

import mlflow
from flask import Flask, request, jsonify

RUN_ID = os.getenv('RUN_ID')
MLFLOW_TRACKING_URI = 'http://127.0.0.1:5000'

logged_model = f's3://credit-card-mlops-orchestration/2/{RUN_ID}/artifacts/model'
model = mlflow.pyfunc.load_model(logged_model)


def prepare_features(credit_card):
    features = {}
    (features['credit_amount'], features['age'], features['installment_commitment'], features['duration'], features['residence_since'], features['existing_credits'],
     features['num_dependents']) = (credit_card['credit_amount'], credit_card['age'], credit_card['installment_commitment'], credit_card['duration'],
                                    credit_card['residence_since'], credit_card['existing_credits'], credit_card['num_dependents'])
    return features


def predict(features):
    preds = model.predict(features)
    return float(preds[0])


app = Flask('classification-prediction')


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    credit_card = request.get_json()

    features = prepare_features(credit_card)
    pred = predict(features)

    result = {
        'class': pred,
        'model_version': RUN_ID
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)