import connexion
from connexion import NoContent
import logging,logging.config
import json
import requests
import yaml

# MAX_EVENTS = 12
# EVENTS_FILE = "events.json"
# logs = []

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    logger = logging.getLogger('basicLogger')

def report_outside_temperature_reading(body):
    # logs.append(body)
    # if len(logs) > MAX_EVENTS:
    #     logs.pop(0)
    # log_json(logs)
    # return logs, 201
    logger.info("Received event %s request with a unique id of %s"
                % ("read temperature", body["sensor_id"]))
    headers = {"content-type": "application/json"}
    response = requests.post(app_config["temperature"]["url"], json=body, headers=headers)
    logger.info("Returned event %s response %s with status %s"
                % ("read temperature", body["sensor_id"], response.status_code))

    # if response.status_code == 201:
    #     print(response.json())

    return NoContent, response.status_code

def report_wind_speed_reading(body):
    # logs.append(body)
    # if len(logs) > MAX_EVENTS:
    #     logs.pop(0)
    # log_json(logs)
    # return logs, 201
    logger.info("Received event %s request with a unique id of %s"
                % ("read wind speed", body["sensor_id"]))
    headers = {"content-type": "application/json"}
    response = requests.post(app_config["wind_speed"]["url"], json=body, headers=headers)
    logger.info("Returned event %s response %s with status %s"
                % ("read wind speed", body["sensor_id"], response.status_code))
    # if response.status_code == 201:
    #     print(response.json())

    return NoContent, response.status_code


# def log_json(logs):
#     final_logs = json.dumps(logs, indent=4)
#     with open(EVENTS_FILE, 'w') as file:
#         file.write(final_logs)





app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("oli817-weather-1.0.0-swagger.yaml",
            strict_validation=True,
            validate_responses=True)





if __name__ == "__main__":
    app.run(port=8080)

