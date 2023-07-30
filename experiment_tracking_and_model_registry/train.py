import os
import pickle
import click
import mlflow
import mlflow.sklearn

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

os.environ["AWS_PROFILE"] = "default"
os.environ["AWS_DEFAULT_REGION"] = 'us-east-1'

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("test")


def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


@click.command()
@click.option(
    "--data_path",
    default="./output",
    help="Location where the raw credit risk data was saved"
)
def run_train(data_path: str):

    mlflow.sklearn.autolog()

    with mlflow.start_run():
        print(mlflow.get_artifact_uri()) 
        print(mlflow.get_tracking_uri())
        X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
        X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))

        rf = RandomForestClassifier(max_depth=10, random_state=0)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_val)

        accuracy = accuracy_score(y_val, y_pred)
        
        mlflow.log_metric("accuracy", accuracy)

if __name__ == '__main__':
    run_train()