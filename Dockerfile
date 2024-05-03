FROM python:3.6

# Creating Application Source Code Directory
RUN mkdir /app

# Setting Home Directory for containers
WORKDIR /app

# Copy src files folder (requirements.txt and classify.py)
COPY . /app/

# Installing python dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Create directories for models and data
RUN mkdir /app/models
RUN mkdir /app/data

# Preload the data
RUN python data_preload.py

ENV APP_ENV development

RUN DATASET=mnist TYPE=ff python train.py
RUN DATASET=kmnist TYPE=ff python train.py
RUN DATASET=mnist TYPE=cnn python train.py
RUN DATASET=kmnist TYPE=cnn python train.py
# Pretrain the models
# Assuming the code in train.py handles training based on the DATASET and TYPE environment variables.

# Application Environment variables. 
# These variables will be used when you run the image. 
# You will also need to pass corresponding DATASET and TYPE variables from the job yaml files of both free-service and default types of jobs.

# Exposing Ports
EXPOSE 5035

# Setting Persistent data
VOLUME ["/app-data"]
ENV DATASET mnist
ENV TYPE ff
# Running Python Application (classify.py)
CMD ["python", "classify.py"]

