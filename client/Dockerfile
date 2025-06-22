# Use an official Node runtime as a parent image
FROM node:18

RUN apt-get update && apt-get upgrade -y

# Set the working directory to /client
WORKDIR /client

# Copy the package.json and package-lock.json to the working directory
COPY ./package*.json ./

# Install the dependencies
RUN npm install -g pnpm \
    && pnpm install

# Copy the remaining application files to the working directory
COPY . .

# Build the application
RUN pnpm build

# Expose port 3000 for the application
EXPOSE 3010

WORKDIR /client

# Start the application
CMD [ "pnpm", "start" ]
