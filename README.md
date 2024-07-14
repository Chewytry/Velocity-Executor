## Introduction

In today's fast-paced world, effective communication is key to success. The ability to present information in a clear, concise, and engaging manner is imperative. This is where our PowerPoint (PPT) Generator comes into play.

Our project focuses on leveraging cutting-edge technology, specifically the RAG (Retrieval-Augmented Generation) pipeline, to revolutionize the way travel itineraries are created. Gone are the days of manually searching for travel destinations; with our PPT Generator, users can simply input a prompt, and the system will automatically generate a comprehensive deck of slides suggesting countries to travel to and attractions to look out for, summarizing relevant information from our H2O.ai collection.

## How to run our app

1. Building docker images

```
docker-compose build
```


2. To run the application:

```
docker-compose up
```
If an error pops up, open a separate terminal and run the following command:
```
wave run app
```
and go to http://localhost:10101/ 

## Repository Structure
    
├── Docker                  : 2 docker files, one for h2owave, one for flask download service

├── themes                  : contains background images for slides of each theme

├── app.py                  : python script for running the application

├── docker-compose.yml      : docker compose file to compose the flask service and the wave app

├── homepage.py             : python script for designing application's homepage

├── recommendations.py      : python script for designing the recommendations page where users input prompts and powerpoint theme choices 

├── service.py              : flask service running the downloads button the downloads directory of the devies

└── slides_generation.py    : python script regarding the creation of slides and extracting of relevant information from h20 gpt output


