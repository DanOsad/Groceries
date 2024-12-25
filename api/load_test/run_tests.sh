#!/bin/bash

locust --config locust.conf
./send_results.py