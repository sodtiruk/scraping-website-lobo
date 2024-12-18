
# Setup for develop

python -m venv env

env\Scripts\activate

pip install -r requirements.txt

# Run Script
python main.py

# Docker
docker-compose up --build

***
If you use Docker, you can run a single command, and it will automatically create the database for you. Then, you can access the database directly through PhpMyAdmin.
-> http://localhost:5001/
username: root
password: password
database: db
table: lobo
you can manual in docker-compose

