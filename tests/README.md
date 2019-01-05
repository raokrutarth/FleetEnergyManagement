
# Description

Integration & unit tests.

**Unit** and **integration** tests can be run once all containers are up and running. If service is already running, skip
`docker-compose up --detach`. When using `docker-compose up --detach`, services may take upto a minute to become available
as the docker images are pulled.

```bash
docker-compose up --detach
docker exec -it ps_web_api python -m unittest discover -v -s /tests/unit/
docker exec -it ps_web_api python -m unittest discover -v -s /tests/integration/
```