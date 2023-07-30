# Machine Learning Model Deployment

This section outlines the process of deploying the model to an AWS S3 bucket (Cloud).

**Note:** This guide assumes the use of an  terminal. A Pipfile is provided in case you encounter environment issues. To create a virtual environment using the Pipfile, run the command: `pipenv install`

For more details on creating a virtual environment using a Pipfile, refer to this [StackOverflow post](https://stackoverflow.com/questions/52171593/how-to-install-dependencies-from-a-copied-pipfile-inside-a-virtual-environment).

Prior to running any commands, **please create an S3 bucket in your AWS account**. The scripts will deploy the model to this bucket.

To access AWS services via the CLI, configure your AWS credentials by running the command: `aws configure` in the terminal. 

When prompted, enter your:

1. AWS Access Key ID
2. AWS Secret Access Key
3. Default region name
4. Default output format

Ensure you enter these credentials before running the scripts.

## Steps to Execute the Script

1. Open three terminal windows: Terminal 1, Terminal 2, and Terminal 3. In all terminals, navigate to the `web-service-mlflow` directory and activate the virtual environment (which should include the libraries specified in the Pipfile). Activate the virtual environment by running the following command in the terminal:
    ```
    pipenv shell
    ```

2. In Terminal 1, type the following command, replacing `{bucket-name}` with the name of the bucket you created in your AWS account:
    ```
    mlflow server --backend-store-uri=sqlite:///mlflow.db --default-artifact-root=s3://{bucket-name}/
    ```
    **Note:** Keep the server running in Terminal 1 and switch to Terminal 2 for the subsequent steps.

3. After executing the command in step 2, run all the cells in `random-forest-mlflow.ipynb`. This will train the model, log it in MLflow, and store it in the S3 bucket you created.

4. In this step, you need to retrieve the RUN_ID of the model that was logged to your S3 bucket. Access your AWS account, open S3 (buckets), and find the RUN_ID at: `Amazon S3 > Buckets > {your-bucket-name} > 1/ > {RUN_ID}`.

5. Open Terminal 2, and export the RUN_ID you obtained from step 4 by running the following command:
    ```
    export RUN_ID="run-id"
    ```
    Replace "run-id" with your actual RUN_ID.

6. Before running `predict.py`, update line 9 with the name of your S3 bucket. For example, if your bucket is named "mlops-zoomcamp-project", line 9 should look like this:
    ```
    logged_model = f's3://mlops-zoomcamp-project/1/{RUN_ID}/artifacts/model'
    ```

7. Now in Terminal 2, after exporting the RUN_ID and updating the bucket name in `predict.py`, execute the following command:
    ```
    python predict.py
    ```
    This command will start the server, which waits for incoming data. **Note:** Keep the server running in Terminal 2 and switch to Terminal 3 for the subsequent steps.

8. Open Terminal 3, and execute the following command:
    ```
    python test.py
    ```
    This command will send numerical features (credit_amount, age, duration, checking_status) to the server, print the model version trained and logged in MLflow and your S3 bucket, and display the predicted credit card classification based on the features sent. You can modify the numerical features in `test.py` as desired.

**Note:** If you encounter a "connection in use" error while running MLflow, execute the following command in the terminal:
    ```
    pkill gunicorn
    ```

You can view the logged model in MLflow (http://127.0.0.1:5000) as well as in the S3 bucket you created.
