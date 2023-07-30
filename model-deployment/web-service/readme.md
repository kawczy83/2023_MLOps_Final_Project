# Machine Learning Model Deployment

This section focuses on deploying a machine learning model as a web service using Flask and Docker. The deployment process is containerized for easier management and portability. 

For more information on setting up a virtual environment using a Pipfile, refer to this [StackOverflow post](https://stackoverflow.com/questions/52171593/how-to-install-dependencies-from-a-copied-pipfile-inside-a-virtual-environment).

## Running the Model Deployment Script using Flask

Follow these steps to execute the script via Flask:

1. Open two terminal windows (Terminal 1 and Terminal 2). In both terminals, navigate to the `web-service` directory and activate the virtual environment (which should include the libraries specified in the Pipfile) by running the command: 
    ```
    pipenv shell
    ```
2. In Terminal 1, start the server by executing the following command:
    ```
    python predict.py
    ```
    **Note:** Keep the server running in Terminal 1 and switch to Terminal 2 to execute the test script.

3. In Terminal 2, execute the following command:
    ```
    python test.py
    ```
    This will send numerical features (credit_amount, age, duration, checking_status) to the server, and the server will respond with a predicted credit card classification based on the features. You can modify the numerical features in `test.py` as desired.

## Running the Model Deployment Script using Docker

Follow these steps to execute the script via Docker:

1. If any web services are running in Terminal 1, stop them. For Windows, you can do this using CTRL + C.

2. In Terminal 1, build a Docker image named "credit-card-prediction" from the Dockerfile by running the following command:
    ```
    docker build -t credit-card-prediction:v1 .
    ```
    **Note:** Do not forget to include the "." at the end of the command.

3. Once the image is built, start the gunicorn server by running the following command in Terminal 1:
    ```
    docker run -it --rm -p 9696:9696 credit-card-prediction:v1
    ```
    **Note:** Keep the server running in Terminal 1 and switch to Terminal 2 to execute the test script.

4. To receive a response from the server, execute the following command in Terminal 2:
    ```
    python test.py
    ```
    This will send numerical features (credit_amount, age, duration, checking_status) to the server, and the server will respond with a predicted credit card classification based on the features. You can modify the numerical features in `test.py` as desired.
