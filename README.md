# Overview

The Spaceship Power Service helps coordinators keep track of the energy usage by different ships. This project implements the Spaceship Power Service that handles POST and GET requests to an API endpoint.

***Project done as part of a take-home challenge for a data engineering position. Explores time-series data handeling and analysis.***

## Design

  See [Design.md](/docs/Design.md). See `Design.pdf` if using offline version.

## Prerequisites

  - Docker

  ```bash
  sudo apt-get update
  sudo apt-get install docker.io
  docker --version
  ```
  - Docker compose
  ```bash
  sudo curl -L "https://github.com/docker/compose/releases/download/1.23.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
  docker-compose --version
  ```
  - Avaiable ports: 5000

## Usage

  ```bash
  docker-compose up
  ```

  Sample POST
  ```curl
  curl -X POST \
    http://127.0.0.1:5000/data \
    -H 'Content-Type: application/json' \
    -H 'cache-control: no-cache' \
    -d '{
        "spaceship_id": 42,
        "units": "kW",
        "data": [
            {
                "datetime": "2019-01-05T04:37:00Z",
                "value": 1302
            },
            {
                "datetime": "2019-01-05T04:42:00ZZ",
                "value": 1200
            },
            {
                "datetime": "2019-01-05T05:42:00Z",
                "value": 3200
            }
        ]
    }'
  ```

  Sample GET
  ```curl
  curl -X GET \
    'http://127.0.0.1:5000/data?spaceship_id=42&start=2019-01-03T04:30:00Z&end=2019-01-05T05:42:00Z' \
    -H 'Content-Type: application/json' \
    -H 'cache-control: no-cache'
  ```

  **May need to use `sudo` when using docker commands depending on installation**

## Tests
  **Unit** and **integration** tests can be run once all containers are up and running. If service is already running, skip
  `docker-compose up`.
  ```bash
  docker-compose up --detach
  docker exec -it ps_web_api python -m unittest discover -v -s /tests/unit/
  docker exec -it ps_web_api python -m unittest discover -v -s /tests/integration/
  ```

## Description

  The application supports the following endpoints.

  - `POST/data`

    Given a spaceship_id and a set of energy consumption data in the request body, parse data and translate to a standard 15-minute energy format. That is, convert the incoming data to 15 minute intervals specifying energy usage. The translated data should be stored for analysis and future requests.

    - **spaceship_id** Integer identifier for a ship in the fleet.
    - **units** String usage units, kW (power) or kWh (energy).
    - **data** Timeseries array of usage in varying time intervals.
      - **datetime** String UTC, ISO8601 format timestamp.
      - **value** Integer usage at the time.

    POST example 1

      ```json
      {
          "spaceship_id": 1,
          "units": "kWh",
          "data": [
              {
                  "datetime": "2018-08-24T00:00:00Z",
                  "value": 12
              },
              {
                  "datetime": "2018-08-24T01:00:00Z",
                  "value": 26
              },
              {
                  "datetime": "2018-08-24T02:00:00Z",
                  "value": 18
              }
          ]
      }
      ```

    POST example 2

      ```json
      {
          "spaceship_id": 2,
          "units": "kW",
          "data": [
              {
                  "datetime": "2018-08-24T00:00:00Z",
                  "value": 22
              },
              {
                  "datetime": "2018-08-24T00:05:00Z",
                  "value": 24
              },
              {
                  "datetime": "2018-08-24T00:10:00Z",
                  "value": 23
              },
              {
                  "datetime": "2018-08-24T00:15:00Z",
                  "value": 18
              },
              {
                  "datetime": "2018-08-24T00:20:00Z",
                  "value": 22
              },
              {
                  "datetime": "2018-08-24T00:25:00Z",
                  "value": 23
              },
              {
                  "datetime": "2018-08-24T00:30:00Z",
                  "value": 8
              }
          ]
      }
      ```

      POST example 3

      ```json
      {
          "spaceship_id": 3,
          "units": "kWh",
          "data": [
              {
                  "datetime": "2018-08-24T00:00:00Z",
                  "value": 2
              },
              {
                  "datetime": "2018-08-24T00:15:00Z",
                  "value": 5
              },
              {
                  "datetime": "2018-08-24T00:30:00Z",
                  "value": 2
              },
              {
                  "datetime": "2018-08-24T00:45:00Z",
                  "value": 6
              }
          ]
      }
      ```

  - `GET/data?spaceship_id=x&start=y&end=z`

    Request Example

      ```url
      GET /data?spaceship_id=1&start=2018-08-24T00-00-00Z&end=2018-08-24T01-00-00Z
      ```

    Response

      ```json
      {
          "spaceship_id": 1,
          "units": "kWh",
          "data": [
              {
                  "datetime": "2018-08-24T00:00:00Z",
                  "value": 3
              },
              {
                  "datetime": "2018-08-24T00:15:00Z",
                  "value": 3
              },
              {
                  "datetime": "2018-08-24T00:30:00Z",
                  "value": 3
              },
              {
                  "datetime": "2018-08-24T00:45:00Z",
                  "value": 3
              }
          ]
      }
      ```

  - `GET/topusers?count=x&start=a&end=b` [TODO]

    Returns a list of `x` spaceship IDs and their consumption that correspond to the ships using the greatest amount of energy within the time window `[a, b]`. If no query parameters are provided, the top **3** users are returned within the entire queriable time window.

    Request Example

      ```txt
      GET /topusers?count=3&start=2018-08-24T00-00-00Z&end=2018-08-24T01-00-00Z
      ```

    Response
      ```json
    {
        "datetime": "2018-08-24T00:00:00Z",
        "ships": [
            {
                "spaceship_id": 34,
                "consumption": 5002
            },
            {
                "spaceship_id": 74,
                "consumption": 74
            },
            {
                "spaceship_id": 525,
                "consumption": 3
            }
        ]
    }
    ```
  - `GET/forecast?spaceship_id=x&start=a&end=b` [TODO]

    Returns the forecasted total energy usage of a spaceship for the time window `[a, b]` using _____ linear regression/LSTM model.

    Request Example

      ```txt
      GET /forecast?spaceship_id=774&start=2018-08-24T00-00-00Z&end=2018-08-24T01-00-00Z
      ```

    Response
      ```json
      {
        "datetime": "2018-08-24T00:00:00Z",
        "expected_consumption": 5524
      }
      ```

## Resources

https://dzone.com/articles/playing-with-docker-mqtt-grafana-influxdb-python-a

https://www.codementor.io/dongido/how-to-build-restful-apis-with-python-and-flask-fh5x7zjrx

<https://medium.com/@umerfarooq_26378/web-services-in-python-ef81a9067aaf>

<https://medium.com/backticks-tildes/lets-build-an-api-with-django-rest-framework-32fcf40231e5>

https://realpython.com/test-driven-development-of-a-django-restful-api/


https://www.analyticsvidhya.com/blog/2016/02/time-series-forecasting-codes-python/

https://machinelearningmastery.com/time-series-forecasting-methods-in-python-cheat-sheet/

https://medium.com/@riken.mehta/full-stack-tutorial-flask-react-docker-ee316a46e876

## useful commands
  ```bash
  show field keys from energy
  docker exec -it ps_influxdb bash

  precision rfc3339
  select * from energy
  ```