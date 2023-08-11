import datetime
import sys
import time
import board
import busio
import mariadb
from adafruit_htu21d import HTU21D
import json

def load_json(file_path):
    with open(file_path, 'r') as secrets_file:
        secrets = json.load(secrets_file)
    return secrets

config = load_json("./config.json")
secrets = load_json("./secrets.json")

i2c = busio.I2C(board.SCL, board.SDA)
sensor = HTU21D(i2c)
print("Connecting to database...")
conn = mariadb.connect(
        user = config["database_user"],
        password = secrets["database_password"],
        host = config["host"], 
        port = config["port"], 
        database = config["database"],
        autocommit = False
)
cur = conn.cursor()
print("Connection is ready")
while True:
    day = datetime.datetime.now().day
    temperature = sensor.temperature
    humidity = sensor.relative_humidity
    now = datetime.datetime.utcnow()
    query = f"INSERT INTO {config[table]} (date, temperature, humidity) VALUES ('{now}', '{temperature}', '{humidity}')"
    print(query)
    cur.execute(query)
    conn.commit()
    time.sleep(config["dt"])


