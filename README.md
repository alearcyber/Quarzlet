# Quarzlet

Team 03 - Aidan Lear, Devin Patel, Vish Patel

The Quarzlet cloud application allows users to create their own multiple choice quizzes and take them.

- [Quarzlet](#quarzlet)
  - [Services](#services)
  - [Structure](#structure)
  - [Installation](#installation)
  - [Run](#run)
  - [External Software Used](#external-software-used)
  - [External Services Used](#external-services-used)
  - [Credits](#credits)

## Services

- QuizTake: Entry point for the product. Allows user to select and take a quiz. The quiz gets scored and the results are presented to the user. Allows user to delete quizzes.
- QuizMake: Allows user to create a new quiz and add it to the database in QuizStore.
- QuizStore: Provides interfacing for database queries and communicates with QuizTake and QuizMake via HTTP requests.
- QuizAuth: Authenticates user credentials.

## Structure

Each service runs within separate Docker containers that communicate with each other via HTTP requests.

- QuizTake: Port 8000
- QuizMake: Port 8001
- QuizStore: Port 8002
- QuizAuth: Port 8003

Docker compose is used to start and link all the service containers.

![Quarzlet Service Structure](documentation/Service-Components.png)

## Installation

Initial configuration is needed before the containers can be created.  
Run the following python script in the project's root directory:

`python3 install.py`

## Run

To run the application, run the following:

`docker compose -f "docker-compose.yaml" up -d --build`

To stop the application, run the following:

`docker compose down`

Once the containers are running, you can access the site by typing [http://127.0.0.1:8000](http://127.0.0.1:8000) into your browser.

By default, the username and password will both be "admin" and the database will be loaded with three sample quizzes.

## External Software Used

- [Docker Build v0.11.2](https://www.docker.com/get-started/) - Builds Docker images from Dockerfiles and source
- [Docker Compose v2.23.0](https://docs.docker.com/compose/install/) - Starts and links multiple Docker containers
- [Docker Engine v24.0.7](https://docs.docker.com/engine/install/) - Daemon to run Docker containers
- [Flask v2.3.3](https://pypi.org/project/Flask) - Python Web Framework
- [Python v3.10](https://www.python.org/downloads/) - Programming Language
- [SQLite v0.5.1](https://pypi.org/project/pysqlite3/) - Lightweight Relational Database

## External Services Used

No external services used.

## Credits

- Base CSS provided by [Bootstrap v4.0](https://getbootstrap.com/)
- The sidebar in QuizTake used HTML and CSS inspired from [Bootstrap Examples](https://getbootstrap.com/docs/4.1/examples/) - [Dashboard](https://getbootstrap.com/docs/4.1/examples/dashboard)
