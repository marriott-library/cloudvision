#!/bin/bash
# run from your local machine to update the production ezproxy server with the
# latest configuration files from gitlab.lib.utah.edu

# Staging
read -p 'Username: ' uservar
ssh $uservar@staging.lib.utah.edu 'cd /var/www/mlib-theme.staging.lib.utah.edu && git pull'
