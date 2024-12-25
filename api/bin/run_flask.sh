# RUNS FLASK SERVER WITH WAITRESS ON HOST MACHINE

export ENABLE_MONITORING=1
export LOG_DIR=/usr/local/share/simba_server/app/logs
export HOSTNAME=$HOSTNAME

cd /usr/local/share/simba_server/app/
waitress-serve --url-prefix=/ --listen=0.0.0.0:4040 app:app