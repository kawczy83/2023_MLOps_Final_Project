import math

import pandas as pd
from sklearn.preprocessing import LabelEncoder

import batch


def test_predict():
    credit_classification = {
        'checking_status': '<0',
        'duration': 6.0,
        'credit_history': 'existing paid',
        'purpose': 'radio/tv',
        'credit_amount': 4000.0,
        'savings_status': '<100',
        'employment': '1<=X<4',
        'installment_commitment': 4.0,
        'personal_status': 'male single',
        'other_parties': 'none',
        'residence_since': 1.0,
        'property_magnitude': 'real estate',
        'age': 30.0,
        'other_payment_plans': 'none',
        'housing': 'own',
        'existing_credits': 0.0,
        'job': 'skilled',
        'num_dependents': 1.0,
        'own_telephone': 'yes',
        'foreign_worker': 'yes',
    }

    # Convert dictionary to DataFrame
    df = pd.DataFrame([credit_classification])

    # Here, encode 'checking_status' the same way as in your training script.
    df['checking_status'] = df['checking_status'].map(
        {'<0': 0, '0<=X<200': 1, '>=200': 2, 'no checking': 3}
    )

    # Encode 'credit_history' and other categorical features
    le = LabelEncoder()
    categorical_features = [
        'credit_history',
        'purpose',
        'savings_status',
        'employment',
        'personal_status',
        'other_parties',
        'property_magnitude',
        'other_payment_plans',
        'housing',
        'job',
        'own_telephone',
        'foreign_worker',
    ]

    for feature in categorical_features:
        df[feature] = le.fit_transform(df[feature])

    actual_prediction = math.floor(batch.predict_model(df))

    expected_prediction = 0

    assert actual_prediction == expected_prediction
