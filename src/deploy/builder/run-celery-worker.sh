#!/bin/bash

# use --detach for daemonize worker

celery worker -A stacks --concurrency=8
