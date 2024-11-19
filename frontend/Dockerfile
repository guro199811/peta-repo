FROM node:21.6.2-alpine

# Setting Working directory
WORKDIR /app


COPY ./frontend/reacting-pet/package*.json ./

# installing npm dependencies
RUN npm install

# Copy 
COPY ./frontend/ .

WORKDIR /app/reacting-pet
# Expose the port the app runs on
EXPOSE 3000

# lauching
CMD ["npm", "run", "dev", "--turbopack"]