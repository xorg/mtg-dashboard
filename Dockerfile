# set base image (host OS)
FROM python:3.8

WORKDIR /app

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# install backend
COPY . .
RUN python setup.py install

# command to run on container start
CMD [ "flask", "run", "--host=0.0.0.0"]
