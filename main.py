
import threading


from random import  randint
import influx_helper
from time import sleep
from faker import Faker



number_of_generators = 5
generator_id_counter = 1
fake = Faker()


#Influx Client paramaters
url =""
org = ""
bucket  = "emergency_generators"
token = ""
ih = influx_helper.influxDBHelper(url, token, org)





class fuel_generator:
    def __init__ (self) -> None:
        global generator_id_counter, fake
         
        self.coord = fake.local_latlng(country_code='US', coords_only=False)
        self.generator_id = "generator" + str(generator_id_counter)
        generator_id_counter+=1
        self.temperature = 0
        self.pressure = 0
        
        self.base_fuel = randint(900, 1000)
        self.current_fuel = None

    def returnGeneratorID(self):
        return self.generator_id

   
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



def runFuelGenerator():
    fuelgenerator = fuel_generator()
    sleeptime = randint(60, 120)
    
    while (True):
        check_generator = {"measurement": "generator_stats", "tags": {"generatorID": fuelgenerator.returnGeneratorID()},"fields": {"lat": float (fuelgenerator.coord[0]), "lon": float(fuelgenerator.coord[1]),
                                                                                                                "temperature": fuelgenerator.returnTemperature(), 
                                                                                                                "pressure": fuelgenerator.returnPressure(), 
                                                                                                                "fuel": fuelgenerator.returnFuelLevel() }}
        print(check_generator,flush=True)
        sleep(sleeptime)
        ih.writeToInflux(bucket, check_generator)

    


if __name__ == "__main__":
    x = 0
    while (x <= number_of_generators):
        generator = threading.Thread(target=runFuelGenerator, daemon=True)
        generator.start()
        x+=1
    sleep(500000)
