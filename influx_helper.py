from influxdb_client import InfluxDBClient



class influxDBHelper ():
    def __init__ (self, url, token, org) -> None:
        self.client = InfluxDBClient(url=url, token=token, org=org, debug=False)
        self.write_api = self.client.write_api()
        self.query_api = self.client.query_api()


    
    # dict {"measurement": "h2o_feet", "tags": {"location": "coyote_creek"},
    #                                  "fields": {"water_level": 1.0}, "time": 1}
    def writeToInflux(self, bucket: str, data: dict) -> None:
        try:
            self.write_api.write(bucket=bucket, record=data)
        except:
            print("Failed to write to Influx.")