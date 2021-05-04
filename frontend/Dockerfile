FROM node:15
ARG FONTAWESOME_AUTH_TOKEN
WORKDIR /code

COPY package.json ./
COPY yarn.lock ./

# For fontawesome pro. Need to set FONTAWESOME_AUTH_TOKEN build arg
COPY .npmrc ./

RUN yarn install

COPY . .
RUN yarn build
EXPOSE 3000
CMD ["node_modules/nuxt/bin/nuxt.js", "start", "-H", "0.0.0.0"]
