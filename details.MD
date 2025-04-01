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