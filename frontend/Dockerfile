FROM node:15
WORKDIR /code

COPY ./package.json ./
COPY ./yarn.lock ./

# Needed for fontawesome pro, but not part of git repo
COPY .npmrc ./

RUN yarn install

COPY . .
RUN yarn build
EXPOSE 3000
CMD ["yarn", "start", "-H", "0.0.0.0"]
