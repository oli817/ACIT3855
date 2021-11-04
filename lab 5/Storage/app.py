import connexion
from connexion import NoContent
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from temperature import Temperature
from windspeed import Windspeed
from base import Base
import yaml
import logging, logging.config
import datetime


with open("app_conf.yml", "r") as f:
    app_config = yaml.safe_load(f.read())
    db_info = app_config["db"]

with open("log_conf.yml", "r") as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    logger = logging.getLogger("basicLogger")

DB_ENGINE = create_engine("mysql+pymysql://%s:%s@%s:%s/%s"
                          % (db_info["user"], db_info["password"], db_info["hostname"], db_info["port"], db_info["db"]))
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

# MAX_EVENTS = 12
# EVENTS_FILE = "events.json"
# logs = []


def report_outside_temperature_reading(body):
    # logs.append(body)
    # if len(logs) > MAX_EVENTS:
    #     logs.pop(0)
    # log_json(logs)
    # return logs, 201
    session = DB_SESSION()

    ot = Temperature(body['sensor_id'],
                       body['address_id'],
                       body['outside_temperature'],
                       body['timestamp']
                       )

    session.add(ot)
    session.commit()
    session.close()

    logger.info("Stored event %s request with a unique id of %s" % ("temperature", body["sensor_id"]))
    return NoContent, 201

def get_outside_temperature_reading(timestamp):
    """ Gets new blood pressure readings after the timestamp """
    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    readings = session.query(Temperature).filter(Temperature.date_created >= timestamp_datetime)
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()
    logger.info("Query for Temperature readings after %s returns %d results" % (timestamp, len(results_list)))
    return results_list, 200

def report_wind_speed_reading(body):
    # logs.append(body)
    # if len(logs) > MAX_EVENTS:
    #     logs.pop(0)
    # log_json(logs)
    # return logs, 201
    session = DB_SESSION()

    ws = Windspeed(body['sensor_id'],
                     body['address_id'],
                     body['wind_speed'],
                     body['timestamp']
                     )

    session.add(ws)
    session.commit()
    session.close()

    logger.info("Stored event %s request with a unique id of %s" % ("wind_speed", body["sensor_id"]))
    return NoContent, 201

def get_wind_speed_reading(timestamp):
    """ Gets new blood pressure readings after the timestamp """
    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    readings = session.query(Windspeed).filter(Windspeed.date_created >= timestamp_datetime)
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()
    logger.info("Query for Wind speed readings after %s returns %d results" % (timestamp, len(results_list)))
    return results_list, 200

# def report_humidity_reading(body):
#     logs.append(body)
#     if len(logs) > MAX_EVENTS:
#         logs.pop(0)
#     log_json(logs)
#     return logs, 201


# def log_json(logs):
#     final_logs = json.dumps(logs, indent=4)
#     with open(EVENTS_FILE, 'w') as file:
#         file.write(final_logs)





app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("oli817-weather-1.0.0-swagger.yaml",
            strict_validation=True,
            validate_responses=True)



if __name__ == "__main__":
    logger.info("Connecting to DB. Hostname: %s , Port: %d" % (db_info["hostname"], db_info["port"]))
    app.run(port=8090)

