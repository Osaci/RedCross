# run environment 
FROM python:3.10-slim-bullseye

# sets working directory 
WORKDIR /app

# install dependencies
RUN apt-get update && apt-get install -y \
    net-tools \
    curl

# copy vertex_chat files to container
COPY . /app

# copy gcloud auth 
COPY ultra-function-439306-r4-3a41fd3b676b.json /app/ultra-function-439306-r4-3a41fd3b676b.json

# certification and key
COPY ssl/cert.pem /etc/ssl/certs/cert.pem
COPY ssl/unencrypted_private.key /etc/ssl/private/unencrypted_private.key

# install modules
RUN pip install --no-cache-dir -r requirements.txt

# ensure certification and key access
RUN chmod 600 /etc/ssl/certs/cert.pem /etc/ssl/private/unencrypted_private.key

# expose port 
EXPOSE 8080

# set gcloud application credentials
ENV GOOGLE_APPLICATION_CREDENTIALS="ultra-function-439306-r4-3a41fd3b676b.json"

# flask app name
ENV FLASK_APP=app.py

# run command 
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app", "--certfile", "/etc/ssl/certs/cert.pem", "--keyfile", "/etc/ssl/private/unencrypted_private.key"]
