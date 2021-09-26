# set base image (host OS)
FROM node

WORKDIR /frontend

# copy the dependencies file to the working directory
COPY package.json .

# install dependencies
RUN npm install

# copy the content of the local src directory to the working directory
COPY .  .

# command to run on container start
CMD [ "npm", "run", "dev"]
