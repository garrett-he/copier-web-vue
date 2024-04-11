ARG NODE_VERSION
FROM node:$NODE_VERSION as builder

WORKDIR /app-build

ADD ./docker ./docker
ADD ./src ./src
ADD index.html .
ADD package* .
ADD tsconfig.json .
ADD vite.config.ts .

RUN npm install
RUN npm run build
RUN npm prune --production

FROM nginx:latest

COPY --from=builder /app-build/dist/ /var/www/html/
COPY --from=builder /app-build/docker/nginx/default.conf /etc/nginx/conf.d/

EXPOSE 80
