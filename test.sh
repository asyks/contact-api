#!/usr/bin/env bash

set -o nounset

## defaults
DEFAULT_HOST=localhost
DEFAULT_PORT=5000
REQUEST_HEADER="Content-Type: application/json"
RETURN_HEADER_STR="\n%{content_type}\n%{http_code}\n"
BASIC_AUTH_USER_PASS="admin:secret"

main () {
  # Valid Requests
  printf "Request the Site Root\n"
  curl -w ${RETURN_HEADER_STR} ${DEFAULT_HOST}:${DEFAULT_PORT}/

  printf "Create a contact\n"
  curl -H "${REQUEST_HEADER}" -X POST \
    -d '{"first_name": "foo", "last_name": "bar", "company": "acme", "email": "foo@bar.com"}' \
    -u "${BASIC_AUTH_USER_PASS}" \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contact/create \
    -w "${RETURN_HEADER_STR}"

  printf "Create a second contact\n"
  curl -H "${REQUEST_HEADER}" -X POST \
    -d '{"last_name": "taz", "company": "acme", "home_phone": 15554762438, "mobile_phone": 14767852}' \
    -u "${BASIC_AUTH_USER_PASS}" \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contact/create \
    -w "${RETURN_HEADER_STR}"

  printf "Create a third contact\n"
  curl -H "${REQUEST_HEADER}" -X POST \
    -d '{"email": "goo@bar.com", "company": "runner", "address": "5263 River St, Port Jervis, NY, 12771", "address_2": "Apartment 216"}' \
    -u "${BASIC_AUTH_USER_PASS}" \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contact/create \
    -w "${RETURN_HEADER_STR}"

  printf "Get a list of all contacts\n"
  curl -X GET ${DEFAULT_HOST}:${DEFAULT_PORT}/contacts \
    -w "${RETURN_HEADER_STR}"

  printf "Get a list of contacts filtered by company\n"
  curl -H "${REQUEST_HEADER}" -X GET \
    -d '{"company": "acme"}' \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contacts \
    -w "${RETURN_HEADER_STR}"

  printf "Get a list of contacts filtered by email and company\n"
  curl -H "${REQUEST_HEADER}" -X GET \
    -d '{"company": "acme", "email": "foo@bar.com"}' \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contacts \
    -w "${RETURN_HEADER_STR}"

  printf "Update a contact\n"
  curl -H "${REQUEST_HEADER}" -X PUT \
    -d '{"id": 1, "email": "foo@slash.com"}' \
    -u "${BASIC_AUTH_USER_PASS}" \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contact/update \
    -w "${RETURN_HEADER_STR}"

  printf "Get a conatct by id\n"
  curl -H "${REQUEST_HEADER}" -X GET -d '{"id": 1}' \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contact \
    -w "${RETURN_HEADER_STR}"

  printf "Delete a contact\n"
  curl -H "${REQUEST_HEADER}" -X DELETE \
    -d '{"id": 1}' \
    -u "${BASIC_AUTH_USER_PASS}" \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contact/delete \
    -w "${RETURN_HEADER_STR}"

  printf "Get a list of contacts filtered by email\n"
  curl -H "${REQUEST_HEADER}" -X GET \
    -d '{"email": "foo@slash.com"}' \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contacts \
    -w "${RETURN_HEADER_STR}"

  printf "\n------------------------\n"

  # Error Requests
  printf "Expect 400 json input invalid\n"
  curl -H "${REQUEST_HEADER}" -X POST \
    -d '{"email1": "z@bar.com", "name": "saz"}' \
    -u "${BASIC_AUTH_USER_PASS}" \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contact/create \
    -w "${RETURN_HEADER_STR}"

  printf "Expect 500 contact does not exist\n"
  curl -H "${REQUEST_HEADER}" -X PUT \
    -d '{"id": 5555, "email": "foo@slash.com"}' \
    -u "${BASIC_AUTH_USER_PASS}" \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contact/update \
    -w "${RETURN_HEADER_STR}"

  printf "Expect 405 method type mismatch create\n"
  curl -H "${REQUEST_HEADER}" -X GET \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contact/create \
    -w "${RETURN_HEADER_STR}"

  printf "Expect 405 method type mismatch delete\n"
  curl -H "${REQUEST_HEADER}" -X POST \
    -u "${BASIC_AUTH_USER_PASS}" \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contact/delete \
    -w "${RETURN_HEADER_STR}"

  printf "Expect 400 json query invalid\n"
  curl -H "${REQUEST_HEADER}" -X GET \
    -d '{"active": false}' \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contacts \
    -w "${RETURN_HEADER_STR}"

  printf "Expect 400 invalid json request body\n"
  curl -H "${REQUEST_HEADER}" -X POST \
    -d '{a}' \
    -u "${BASIC_AUTH_USER_PASS}" \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contact/create \
    -w "${RETURN_HEADER_STR}"

  printf "Expect 401 unauthorized create\n"
  curl -H "${REQUEST_HEADER}" -X POST \
    -d '{"email": "ioo@bar.com", "name": "laz", "company": "acme"}' \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contact/create \
    -w "${RETURN_HEADER_STR}"

  printf "Expect 401 unauthorized update\n"
  curl -H "${REQUEST_HEADER}" -X PUT \
    -d '{"id": 1, "email": "foo@dash.com"}' \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contact/update \
    -w "${RETURN_HEADER_STR}"

  printf "Expect 401 unauthorized delete\n"
  curl -H "${REQUEST_HEADER}" -X DELETE \
    -d '{"id": 1}' \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contact/delete \
    -w "${RETURN_HEADER_STR}"
}

main "${@:-}"
exit $?
