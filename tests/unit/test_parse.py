
import sys

sys.path.append('../app/')
sys.path.append('../app/data_manager')
import data_manager.energy
import app


# kwh mean and deaggregate
data_kwh_mean_disagg = [
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
        {
            "datetime": "2018-08-24T05:10:00Z",
            "value": 7
        },
]

data_kwh_basic = [
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