# pylint: disable=broad-except

import os
import pickle

import pandas as pd
from scipy.io.arff import loadarff
from sklearn.preprocessing import LabelEncoder

# Define your feature names
FEATURE_NAMES = [
    'checking_status',
    'duration',
    'credit_history',
    'purpose',
    'credit_amount',
    'savings_status',
    'employment',
    'installment_commitment',
    'personal_status',
    'other_parties',
    'residence_since',
    'property_magnitude',
    'age',
    'other_payment_plans',
    'housing',
    'existing_credits',
    'job',
    'num_dependents',
    'own_telephone',
    'foreign_worker',
]


def get_input_path():
    """Retrieve the path of the input file."""
    default_input_pattern = '../../data/credit_data.arff'
    input_pattern = os.getenv('INPUT_FILE_PATTERN', default_input_pattern)
    return input_pattern


def get_output_path():
    """Retrieve the path of the output file."""
    default_output_pattern = 's3://credit-card-mlops-project/out/predictions.csv'
    output_pattern = os.getenv('OUTPUT_FILE_PATTERN', default_output_pattern)
    return output_pattern


def load_model(path):
    """Load the Random Forest model from a specified path."""
    try:
        with open(path, 'rb') as f_in:
            objects = pickle.load(f_in)
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        objects = None
    return objects


def save_data(df, filename):
    """Save DataFrame to a specified file."""
    try:
        df.to_csv(filename, compression=None, index=False)
    except Exception as e:
        print(f"Error saving data: {str(e)}")


def predict_model(df):
    with open('random_forest_model.bin', 'rb') as f_in:
        model_objects = pickle.load(f_in)

    # Extract the model and preprocessing objects
    model = model_objects['model']
    label_encoders = model_objects['label_encoders']
    scaler = model_objects['scaler']

    # Preprocess the features using the same label encoders and scaler
    for column, le in label_encoders.items():
        if column in df:
            df[column] = le.transform(df[column])

    # Apply scaling
    df = scaler.transform(df)

    # Make prediction using the model
    preds = model.predict(df)  # Note: We're using the model here, not the dictionary
    return preds


def main():
    """Main function to load data, predict, and save results."""
    input_file = get_input_path()
    output_file = get_output_path()

    model = load_model('random_forest_model.bin')
    if model is None:
        return

    # Load the data file
    try:
        data, _ = loadarff(input_file)
        df = pd.DataFrame(data)
        df = df.applymap(lambda x: x.decode() if isinstance(x, bytes) else x)
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return

    # Perform encoding on categorical features
    le = LabelEncoder()
    for column in df.columns:
        if df[column].dtype == 'object' and column != 'checking_status':
            # Ensure the column does not contain null/missing values
            if df[column].isna().any():
                df[column].fillna(
                    'missing', inplace=True
                )  # replace NaNs with a string like 'missing'

            # Convert everything to string type before encoding
            df[column] = df[column].astype(str)

            # Then perform encoding
            df[column] = le.fit_transform(df[column])

    # Manually map 'checking_status' feature
    df['checking_status'] = df['checking_status'].map(
        {'<0': 0, '0<=X<200': 1, '>=200': 2, 'no checking': 3}
    )

    # Perform prediction
    try:
        X_val = df[FEATURE_NAMES]
        X_val = X_val.reindex(columns=FEATURE_NAMES)
        y_pred = predict_model(X_val)
    except Exception as e:
        print(f"Error predicting data: {str(e)}")
        return

    # Save results
    df_result = pd.DataFrame()
    df_result['predicted_credit_classification'] = y_pred
    save_data(df_result, output_file)


if __name__ == '__main__':
    main()
