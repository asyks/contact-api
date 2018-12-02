FROM python:3.7-alpine

ENV PROJECT_DIR=/opt/contact-api/.venv
ENV VENV_DIR=/opt/contact-api/.venv
ENV FLASK_APP=${PROJECT_DIR}/main.py

# Setup python environment
WORKDIR ${PROJECT_DIR}
COPY ./requirements.txt ${PROJECT_DIR}
RUN python -m venv ${VENV_DIR}
RUN source ${VENV_DIR}/bin/activate
RUN pip install -r ${PROJECT_DIR}/requirements.txt

# Copy source code to image
COPY ./main.py ${PROJECT_DIR}

ENTRYPOINT ["flask", "run", "--host", "0.0.0.0"]
