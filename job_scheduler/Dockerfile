FROM python:3.9

WORKDIR /app

# service account credentails (should be set as a k8s secret)
COPY serene-radius-314018-c5074800c846.json /app
ENV GOOGLE_APPLICATION_CREDENTIALS=serene-radius-314018-c5074800c846.json

# Downloading gcloud package
RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz

# Installing the package
RUN mkdir -p /usr/local/gcloud \
  && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz \
  && /usr/local/gcloud/google-cloud-sdk/install.sh

# Adding the package path to local
ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin
RUN gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS

# install dependencies
COPY requirements.txt /app
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY . /app

# command to run on container start
CMD [ "python", "app.py" ]
