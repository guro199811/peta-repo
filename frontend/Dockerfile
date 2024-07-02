FROM node:21.6.2

# Settingh Working directory
WORKDIR /app


COPY ./frontend/reacting-pet/package*.json .

# installing npm dependencies
RUN npm install

# Copy 
COPY ./frontend/ .

WORKDIR /app/reacting-pet
# Expose the port the app runs on
EXPOSE 5173

# lauching
CMD ["npm", "run", "dev"]