from influxdb import InfluxDBClient
import os
import requests
import time

class DBManager:
    '''
        Database client for influxDB

        docker run --rm \
        -p 8086:8086
        -p 2003:2003
        -e INFLUXDB_GRAPHITE_ENABLED=true
      -e INFLUXDB_DB=db0 -e INFLUXDB_ADMIN_ENABLED=true \
      -e INFLUXDB_ADMIN_USER=admin -e INFLUXDB_ADMIN_PASSWORD=supersecretpassword \
      -e INFLUXDB_USER=telegraf -e INFLUXDB_USER_PASSWORD=secretpassword \
      -v $PWD:/var/lib/influxdb \
      influxdb /init-influxdb.sh

    '''
    @staticmethod
    def setup(log):
        influx_host = os.getenv('INFLUX_HOST', 'localhost')
        influx_port = os.getenv('INFLUX_PORT', '8086')
        influx_user = os.getenv('INFLUX_USER', 'root')
        influx_pass = os.getenv('INFLUX_PASS', 'root')
        # Create our connections
        # Check to make sure we can create a connection
        got_if_connection = False
        while not got_if_connection:
            log.debug('Trying InfluxDB connection...')
            log.debug("Influx host: %s" % influx_host)
            log.debug("Influx port: %s" % influx_port)
            influx_client = InfluxDBClient(host=influx_host, port=influx_port,
                                        username=influx_user,
                                        password=influx_pass)
            try:
                log.debug('Existing dbs: {}'.format(influx_client.get_list_database()))
            except requests.exceptions.ConnectionError:
                log.debug('No InfluxDB connection yet. Waiting 5 seconds and '+
                    'retrying.')
                time.sleep(5)
            else:
                got_if_connection = True

