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
    -d '{"email": "foo@bar.com", "name": "baz", "company": "acme"}' \
    -u "${BASIC_AUTH_USER_PASS}" \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contact/create \
    -w "${RETURN_HEADER_STR}"

  printf "Create a second contact\n"
  curl -H "${REQUEST_HEADER}" -X POST \
    -d '{"email": "goo@bar.com", "name": "taz", "company": "acme"}' \
    -u "${BASIC_AUTH_USER_PASS}" \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contact/create \
    -w "${RETURN_HEADER_STR}"

  printf "Create a third contact\n"
  curl -H "${REQUEST_HEADER}" -X POST \
    -d '{"email": "hoo@bar.com", "name": "saz", "company": "runner"}' \
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

  printf "Get a list of contacts filtered by email\n"
  curl -H "${REQUEST_HEADER}" -X GET \
    -d '{"email": "foo@bar.com"}' \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contacts \
    -w "${RETURN_HEADER_STR}"

  printf "Get a conatct by id\n"
  curl -H "${REQUEST_HEADER}" -X GET -d '{"id": 1}' \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contact \
    -w "${RETURN_HEADER_STR}"

  printf "Update a contact\n"
  curl -H "${REQUEST_HEADER}" -X PUT \
    -d '{"id": 1, "email": "foo@slash.com"}' \
    -u "${BASIC_AUTH_USER_PASS}" \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contact/update \
    -w "${RETURN_HEADER_STR}"

  printf "Delete a contact\n"
  curl -H "${REQUEST_HEADER}" -X DELETE \
    -d '{"id": 1}' \
    -u "${BASIC_AUTH_USER_PASS}" \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contact/delete \
    -w "${RETURN_HEADER_STR}"

  printf "\n------------------------\n"

  # Error Requests
  printf "Expect contact does not exist\n"
  curl -H "${REQUEST_HEADER}" -X PUT \
    -d '{"id": 5555, "email": "foo@slash.com"}' \
    -u "${BASIC_AUTH_USER_PASS}" \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contact/update \
    -w "${RETURN_HEADER_STR}"

  printf "Expect method type mismatch\n"
  curl -H "${REQUEST_HEADER}" -X GET \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contact/create \
    -w "${RETURN_HEADER_STR}"

  printf "Expect 'active' not supported\n"
  curl -H "${REQUEST_HEADER}" -X GET \
    -d '{"active": false}' \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contacts \
    -w "${RETURN_HEADER_STR}"

  printf "Expect invalid json request body\n"
  curl -H "${REQUEST_HEADER}" -X POST \
    -d '{a}' \
    -u "${BASIC_AUTH_USER_PASS}" \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contact/create \
    -w "${RETURN_HEADER_STR}"

  printf "Expect missing 'email' field\n"
  curl -H "${REQUEST_HEADER}" -X POST \
    -d '{"name": "foobar", "company": "acme"}' \
    -u "${BASIC_AUTH_USER_PASS}" \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contact/create \
    -w "${RETURN_HEADER_STR}"

  printf "Expect internal server error\n"
  curl -H "${REQUEST_HEADER}" -X PUT \
    -d '{"email": "foo@slash.com"}' \
    -u "${BASIC_AUTH_USER_PASS}" \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contact/update \
    -w "${RETURN_HEADER_STR}"

  printf "Expect unauthorized against create\n"
  curl -H "${REQUEST_HEADER}" -X POST \
    -d '{"email": "ioo@bar.com", "name": "laz", "company": "acme"}' \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contact/create \
    -w "${RETURN_HEADER_STR}"

  printf "Expect unauthorized against update\n"
  curl -H "${REQUEST_HEADER}" -X PUT \
    -d '{"id": 1, "email": "foo@dash.com"}' \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contact/update \
    -w "${RETURN_HEADER_STR}"

  printf "Expect unauthorized against delete\n"
  curl -H "${REQUEST_HEADER}" -X DELETE \
    -d '{"id": 1}' \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contact/delete \
    -w "${RETURN_HEADER_STR}"
}

main "${@:-}"
exit $?
