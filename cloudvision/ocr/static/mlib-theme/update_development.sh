#!/bin/bash
# run from your local machine to update the production ezproxy server with the
# latest configuration files from gitlab.lib.utah.edu

# Development
read -p 'Username: ' uservar
ssh $uservar@development.lib.utah.edu 'cd /var/www/mlib-theme.development.lib.utah.edu && git pull'
