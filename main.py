
import threading


from random import  randint
import influx_helper
from time import sleep
from faker import Faker



number_of_engines = 5
engine_id_counter = 1
fake = Faker()


#Influx Client paramaters
url ="https://us-east-1-1.aws.cloud2.influxdata.com/"
org = ""
bucket  = "fuel_engine"
token = ""
ih = influx_helper.influxDBHelper(url, token, org)





class fuel_generator:
    def __init__ (self) -> None:
        global engine_id_counter, fake
         
        self.coord = fake.local_latlng(country_code='US', coords_only=False)
        self.engine_id = "engine" + str(engine_id_counter)
        engine_id_counter+=1
        self.temperature = 0
        self.pressure = 0
        
        self.base_fuel = randint(900, 1000)
        self.current_fuel = None

    def returnEngineID(self):
        return self.engine_id

   
    def returnTemperature(self):
        self.temperature = randint(-10, 90)
        return self.temperature

    def returnPressure(self):
        self.pressure = randint(100, 1000)
        return self.pressure
    
        
    def returnFuelLevel(self):
        fuel_used = randint(1, 10)
        if self.current_fuel == None:
            self.current_fuel = self.base_fuel - fuel_used
        else:
            if self.current_fuel <= 0:
                refill = randint(500, 1000)
                self.current_fuel = self.current_fuel + refill
            else:
                self.current_fuel = self.current_fuel - fuel_used


        return self.current_fuel



def runFuelEngine():
    fuelEngine = fuel_generator()
    sleeptime = randint(60, 120)
    
    while (True):
        check_engine = {"measurement": "engine_stats", "tags": {"engineID": fuelEngine.returnEngineID()},"fields": {"lat": float (fuelEngine.coord[0]), "lon": float(fuelEngine.coord[1]),
                                                                                                                "temperature": fuelEngine.returnTemperature(), 
                                                                                                                "pressure": fuelEngine.returnPressure(), 
                                                                                                                "fuel": fuelEngine.returnFuelLevel() }}
        print(check_engine,flush=True)
        sleep(sleeptime)
        ih.writeToInflux(bucket, check_engine)

    


if __name__ == "__main__":
    x = 0
    while (x <= number_of_engines):
        engine = threading.Thread(target=runFuelEngine, daemon=True)
        engine.start()
        x+=1
    sleep(500000)
