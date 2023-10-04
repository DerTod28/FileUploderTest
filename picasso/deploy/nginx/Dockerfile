FROM nginx:stable-alpine3.17-slim

RUN chmod 777 /etc/nginx/conf.d/default.conf && rm /etc/nginx/conf.d/default.conf
COPY picasso/deploy/nginx/nginx.conf /etc/nginx/conf.d/default.conf
