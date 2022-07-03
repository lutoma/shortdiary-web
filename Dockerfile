FROM node:18
ARG FONTAWESOME_AUTH_TOKEN

WORKDIR /app
COPY package.json ./
COPY yarn.lock ./
COPY .npmrc ./

RUN yarn install
COPY . .
RUN yarn build

FROM caddy:2-alpine
LABEL org.opencontainers.image.title="Shortdiary (web)"
LABEL org.opencontainers.image.description="A snazzy diary with client-side encryption"
LABEL org.opencontainers.image.url=https://shortdiary.com
COPY Caddyfile /etc/caddy/Caddyfile
COPY --from=0 /app/dist /srv
EXPOSE 80
