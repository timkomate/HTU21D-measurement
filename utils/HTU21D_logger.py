import datetime
import time
import board
import busio
import mariadb
from adafruit_htu21d import HTU21D
import json
import logging


class HTU21DLogger:
    def __init__(self, config_path, secrets_path):
        self.config = self.load_json(config_path)
        self.secrets = self.load_json(secrets_path)
        self.init_logging()
        self.init_database_connection()
        self.init_sensor()

    @staticmethod
    def load_json(file_path):
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
        return data

    def init_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger(__name__)

    def init_database_connection(self):
        try:
            self.conn = mariadb.connect(
                user=self.config["database_user"],
                password=self.secrets["database_password"],
                host=self.config["host"],
                port=self.config["port"],
                database=self.config["database"],
                autocommit=False,
            )
            self.cur = self.conn.cursor()
            self.logger.info("Database connection is ready")
        except mariadb.Error as e:
            self.logger.error(
                f"An error occurred while connecting to the database: {e}"
            )
            sys.exit(1)

    def init_sensor(self):
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            self.sensor = HTU21D(i2c)
        except Exception as e:
            self.logger.error(f"An error occurred while initializing the sensor: {e}")
            sys.exit(1)

    def log_sensor_data(self):
        while True:
            day = datetime.datetime.now().day
            temperature = self.sensor.temperature
            humidity = self.sensor.relative_humidity
            now = datetime.datetime.utcnow()
            query = f"INSERT INTO {self.config['table_name']} (date, temperature, humidity) VALUES ('{now}', '{temperature}', '{humidity}')"
            self.logger.info(query)
            try:
                self.cur.execute(query)
                self.conn.commit()
            except mariadb.Error as e:
                self.logger.error(
                    f"An error occurred while inserting data into the database: {e}"
                )
                self.conn.rollback()
            time.sleep(self.config["dt"])

    def run(self):
        try:
            self.logger.info("Starting sensor data logging...")
            self.log_sensor_data()
        finally:
            self.cur.close()
            self.conn.close()
            self.logger.info("Database connection closed")
