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

## Endpoints

###Create Contact
To create a contact record send a POST request with json body to /contact/create
supported fields: "email", "name", "company"

###Get one Contact
To get a single contact by id send a GET request with json body to /contact
supported fields: "id"

###Get multiple Contacts
To get a list of contacts send a GET request with or without a json body to /contacts
supported fields: "email", "name", "company"

###Update Contact
To update an existing contact send a PUT request with json body to /contact/update
supported fields: "email", "name", "company"

###Delete Contact
To delete a contact send a DELETE request with json body to /contact/delete
supported fields: "id"
