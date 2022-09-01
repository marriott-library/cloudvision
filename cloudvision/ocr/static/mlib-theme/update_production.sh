#!/bin/bash
# run from your local machine to update the production ezproxy server with the
# latest configuration files from gitlab.lib.utah.edu

# Production
read -p 'Username: ' uservar
ssh $uservar@brussels.lib.utah.edu 'cd /var/www/mlib-theme.lib.utah.edu && git pull'
