import os

import pandas as pd


def write_to_csv(df, file_path):
    # Write the DataFrame to a CSV file
    df.to_csv(file_path, index=False)


def test_batch_prediction():
    # Define your test input data
    data = [
        {
            'checking_status': '<0',
            'duration': 6,
            'credit_history': 'critical/other existing credit',
            'purpose': 'radio/tv',
            'credit_amount': 1169,
            'savings_status': 'unknown/ no savings account',
            'employment': '>=7',
            'installment_commitment': 4,
            'personal_status': 'male single',
            'other_parties': 'none',
            'residence_since': 4,
            'property_magnitude': 'real estate',
            'age': 67,
            'other_payment_plans': 'none',
            'housing': 'own',
            'existing_credits': 2,
            'job': 'skilled',
            'num_dependents': 1,
            'own_telephone': 'yes',
            'foreign_worker': 'yes',
        },
        # Add more rows as necessary
    ]
    df_input = pd.DataFrame(data)

    # Define your file paths
    input_file_path = "s3://credit-card-mlops-project/in/credit_data.arff"
    output_file_path = "s3://credit-card-mlops-project/out/predictions.csv"

    # Write the DataFrame to the input file
    write_to_csv(df_input, input_file_path)

    # Run the batch prediction script
    os.system(f"cd .. && pipenv run python3 batch.py")

    # Read the output file
    df_output = pd.read_csv(output_file_path)
    print("printing predictions.csv....")
    print(df_output)


if __name__ == "__main__":
    test_batch_prediction()
