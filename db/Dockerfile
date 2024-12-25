# Use the official MariaDB image from the Docker Hub
FROM mariadb:latest

# Set environment variables for MariaDB
ENV MYSQL_ROOT_PASSWORD=rootpassword
ENV MYSQL_DATABASE=grocery_system

# Copy the init.sql file into the Docker container's /docker-entrypoint-initdb.d/ directory
# This will automatically execute the script when the container starts
COPY init.sql /docker-entrypoint-initdb.d/

# Expose the default MariaDB port
EXPOSE 3306
