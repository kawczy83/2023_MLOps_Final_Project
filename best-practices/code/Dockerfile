FROM python:latest

RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app

COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN pipenv install --system --deploy

COPY [ "batch.py", "batch.py" ]
COPY [ "random_forest_model.bin", "random_forest_model.bin" ]

ENTRYPOINT [ "python3", "batch.py" ]
