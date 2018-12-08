# contact-api
Python Take-Home Assignment: Contact API for Urban Airship Web Team

## Running the app

### With Docker and Docker Compose
To build and run:

```docker-compose up --build```

To build only:

```docker-compose build --force-rm```

### With Docker only
Build the container:

```docker build -t contact-api .```

Run the container:

```docker run --env-file=vars.env -p 127.0.0.1:5000:5000 -it contact-api```

### Debug mode
By default flask debug mode is set to 0/off via FLASK_DEBUG. To turn on debug mode
edit the arg in docker-compose.yaml and rebuild with `docker-compose`, or build
the image specifiying DEBUG=1 as a build-arg.

```docker build --build-arg DEBUG=1 -t contact-api ```

**Note:**
I've run into an issue a couple times with apk failing to find or download
the sqlite package, normally just rerunning the build step fixes this problem,
sometimes multiple reruns are required.

## Endpoints

### Create Contact
To create a contact record send a POST request with json body to `/contact/create`.
On success a 200 response containing the record should be sent to the client.

### Get one Contact
To get a single contact by id send a GET request with json body to `/contact`.
On success a 200 response containing the record should be sent to the client.
The field id is required.

### Get multiple Contacts
To get a list of contacts send a GET request with or without a json body to `/contacts`.
By default all (active/non-deleted) contacts are returned.
Contact records can be filtered by supplying json fields in the request body.
The supported fields are: email and company. If both fields are supplied the
result with be anded together, so email and company must match the values supplied.
On success a 200 response containing the records should be sent to the client.

### Update Contact
To update an existing contact send a PUT request with json body to `/contact/update`.
On success a 201 response containing the record should be sent to the client.
The field id is required.

### Delete Contact
To delete a contact send a DELETE request with json body to `/contact/delete`.
On success a 200 response containing the record should be sent to the client.
The field id is required.

## Test script

As I was working writing the endpoints I wrote a test script `test.sh` for
curl-ing them with different data/headers/methods. I tried to add curls for all
the required functionality, as well as several error responses. `

## Basic Auth

I stuck to having a single set of creds. To change the creds set the env vars:
USERNAME and PASSWORD. The default creds are stored in `vars.env`. I adapted my
basic auth solution from [this flask snippet](http://flask.pocoo.org/snippets/8/).

## Data

I decided to go with a sqlite in-memory database, as it seemed to be an easy
and reliable way to create a persistent (between app restarts) datastore that does
not write to the filesystem. I stuck with a single model/table for Contact, with
no unique fields. The fields of the Contact model are:

  * id -  primary key
  * active - bool, stores delete status, if True the record is hidden from views
  * first_name - string
  * last_name - string
  * company - string
  * email - string
  * phone - integer
  * address - string
  * address_2 - string
  * updated_by - stores the username of the user who last changed the record

## TODO

Given more time to work on the project, there's a number of things I'd add or
improve. I hadn't worked with flask in a while, and had to brush up on some of the
basic concepts. In many cases I chose simple solutions the I felt met the
requirements in leiu of more robust options. Roughly in order of importance:

  * Moving the model class to a separate module - keeping the model and views in
  the same module seemed like the easiest way to ensure that everything references
  the same app instance, but I'd like to look more into using an app factory.
  * Adding pagination to the get_contacts endpoint - This is the only endpoint that
  can return multiple records, it returns all active contacts by default, and should
  ideally support pagination to reduce load on the db for larger datasets.
  * Fine tuning model fields - I chose the datatypes and lengths for each
  field somewhat arbitrarily, and would like to take another pass over them and
  make adjustments. I'd also like to do some additional syntax validation for fields
  storing standard things like email addresses, and phone numbers. It looks like this
  could be done pretty easily using Flask-WTF and/or WTForms.
  * Sanitizing json field values - I've read that SQLAlchemy handles quoting special 
  characters in inputs on its own, so this may not be necessary, but given more time
  I'd do further reading/testing to verify whether that is in fact the case.
  * Improving error handling and responses
  * Adding logging where appropriate
