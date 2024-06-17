FROM node:21.6.2

# Settingh Working directory
WORKDIR /app

RUN ls
# Copy 
COPY ./frontend/reacting-pet/ .

# installing npm dependencies
RUN npm install


# lauching
CMD ["npm", "start"]