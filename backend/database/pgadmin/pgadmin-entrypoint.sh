#!/bin/sh

# Redirect stdout and stderr to /dev/null to suppress logging
exec > /dev/null 2>&1

# Start pgAdmin
exec /entrypoint.sh "$@"
