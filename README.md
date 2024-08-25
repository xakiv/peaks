
Dear hiker, this is the result of a technical assessment.  
The main task is to deliver a small FastAPI application,  
that handles CRUD operations on geospatial data.  
The application is dockerized   
and tests are available for a coverage score greater than 90%  

# Getting started  

### Prerequisites

- Make sure that you have [Docker](https://www.docker.com/get-started) and [Docker Compose](https://github.com/docker/compose) installed.
- Also [git](https://github.com/git-guides/install-git) should be installed to retrieve the app sources.


```commandline

git pull https://github.com/xakiv/peaks peaks
cd peaks

# Secrets are stored in a `.env` file that you need to create and keep out of the vcs repo
cp envsample .env

docker-compose up --build
```

# API documentation
The APIs services are described and available at [this endpoint](http://127.0.0.1:8000/docs)  
when docker services are running
```commandline
docker-compose up -d
```


# Tests and coverage  

Run tests when docker services are running  
```commandline
docker-compose up -d

docker exec -it peaks-container-1 bash -c "coverage run --module pytest -v && coverage report --show-missing"
```
