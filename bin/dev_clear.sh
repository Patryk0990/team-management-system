#!/bin/bash
set -e

{
    docker compose stop
    docker compose rm -svf

} || {
    docker-compose stop
    docker-compose rm -svf
}

docker volume list | egrep 'team-management-system_.+data' | awk '{ print $2 }' | xargs -r docker volume rm
docker images | egrep 'team-management-system-.+' | awk '{ print $1 }' | xargs docker rmi -f || true