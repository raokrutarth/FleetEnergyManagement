# Overview

The Spaceship Power Service helps coordinators keep track of the energy usage by different ships. This project implements the Spaceship Power Service that handles POST and GET requests to an API endpoint.

***Project done as part of a take-home challenge for a data engineering position. Explores time-series data handeling, visualization and analysis.***

## Prerequisites

- Docker
- Docker compose
- Linux?

## Description

The application supports the following endpoints.

- `POST/data`

  Given a spaceship_id and a set of energy consumption data in the request body, parse data and translate to a standard 15-minute energy format. The translated data should be stored for analysis and future requests.

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

- `GET/topusers?count=x&start=a&end=b`

  Returns a list of `x` spaceship IDs and their consumption that correspond to the ships using the greatest amount of energy within the .

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
                "spaceship_id": "2018-08-24T00:30:00Z",
                "consumption": 3
            }
        ]
    }
    ```
