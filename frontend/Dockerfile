FROM node:21.6.2-alpine

# Setting Working directory
WORKDIR /app

# Copy 
COPY ./frontend/ .

WORKDIR /app/reacting-pet
# Expose the port the app runs on
EXPOSE 3000

# installing npm dependencies
RUN npm install
# RUN npm run build-scss

# lauching
CMD ["npm", "run", "dev", "--turbo"]