# SECFORM4 Project

This project is dedicated to tracking insider trading activity using SEC form 4 filing information.

The project has been built using the following list of technologies

- Python (FastAPI, Airflow, requests, Beautifulsoup, Pytest)
- React (Material UI, Typescript, Plotly)
- PostgreSQL
- AWS
    - no server-side rendering, so vite will use Cloudfront + S3
    - RDS will be used for postgres database
    - likely API gateway will be used for FastAPI
        - checking if instead AWS elastic beanstalk can be used
        - I want my API to be secure, so only my front end can access the database/api
    - likely EC2 will be used for data pipeline
        - see if can use AWS lambda + event bridge (cron trigger) for cheaper option
- various other technologies (SQLAlchemy, XML, JSON, Swagger, Docker)
- devops: see if I can incorporate deploy on push to AWS with github actions

## Technical challenges
- redoing the chart components to save money so that I can get better performance using plotly graphs
    - improves rendering time/performance plus I get features like pan and zoom for free!
    - material ui charges a premium fee for that, which I didn't want to pay for

## What I've learned
- front end development with React, Typescript, MUI, Plotly
- public cloud services
- systems design
- modern devops tooling (github actions)
- testing frameworks
- data pipeline development on windows (running apache airflow using Docker)
- batch processes on windows
    - adhoc scripts to gather data on a schedule on windows machines
- multithreading requests in python
    - although SEC throttles requests to be at most 10 requests per second, can try to maximize parallelism with multiprocessing in python

## Features to be developed
- sector overview
- alert system
    - Ideally, a site visitor can input their email and be notified when a specific company is being traded by an insider, or an insider is buying/selling
- refactor
    - better logging, failure detection, exception handling
    - be sure there's no issues with front end
        - are there memory leaks?


