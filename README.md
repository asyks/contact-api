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

```docker run --env-file=vars.env -p 127.0.0.1:5000:5000 -it contact-api```

## Endpoints

### Create Contact
To create a contact record send a POST request with json body to `/contact/create`.

required json fields: "email"

supported json fields: "email", "name", "company"

### Get one Contact
To get a single contact by id send a GET request with json body to `/contact`.

required json fields: "id"

### Get multiple Contacts
To get a list of contacts send a GET request with or without a json body to `/contacts`.
Supplying a json body will make the app attempt to filter contact records by the
provided fields.

supported json fields: "email", "name", "company", "active"

### Update Contact
To update an existing contact send a PUT request with json body to `/contact/update`.

required json fields: "id"

supported json fields: "email", "name", "company"

### Delete Contact
To delete a contact send a DELETE request with json body to `/contact/delete`.

required json fields: "id"

## Test script

As I was working on the project I wrote a test script `test.sh` for curl-ing
the endpoints with different data/headers/methods. I tried to add curls for all
the required functionality, as well as several error responses.

## Basic Auth

I stuck to having a single set of creds. To change the creds set the env vars:
USERNAME and PASSWORD. The default creds are stored in `vars.env`. I adapted my
basic auth solution from [this flask snippet](http://flask.pocoo.org/snippets/8/).

## Data

I decided to go with a sqlite in-memory database, as it seemed to be an easy
and reliable way to create a persistent (between app restarts) datastore that does
not write to the filesystem. I stuck with a single model/table for Contact, and
a super minimal number of fields: id, name, company, email, active, updated_by.
The primary key is id, and email is the only required field. The active field
stores a contact record's "delete" status, when deleted a contact is changed to
active=False. The updated_by field stores a reference to the authenticated user's
username, who made the last change to the record.
