# Importing the libraries
import sched, time

# Importing the process
from .soilmoisture_prediction import predict_soil_moisture_from_database
from .pumping_time_prediction import predict_pumping_time_from_database

# Scheduler
s = sched.scheduler(time.time, time.sleep)

# Date and time for first prediction time
start_date = time.strftime("%Y-%m-%d", time.localtime())
start_time = '07:00:00'

# Active prediction time
active_time_string = start_date + " " + start_time
ts = time.strptime(active_time_string, "%Y-%m-%d %H:%M:%S")
active_time_seconds = time.mktime(ts)

# Future prediction duration measured by minute
future_minutes = 30

# Time step to next prediction time measured by second
timestep_seconds = future_minutes * 60

# Initial number of records
number_of_records = 1080

# Sampling pace measured by seconds
sampling_pace = 5

# Model file path

def prediction_process():
  global active_time_seconds
  global number_of_records
  global future_minutes
  
  while True:
    if active_time_seconds >= time.time():
      active_time_struct = time.localtime(active_time_seconds)
      
      # Reset prediction time
      if (active_time_struct.tm_hour == 12 and active_time_struct.tm_min == 0 and active_time_struct.tm_sec == 0):
        active_time_seconds += 19 * 3600
        number_of_records = 1080
      
      # Schedule prediction
      s.enterabs(active_time_seconds, 1, predict_soil_moisture_from_database, argument=(active_time_seconds, number_of_records, future_minutes,))
      s.enterabs(active_time_seconds, 2, predict_pumping_time_from_database, argument=(active_time_seconds, future_minutes))
      s.run()

    active_time_seconds += timestep_seconds
    number_of_records += timestep_seconds // sampling_pace

if __name__ == '__main__':
  prediction_process()