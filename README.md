
Sensor Data Logger README
This repository contains a Python script that reads temperature and humidity data from an Adafruit HTU21D sensor and stores it in a MariaDB (MySQL) database. The script is designed to run on a Raspberry Pi or a similar device. It periodically reads sensor data and inserts it into the database for further analysis and monitoring.

## Prerequisites
Before running the script, ensure you have the following components and software installed:

- Raspberry Pi (or similar) with the required GPIO pins.
- Adafruit HTU21D temperature and humidity sensor.
- Python 3.x installed on your device.
- MariaDB (MySQL) database server set up with appropriate access credentials.
- Required Python packages: `busio`, `board`, `mariadb`, and `adafruit_htu21d`. You can install them using pip:

`pip install adafruit-circuitpython-htu21d mariadb`

## Configuration
The script requires two JSON configuration files: `config.json` and `secrets.json`.

- `config.json` contains general configuration parameters for the script:
* database_user: MariaDB username for accessing the database.
* host: Database host address.
* port: Database port number.
* database: Name of the database to store the data.
* dt: Time interval (in seconds) between sensor readings.
- `secrets.json` contains sensitive information like the database password. Make sure to keep this file secure and don't share it in public repositories.

Example `config.json`:
```
{
  "database_user": "your_username",
  "host": "localhost",
  "port": 3306,
  "database": "sensor_data",
  "dt": 300
}
```
Example secrets.json:
```
{
  "database_password": "your_password"
}
```
## Usage
Clone this repository to your Raspberry Pi.

Create the `config.json` and `secrets.json` files with appropriate values.

Connect the Adafruit HTU21D sensor to the appropriate GPIO pins on your Raspberry Pi.

Run the script using the following command:

```python sensor_data_logger.py```

The script will establish a connection to the database, read sensor data at the specified interval, and insert it into the database. The process will continue indefinitely until manually stopped.

## Important Notes
The script uses the autocommit = False option while connecting to the database to ensure data consistency. It commits the data after each insert operation.

The adafruit_htu21d library is used to interface with the HTU21D sensor. Ensure the sensor is properly connected to the I2C pins.

Make sure you have the necessary privileges and firewall settings to allow the Raspberry Pi to connect to the MariaDB database.

This script provides a basic example of logging sensor data. Depending on your needs, you might want to add error handling, data validation, or more advanced database interactions.

Always keep your sensitive information (passwords, API keys, etc.) secure and avoid sharing them in public repositories.

## License
This script is provided under the MIT License. Feel free to modify and distribute it as needed while keeping the original license intact.
