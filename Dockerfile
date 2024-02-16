# Pull nginx base image
FROM nginx

# Expost port 80
EXPOSE 80

# Copy custom configuration file from the current directory
COPY nginx.conf /etc/nginx/nginx.conf

# Copy static assets into var/www
COPY ./dist /var/www
COPY ./node_modules /var/www/node_modules

# Start up nginx server
CMD ["nginx"]