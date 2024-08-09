# Insta Blast DM

### Overview
This project is a Python application that uses SQLite for database management. Ensure your machine have chromedriver for selenium to drive it. It includes a Docker setup for containerized deployment.

### Prerequisites
Before you begin, ensure you have the following installed:

- Python (version 3.10 or higher)
- Docker
- Selenium (need chromedriver) if using docker you can using selenium/standalone-chrome. Chck out the docker-compose.yml!
- Conda (optional)

### Setup Instructions

#### Clone repository
```bash 
git clone https://github.com/bagusgandhi/insta-blast-dm.git

cd your-repository
```

<!-- sqlite3 your_database_file.db -->


<!-- CREATE TABLE profiles (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    link TEXT UNIQUE NOT NULL,
    delivered BOOLEAN DEFAULT FALSE
); -->

#### Setup python env with conda (optional)
``` bash
conda env create -f environment.yml

conda activate hentek
```

#### Install requirements
``` bash 
pip install -r requirements.txt
```

#### setup sqlite database
you need setup sqlite on your machine first, after that follow this

``` bash
# create sqlite database
sqlite3 your_database_file.db

# on cli sqlite create table like this
sqlite> CREATE TABLE profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_link TEXT UNIQUE,
    delivered BOOLEAN DEFAULT FALSE
);
```

#### Setup env
``` bash
nano .env

# add this
# IMAGE_PATH= # your image path
# SELENIUM_HOST= # http://localhost:4444/wd/hub selenium host
# MESSAGE_COUNT= # 10
# USERNAME= #your username instagram
# PASSWORD= # your password instagram
# DB= # your_database.db

```

#### Selenium Standalone setup
``` bash 
docker compose up -d --build selenium
```

#### Run Script
``` bash
# for login, you need run this for first time
pyhton login.py

# after login then blast
pyhton main.py

# need scheduling?
pyhton scheduler.py
```

#### Deployment
``` bash 
docker compose up -d --build
```



