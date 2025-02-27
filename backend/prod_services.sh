#!/bin/bash

# Restart Django (via supervisorctl)
echo "Restarting Django..."
sudo supervisorctl restart django

# Restart Nginx
echo "Restarting Nginx..."
sudo systemctl restart nginx

echo "Both Django and Nginx have been restarted successfully."

