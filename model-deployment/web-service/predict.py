import pickle

from flask import Flask, request, jsonify

with open('dv.pkl', 'rb') as f_in:
    dv = pickle.load(f_in)

with open('log_reg.pkl', 'rb') as f_in:
    model = pickle.load(f_in)


def prepare_features(credit_card):
    features = {}
    (features['credit_amount'], features['age'], features['checking_status'], features['duration']) = (credit_card['credit_amount'], credit_card['age'], credit_card['checking_status'], credit_card['duration'])
    return features


def predict(features):
    X = dv.transform(features)
    preds = model.predict(X)
    labels = {0: 'good', 1: 'bad'}

    return labels[int(preds[0])]


app = Flask('classification-prediction')


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    credit_card = request.get_json()

    features = prepare_features(credit_card)
    pred = predict(features)

    result = {
        'class': pred
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)