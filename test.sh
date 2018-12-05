#!/usr/bin/env bash

set -o nounset

## defaults
DEFAULT_HOST=localhost
DEFAULT_PORT=5000
REQUEST_HEADER="Content-Type: application/json"
RETURN_HEADER_STR="\n%{content_type}\n%{http_code}"

main () {
  #curl -w ${RETURN_HEADER_STR} ${DEFAULT_HOST}:${DEFAULT_PORT}/

  curl -H "${REQUEST_HEADER}" -X POST -d '{"email": "foo@bar.com", "name": "baz"}' \
    ${DEFAULT_HOST}:${DEFAULT_PORT}/contact/create \
    -w "${RETURN_HEADER_STR}"
}

main "${@:-}"
exit $?
