FROM node:10
WORKDIR /usr/src/app

# NOTE: install app dependency
COPY package*.json ./

RUN npm install
# RUN npm ci --only=production

# NOTE: add app sources
COPY . .

EXPOSE 8080
CMD ["node", "server.js"]
