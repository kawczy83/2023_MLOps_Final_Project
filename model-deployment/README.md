# Model Deployment


This guide explores two primary ways to deploy a machine learning model:

1. **Offline Mode - Batch Deployment**
2. **Online Mode - Web Service and Streaming Deployment**

## 1. Offline Mode - Batch Deployment

Batch deployment is a strategy employed when predictions are required at fixed intervals, such as daily, hourly, weekly, or monthly. This method utilizes a database containing all our data, and a scoring job that houses our model. The scoring job extracts data from the database and applies the model to generate predictions at the specified interval.

## 2. Online Mode - Web Service and Streaming Deployment

Online deployment ensures that your model is always available to make predictions. There are two main approaches for online model deployment:

* **Web Service Deployment**
* **Streaming Deployment**

### 2a. Web Service Deployment

In web service deployment, the model is hosted within a web service. The application communicates with the backend, which in turn interacts with the web service by sending queries. The web service applies the model to these queries and sends back the results (predictions). This deployment model necessitates that the web service be operational at all times and typically follows a one-to-one relationship pattern.

### 2b. Streaming Deployment

Streaming deployment is ideal for scenarios involving continuous event streams. Model services listen for these events on the stream and output predictions accordingly.

Streaming involves three key components: Event Stream, Producers, and Consumers. The producer generates events, pushes them to an event stream, and the consumer reads from this stream to respond to the events.

Event streams and consumers are typically hosted by online services. Commonly used services include:

* Event Stream : Kafka, AWS Kinesis
* Consumers : AWS Lambda

The streaming deployment model can accommodate one-to-many or many-to-many relationship patterns.

---

For the purpose of this guide, I have deployed a model as a **web service**.

### Repository Structure  

1. `web-service`

This directory contains the application that uses Flask and Docker to make predictions on my dataset. The prediction script is encapsulated within a Flask application and packaged into a Docker container.

2. `web-service-mlflow`

This directory demonstrates the use of MLflow for training and logging the model. The trained model is then deployed to a cloud-based storage service (S3 bucket).

Each directory includes a dedicated README file that provides instructions on how to execute the scripts.
