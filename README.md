# contact-api
Python Take-Home Assignment: Contact API for Urban Airship Web Team

## Running the app

### With Docker and Docker Compose
To build and run
```docker-compose up```

To build only
```docker-compose build --force-rm```

### With Docker only
Build the container
```docker build -t contact-api .```

Run the container
```docker run -p 127.0.0.1:5000:5000 -it contact-api```
