

from uuid import uuid1
BASIC = {
    "spaceship_id": str(uuid1()),
    "units": "kWh",
    "data": [
        {
            "datetime": "2018-08-24T00:00:00Z",
            "value": 300
        },
        {
            "datetime": "2018-08-24T00:15:00Z",
            "value": 700
        },
        {
            "datetime": "2018-08-24T00:30:00Z",
            "value": 200
        },
        {
            "datetime": "2018-08-24T00:45:00Z",
            "value": 100
        }
    ]
}

TO_DISSAGG = {
    "spaceship_id": str(uuid1()),
    "units": "kWh",
    "data": [
        {
            "datetime": "2019-01-01T04:00:00Z",
            "value": 2
        },
        {
            "datetime": "2019-01-01T04:30:00Z",
            "value": 1
        },
        {
            "datetime": "2019-01-01T05:00:00Z",
            "value": 6
        },
    ]
}

TO_AGG = {
    "spaceship_id": str(uuid1()),
    "units": "kWh",
    "data": [
        {
            "datetime": "2018-08-24T04:00:00Z",
            "value": 2
        },
        {
            "datetime": "2018-08-24T04:05:00Z",
            "value": 1
        },
        {
            "datetime": "2018-08-24T04:10:00Z",
            "value": 6
        },
    ]
}

TO_CONV = {
    "spaceship_id": str(uuid1()),
    "units": "kW",
    "data": [
        {
            "datetime": "2006-12-24T04:00:00Z",
            "value": 230
        },
        {
            "datetime": "2006-12-24T04:15:00Z",
            "value": 120
        },
        {
            "datetime": "2006-12-24T04:30:00Z",
            "value": 650
        },
    ]
}

TO_CONV_AGG = {
    "spaceship_id": str(uuid1()),
    "units": "kW",
    "data": [
        {
            "datetime": "2006-12-24T23:00:01Z",
            "value": 2
        },
        {
            "datetime": "2006-12-24T23:05:01Z",
            "value": 1
        },
        {
            "datetime": "2006-12-24T23:10:01Z",
            "value": 6
        },
    ]
}

TO_CONV_DISAGG = {
    "spaceship_id": str(uuid1()),
    "units": "kW",
    "data": [
        {
            "datetime": "2006-12-24T04:00:00Z",
            "value": 2
        },
        {
            "datetime": "2006-12-24T05:00:00Z",
            "value": 1
        },
        {
            "datetime": "2006-12-24T06:00:00Z",
            "value": 6
        },
    ]
}

TO_CONV_MIXED = {
    "spaceship_id": str(uuid1()),
    "units": "kW",
    "data": [
        {
            "datetime": "2006-12-24T03:45:00Z",
            "value": 6
        },
        {
            "datetime": "2006-12-24T04:20:00Z",
            "value": 6
        },
        {
            "datetime": "2006-12-24T04:00:00Z",
            "value": 2
        },
        {
            "datetime": "2006-12-24T05:00:00Z",
            "value": 4
        },
        {
            "datetime": "2006-12-24T06:00:00Z",
            "value": 6
        },
    ]
}