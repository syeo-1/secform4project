### things to keep in mind
#### I'm looking for non-derivative, and non-RSU orders

- in other words, only when people are directly buying and selling shares in a company, I want that information
- the link below is for RSU related acquisition of stock for Jetblue airways
- https://www.sec.gov/Archives/edgar/data/1858380/000115846325000044/0001158463-25-000044-index.htm

- also since I want non-derivative data, need to know how to recognize and not waste space to save it:
- here's an example for softbank
- https://www.sec.gov/Archives/edgar/data/1065521/000149315225009612/0001493152-25-009612-index.htm

- i think i should also focus on non-issuer reports, so only officer level and above people purchasing or selling stock!! (so only reporting ones)

## form 4 codes:

https://www.sec.gov/edgar/searchedgar/ownershipformcodes.html

why's there a huge discrepency with the period of report, and filing/acceptance date for this one:
https://www.sec.gov/Archives/edgar/data/1545565/000110465925023121/0001104659-25-023121-index.htm

## form 4 info regarding the two day delay in filing transactions
https://www.sec.gov/files/forms-3-4-5.pdf


## what if someone buys and sells at the same time?

### so, there are several transactions within the same report, and all of them are non-derivative!

### form 4 details: (section 8 useful for transaction codes)
- https://www.sec.gov/about/forms/form4data.pdf

### multi purchase
https://www.sec.gov/Archives/edgar/data/1878542/000138746725000038/0001387467-25-000038-index.htm

### focus on direct ownership. so this will be D in column 6 table 1
### there can be a mix of things in table 1 (RSU with standard purchase!!)
https://www.sec.gov/Archives/edgar/data/1859449/000161755325000024/0001617553-25-000024-index.htm

### cannot process transaction code V as well for non-derivative transactions:
- https://www.sec.gov/Archives/edgar/data/103379/000112760224011589/xslF345X05/form4.xml
or mayber this one according to chatgpt
- https://www.sec.gov/Archives/edgar/data/320193/000032019324000132/xslF345X05/wk-form4_1734564614.xml
### I think this one actually has the v code marked!
- https://www.sec.gov/Archives/edgar/data/1108524/000112760223018474/xslF345X04/form4.xml

====================================

### docker compose details
- I'll want to try to create a dev/prod environment
- got a recommendation to check out profiles in docker compose based on this reddit thread
- https://www.reddit.com/r/docker/comments/13kxfjf/how_to_handle_dockercompose_for_production_and/
- https://docs.docker.com/compose/how-tos/profiles/

- right now the goal will be to create airflow and postgres within the same docker compose and
set it up so that the volume is within the container itself. When I move to AWS, the goal will be to
set up RDS so that data will instead be saved there

### docker compose and networking for postgres and pgadmin
- https://docs.docker.com/compose/how-tos/networking/
- by default, a network called myapp_default is created when using docker compose files
- so with that in mind, pgadmin should be able to communicate with the database for the data
- be sure to use the container_name field of your postgres instance when connecting to the database from pgadmin
    - this will be the hostname/address field!
- also I had to manually create an empty postgres-db-volume folder to correspond to the volumes parameter within this project directory

### need to be able to handle timezone transaction dates!
eg. it's typically this: 2025-03-31 for example
but sometimes can be something like this: 2025-03-26-05:00, which isn't valid in postgres
- also need to ensure 

### if it's necessary, may need to create a default admin user if airflow won't let you login
- do the following:
    - docker exec -it <docker service id> bash
        - get the id of the airflow webserver service from docker desktop for the service
    - run the following command to set up a default admin user
        - airflow users  create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin
    - should now be able to login with username: admin, password: admin

### how should i be structuring the api endpoints?
- i want to get data for the following from my data (eventually)
- all trades for a particular ticker
- all trades from a specific person
- all trades/tickers from a particular industry
- largest (top 10) movers in a particular industry
- largest movers by company market cap

    - I'll need to create another table with the following information
    - ticker, industry, and company market cap
        - the market cap info would have to be updated daily
        - actually, so would the other two, if new companies get listed

- for each of the routes, I can do things like /ticker/:specific_ticker
    - or, /ticker/sort(?) maybe?

- I can use this as a reference for fastapi backend: https://github.com/polarsource/
    - example of using select statements in sqlalchemy: https://github.com/polarsource/polar/blob/main/server/polar/storefront/service.py

- also an example of creating exceptions in Python: https://github.com/polarsource/polar/blob/main/server/polar/exceptions.py
    - and how to use them: https://github.com/polarsource/polar/blob/main/server/polar/storefront/endpoints.py


# basic front end work!

### what information do I have, and what would I like to be displayed

#### transaction information
- maybe it would be interesting to see an individual's known holdings
    - ie. what stocks do we know they're currently holding onto?
- also, would like to know, what are their overall profit/loss based on 


### to refer to for inspo
- https://www.gurufocus.com/insider/summary

### creating the front end
- I'm gonna try and use Vite for front end development
    - using typescript and bootstrap? or tailwind we'll see... keep things simple tho

### data retrieval set up
- realistically, I should just use AWS lambda and cloudwatch instead of an EC2 instance. Much cheaper, but
would not be using airflow. I'll just say I migrated away for cost saving by like 95%. which is true, since t2small will likely cost like 15 dollars a month, and lambda with cloudwatch may cost like less than a dollar i hope


### TODO: retrieving historical/missing data
- I can actually retrieve all form 4 information!!!
    - would have to scrape using this link and adjust start/end dates, form value, and increment page number
        - https://www.sec.gov/edgar/search/#/dateRange=custom&category=custom&startdt=2025-03-10&enddt=2025-04-09&forms=4&page=100
    - looks like I can only reliably get data one week at a time. No matter what the custom range you give, it seems that you can only retrieve up to 10_000 elements. So if there's more than that, then 

### useeffect
- use useEffect to run re-renders on the UI. Within it, there's a dependency array. Whenever variables are modified/changed for those dependencies, a re-render is triggered. You can also just leave it empty if you don't plan on running any re-renders when certain variables are changing

### slow search results TODO:
- this might be something to keep in mind if the site goes live: https://mui.com/material-ui/react-autocomplete/#search-as-you-type
- if I'm doing requests per keystroke on the search bar, then need to throttle requests somehow

### nice future features
- use react-plotly-js for the bar chart instead, so users can have pan and zoom for the charts (only material ui pro has that feature)
- top activity for homepage (ie. most transactions in a given timeframe)

### trying to copy the bloomberg terminal color scheme and styles