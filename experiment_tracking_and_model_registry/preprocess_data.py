import os
import pickle
import click
import pandas as pd
from scipy.io.arff import loadarff 
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer


def dump_pickle(obj, filename: str):
    with open(filename, "wb") as f_out:
        return pickle.dump(obj, f_out)


def read_dataframe(filename: str):
    raw_data = loadarff(filename)

    df = pd.DataFrame(raw_data[0])
    df = df.applymap(lambda x: x.decode() if isinstance(x, bytes) else x)

    categorical = ['checking_status', 'credit_history', 'purpose', 'savings_status', 
                   'employment', 'personal_status', 'other_parties', 'property_magnitude', 
                   'other_payment_plans', 'housing', 'job', 'own_telephone', 'foreign_worker']
    df[categorical] = df[categorical].astype(str)

    return df


def preprocess(df: pd.DataFrame, dv: DictVectorizer, fit_dv: bool = False):
    categorical = ['checking_status', 'credit_history', 'purpose', 'savings_status', 
                   'employment', 'personal_status', 'other_parties', 'property_magnitude', 
                   'other_payment_plans', 'housing', 'job', 'own_telephone', 'foreign_worker']
    numerical = ['duration', 'credit_amount', 'installment_commitment', 'residence_since', 
                 'age', 'existing_credits', 'num_dependents']
    dicts = df[categorical + numerical].to_dict(orient='records')
    if fit_dv:
        X = dv.fit_transform(dicts)
    else:
        X = dv.transform(dicts)
    return X, dv


@click.command()
@click.option(
    "--raw_data_path",
    default="./data",
    help="Location where the raw credit risk data was saved"
)
@click.option(
    "--dest_path",
    default="./output",
    help="Location where the resulting files will be saved"
)
def run_data_prep(raw_data_path: str, dest_path: str):
    # Load arff file
    df = read_dataframe(
        os.path.join(raw_data_path, "credit_data.arff")
    )

    # Extract the target
    target = 'class'
    y = df[target].values

    # Split data into train, validation, and test sets
    df_train, df_test, y_train, y_test = train_test_split(df, y, test_size=0.2, random_state=42)
    df_train, df_val, y_train, y_val = train_test_split(df_train, y_train, test_size=0.25, random_state=42)

    # Fit the DictVectorizer and preprocess data
    dv = DictVectorizer()
    X_train, dv = preprocess(df_train, dv, fit_dv=True)
    X_val, _ = preprocess(df_val, dv, fit_dv=False)
    X_test, _ = preprocess(df_test, dv, fit_dv=False)

    # Create dest_path folder unless it already exists
    os.makedirs(dest_path, exist_ok=True)

    # Save DictVectorizer and datasets
    dump_pickle(dv, os.path.join(dest_path, "dv.pkl"))
    dump_pickle((X_train, y_train), os.path.join(dest_path, "train.pkl"))
    dump_pickle((X_val, y_val), os.path.join(dest_path, "val.pkl"))
    dump_pickle((X_test, y_test), os.path.join(dest_path, "test.pkl"))


if __name__ == '__main__':
    run_data_prep()
