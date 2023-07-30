cd "$(dirname "$0")"

if [ "${LOCAL_IMAGE_NAME}" == "" ]; then
    LOCAL_TAG=`date +"%Y-%m-%d-%H-%M"`
    export LOCAL_IMAGE_NAME="credit-classification-prediction:${LOCAL_TAG}"
    echo "LOCAL_IMAGE_NAME is not set, building a new image with tag ${LOCAL_IMAGE_NAME}"
    docker build -t ${LOCAL_IMAGE_NAME} ..
else
    echo "no need to build image ${LOCAL_IMAGE_NAME}"
fi

aws s3 mb s3://credit-card-mlops-project

# check whether s3 bucket is created or not
aws s3 ls

export INPUT_FILE_PATTERN="s3://credit-card-mlops-project/in/credit_data.arff"
export OUTPUT_FILE_PATTERN="s3://credit-card-mlops-project/out/predictions.csv"

pipenv run python integration_test.py

# verify input file
aws s3 ls s3://credit-card-mlops-project/in/

# verify output file
aws s3 ls s3://credit-card-mlops-project/out/

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi

docker-compose down
