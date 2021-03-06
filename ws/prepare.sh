#!/bin/bash
# on launch
sudo amazon-linux-extras install python3
sudo yum install python-devel postgresql-devel
sudo yum install postgresql
sudo mkdir -p /var/www/ws
sudo chown ec2-user: /var/www/ws
python3 -m venv /var/www/ws/venv
source /var/www/ws/venv/bin/activate
pip install --upgrade pip
pip install flask-restplus
pip install Flask-Migrate
pip install Flask-Script
pip install --upgrade Werkzeug==0.16.1
pip install psycopg2-binary
pip install boto3
pip freeze > /var/www/ws/requirements.txt

export DATABASE_URL=postgresql://postgres:p0stgr3s@pgdb.cbazdk8j8ucl.eu-west-1.rds.amazonaws.com:5432/postgres
export ENV=prod

# after venv initiated
python3 /var/www/ws/manage.py db init
python3 /var/www/ws/manage.py db migrate --message 'initial database migration'
python3 /var/www/ws/manage.py db upgrade

# run application
python3 /var/www/ws/manage.py run
