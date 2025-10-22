from db_client_ABC import db_client
from influxdb_client import InfluxDBClient
from templates import influx_template

class InfluxDB_client(db_client):
    """ influxdb client """
    def __init__(self, connection_datas:dict):
        self.org = connection_datas['org']
        self.token = connection_datas['token']
        self.url = connection_datas['url']
        self.connected = False
        self.buckets: list[str] = []
    
    def connect(self):
        # try to create a client
        self.client = InfluxDBClient(
            url=self.url, org=self.org, token=self.token
        )
        if self.client.ping():
            self.connected = True
            print('connecting successfully')
            self.initialize_metrics()
        else:
            del self.client
            print('connnection failed, please check and reset the log in infos.')
        
    def initialize_metrics(self):
        buckets_api = self.client.buckets_api()
        buckets = buckets_api.find_buckets()
        self.buckets = buckets.buckets
        
    def disconnect(self):
        # disconnect the client
        if self.connected:
            self.client.close()
            del self.client
    
    def query(self, query_tmp, bucket, start, stop, measurement_name, field):
        if self.connected:
            query_api = self.client.query_api()
            query_exp = query_tmp.format(bucket=bucket,start=start,stop=stop,measurement_name=measurement_name,field=field)
            # print(query_exp
            try:
                query_result = query_api.query(query_exp)
            except Exception as e:
                raise 
            else:
                return query_result
        else:
            print('Connect first, please.')

    def write_data(self):
        pass

    def describe(self):
        pass

if __name__ == '__main__':
    import os
    import json
    connection_datas = {
        'org' : 'DFMC',
        'url' : 'http://localhost:8086',
        'token' : os.getenv('INFLUXDB_TOKEN')
    }
    influxdb_client = InfluxDB_client(connection_datas)
    influxdb_client.connect()
    # for bucket in influxdb_client.buckets:
    #     print(bucket.name)
    query1 = influx_template.query1
    query2 = influx_template.query2
    try:
        # query_result = influxdb_client.query(query1,bucket='test_data',
        #                                 start='2025-07-30T05:20:00Z', stop='2025-08-29T05:20:00Z',
        #                                 measurement_name='processing_quantity',
        #                                 field='1')
        query_result = influxdb_client.query(query2,bucket='test_data',
                                        start='-180d', stop='now()',
                                        measurement_name='processing_quantity',
                                        field='1')
    except Exception as e:
        ebody = e.body.decode('utf-8')
        obj = json.loads(ebody)
        print(obj)
    # else:
    #     from typing import Iterable
    #     print(isinstance(query_result,Iterable))


    for table in query_result:
        print(table)
        for row in table:
            print(row.values)
