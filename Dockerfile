FROM python:3.7-alpine

ENV PROJECT_DIR=/opt/contact-api/ \
    VENV_DIR=/opt/contact-api/.venv \
    SOURCE_DIR=/opt/contact-api/contact_api
ENV FLASK_APP=${SOURCE_DIR}/main.py \
    FLASK_DEBUG=1

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
COPY ./contact_api ${SOURCE_DIR}

ENTRYPOINT ["flask", "run", "--host", "0.0.0.0"]
