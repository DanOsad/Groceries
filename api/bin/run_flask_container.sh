# RUNS FLASK SERVER WITH WAITRESS INSIDE DOCKER CONTAINER

export ENABLE_MONITORING=0
export LOG_DIR=/app/logs

cd /app
waitress-serve --url-prefix=/ --listen=0.0.0.0:5000 app:app