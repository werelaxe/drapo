#!/bin/bash

# use --detach for daemonize worker

celery worker -A task_instances --concurrency=2

