""" For each date present in cape_town_day_stages insert all load-shedding stages with times for day into DB. Json file is generated
    from jupyter notebook in eskom_past_stages
"""
import psycopg2
import json
from decouple import config


#Connect to Database    
conn = psycopg2.connect(database = config('DB_NAME', default=''),
                        user = config('DB_USER', default=''),
                        password = config('DB_PASSWORD', default=''),
                        host = config('DB_HOST', default=''),
                        port = config('DB_PORT', default=''))
    
cur = conn.cursor()
t_name = 'cape_town_past_stages'

#load json file into data dict
with open('cape_town_day_stages.json') as json_file:
    data = json.load(json_file)

#Uncomment to create table
#cur.execute(f"""CREATE TABLE {t_name} (
#            past_stage_id serial PRIMARY KEY, 
#            date DATE NOT NULL, 
#            stage SMALLINT NOT NULL, 
#            start_time TIME NOT NULL, 
#            end_time TIME NOT NULL);""")

cur.execute(f"""SET datestyle = dmy;""")

for day,day_slots in data.items(): 
    #For each day in data dict
    for slot_num, slot in day_slots.items():
        #Insert each stage slot into table with day field
        cur.execute(f"""INSERT INTO {t_name} (date, stage, start_time, end_time) 
                    VALUES ('{day}', {slot['stage']}, '{slot['start']}', '{slot['end']}');""")
   
conn.commit()
print("Records created successfully")
conn.close()