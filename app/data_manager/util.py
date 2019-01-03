import pandas as pd
import json


TIME_FREQ = '15T'


data = [
    # {
    #     "datetime": "2018-08-24T04:00:00Z",
    #     "value": 2
    # },
    # {
    #     "datetime": "2018-08-24T04:01:00Z",
    #     "value": 1
    # },
    # {
    #     "datetime": "2018-08-24T04:00:00Z",
    #     "value": 2
    # },
    # {
    #     "datetime": "2018-08-24T04:05:00Z",
    #     "value": 1
    # },
    # {
    #     "datetime": "2018-08-24T04:10:00Z",
    #     "value": 6
    # },
    # {
    #     "datetime": "2018-08-24T05:10:00Z",
    #     "value": 7
    # },
    {
        # "datetime": "2018-08-24T06:10:00Z",
        "value": 4
    },
    {
        "datetime": "2018-08-24T05:45:00Z",
        "value": 5
    },

    ]

df = pd.DataFrame(data)
df['datetime'] = pd.to_datetime(df['datetime'])
df = df.set_index('datetime')
df = df.sort_index()
df['value'] = df['value'].astype('float')
print('Pre: \n', df)
# rg = pd.date_range(df['datetime'].min(), df['datetime'].max(), freq='15min')
# print('Date range: ', rg)

print('no-duplicates-ts: ', pd.Series(df.index).is_unique)

print('has null: ', df.index.isnull().any().any())
# df = df.groupby(pd.Grouper(freq='15Min', label='right')).mean()
# df = df.fillna(method='ffill')
# df = df.resample('15T', label='right').mean()
# df = df.fillna(method='ffill')

# df = df.resample('15T').mean()
# df = df.resample('15T', closed='right').ffill()
# df = df.groupby(pd.Grouper(freq='15Min', label='right')).mean() #  closed='right'
# df = df.resample('15T', closed='left').first()
# df = df.fillna(method='ffill')
# df = df.resample(TIME_FREQ, label='right').sum()




# -ve val check
# print(any(df['value'] < 0))

# timestamp check



print('\n\nPost: \n')
print(df)

print('value type: ', type(df['value'][0]))


# from flask import jsonify

# print(json.dumps({'data': 89, 'a': [1,2,3]}))

# print(json.dumps({'entries': [
#   {
#     't': 's',
#     'v': 5
#   }
# ]}))
# df.groupby('datetime')['value'].fillna(method='ffill') # fill in row 5 but not row 3