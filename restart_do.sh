#!/bin/bash

systemctl restart nginx
echo "restarted nginx"
systemctl restart gunicorn
echo "restarted gunicorn"
systemctl daemon-reload
echo "restarted daemon"