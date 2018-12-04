FROM python:3.7-alpine

ENV PROJECT_DIR=/opt/contact-api/ \
    VENV_DIR=/opt/contact-api/.venv \
    SOURCE_DIR=/opt/contact-api/contact_api
ENV FLASK_APP=${SOURCE_DIR}/main.py

# Install sqlite
RUN apk update &&\
    apk add sqlite

# Setup python environment
WORKDIR ${PROJECT_DIR}
COPY ./requirements.txt ${PROJECT_DIR}
RUN python -m venv ${VENV_DIR}
RUN source ${VENV_DIR}/bin/activate
RUN pip install -r ${PROJECT_DIR}/requirements.txt

# Copy source code to image
COPY ./contact_api ${PROJECT_DIR}/contact_api

# Initialize sqlite db
RUN python -c "from contact_api import db; db.init_db()" 

ENTRYPOINT ["flask", "run", "--host", "0.0.0.0"]
