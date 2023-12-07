# Loggr App

Loggr is a low-interaction generic log-based social media, in which all user posts are ‘logs’. Logs are effectively loosely structured text data. Each log is part of a loose list of logs, a “Grove”. Users can make Groves for anything from their reviews of movies they’ve seen to hikes they’ve been on. Users can see, like, comment, and save logs from other user’s Groves, but only those that are manually made public and set to a predefined category. People can share their lists, but lists are private by default, ensuring that Loggr stands apart from traditional social media by prioritizing privacy and discrete social interaction. Paid “Enterprise” users can access deeper analytics about what people are up to, but not too much.

This repository contains the database and REST API that power our app.
The repository for the app itself can be found here: https://github.com/jktjia/CS3200-appsmith

# MySQL + Flask Boilerplate Project

This repo contains a boilerplate setup for spinning up 3 Docker containers: 
1. A MySQL 8 container for obvious reasons
1. A Python Flask container to implement a REST API
1. A Local AppSmith Server

## How to setup and start the containers
**Important** - you need Docker Desktop installed

1. Clone this repository.  
1. Create a file named `db_root_password.txt` in the `secrets/` folder and put inside of it the root password for MySQL. 
1. Create a file named `db_password.txt` in the `secrets/` folder and put inside of it the password you want to use for the a non-root user named webapp. 
1. In a terminal or command prompt, navigate to the folder with the `docker-compose.yml` file.  
1. Build the images with `docker compose build`
1. Start the containers with `docker compose up`.  To run in detached mode, run `docker compose up -d`. 




