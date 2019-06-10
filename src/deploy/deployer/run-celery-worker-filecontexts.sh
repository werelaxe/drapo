#!/bin/bash

# use --detach for daemonize worker

celery worker -A filecontexts --concurrency=2

