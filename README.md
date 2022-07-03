### Prerequisites
Docker

### Installation

1. Install docker on your machine
2. Make sure docker is running
3. Open command line and go to the directory with Dockerfile and docker-compose.yml 
4. Use command: "docker-compose up" to run server 
5. Docker compose includes:
    - setting up Postgresql image with a Postgresql database
    - setting up Python image and installs requirements
    - actions included in Python image:
        - making migrations
        - migrating data
        - loading tag, blog and user fixtures
        - running API tests
        - running server
6. The app will run on address: http://127.0.0.1:8000/

To view API documentation: http://127.0.0.1:8000/api_documentation

User fixtures include a testing superuser account:
   - username: a
   - password: a
