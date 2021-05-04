FROM node:15
WORKDIR /code

COPY package.json ./
COPY yarn.lock ./

# For fontawesome pro. Need to set FONTAWESOME_AUTH_TOKEN env variable
COPY .npmrc ./

RUN yarn install

COPY . .
RUN yarn build
EXPOSE 3000
CMD ["yarn", "start", "-H", "0.0.0.0"]
