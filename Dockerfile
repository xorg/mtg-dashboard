# set base image (host OS)
FROM python:3.8

WORKDIR /app

# install backend
COPY . .
RUN python setup.py install

# install dependencies
RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt

# command to run on container start
CMD [ "flask", "run", "--host=0.0.0.0"]
