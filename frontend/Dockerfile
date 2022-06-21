FROM node:18

WORKDIR /app
COPY package.json ./
COPY yarn.lock ./
COPY .npmrc ./

RUN yarn install
COPY . .
RUN yarn build

FROM caddy:2-alpine
COPY Caddyfile /etc/caddy/Caddyfile
COPY --from=0 /app/dist /srv
EXPOSE 80
