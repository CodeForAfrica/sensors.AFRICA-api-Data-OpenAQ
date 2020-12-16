import time
from operator import itemgetter

import arrow

from chalicelib import settings
from chalicelib.openaq_api import DEFAULT_START_DATE, Api
from chalicelib.sensorsafrica import DB
from chalicelib.sheets import ApiParametersSheet


def from_openaq_to_location_json(json):
    city, coordinates, country, location = itemgetter(
        "city", "coordinates", "country", "location"
    )(json)
    return {
        "location": location,
        "city": city,
        "country": country,
        "latitude": f"{coordinates['latitude']}",
        "longitude": f"{coordinates['longitude']}",
    }


def from_openaq_to_node_json(json, location):
    uid = f"oaqn_{json['id']}"
    return {
        "uid": uid,
        "location": location.id,
        "owner": location.owner,
    }


def from_openaq_to_sensor_type_json(json):
    uid = f"oaqs_{json['id']}"
    name = f"OpenAQ {json['id']}"
    manufacturer = "OpenAQ"
    return {
        "uid": uid,
        "name": name,
        "manufacturer": manufacturer,
    }


def from_openaq_to_sensor_jsons(json, sensor_type, node):
    if not json.get("parameters"):
        return []

    aq_parameters = [
        (x.strip()).lower()
        for x in settings.OPENAQ_API_PARAMETERS.split(",")
        if x.strip()
    ]
    sensor_parameters = [(x.strip()).lower() for x in json["parameters"] if x.strip()]
    matched_parameters = list(filter(lambda x: x in aq_parameters, sensor_parameters))
    sensors = []
    for param in matched_parameters:
        sensor = {
            "sensor_type": sensor_type.id,
            "node": node.id,
            "pin": settings.OPENAQ_API_PARAMETERS_PIN_MAPPING[param],
        }
        sensors.append(sensor)

    return sensors


def from_openaq_to_sensor_data_json(json):
    if not (json.get("parameter") and json.get("date")):
        return None

    sensor_parameter = json["parameter"].strip().lower()
    aq_parameters = [
        (x.strip()).lower()
        for x in settings.OPENAQ_API_PARAMETERS.split(",")
        if x.strip()
    ]
    if sensor_parameter not in aq_parameters:
        return None
    timestamp = json["date"].get("utc") or json["date"].get("local")
    if not timestamp:
        return None
    sampling_rate = None
    averaging_period = json.get("averagingPeriod")
    if averaging_period:
        # OpenAQ seem to be "averaging" values per hour
        sampling_rate = int(averaging_period.get("value") * 3600)
    value = json["value"]
    value_type = settings.SENSORSAFRICA_API_PARAMETER_MAPPING[sensor_parameter]
    return {
        "sampling_rate": sampling_rate,
        "timestamp": timestamp,
        "sensordatavalues": [
            {
                "value": value,
                "value_type": value_type,
            }
        ],
    }


def find_node_for_location(location, nodes_per_location, api, params=None):
    node = nodes_per_location.get(location)
    if node:
        return node

    # We're most probably dealing with renamed location
    results = api.location(location, params)
    if len(results):
        for result in results:
            # Find those results that have exact location in their locations list
            locations = result.get("locations")
            if locations and location in locations:
                # Return first node with location matching those in locations
                for possible_location in locations:
                    node = nodes_per_location.get(possible_location)
                    if node:
                        # Remember the new location
                        nodes_per_location[location] = node
                        return node

    return None


def run(app):
    data_count = 0
    sheet = ApiParametersSheet()
    api_parameters = sheet.load()
    if api_parameters:
        api = Api(api_parameters)
        db = DB()
        start_time = arrow.utcnow()
        location_results = api.locations()
        for result in location_results:
            last_end_date = api_parameters.get("last_end_date")
            # New location
            if not last_end_date or result.get("firstUpdated") > last_end_date:
                location_json = from_openaq_to_location_json(result)
                location = db.add_location(location_json)
                node_json = from_openaq_to_node_json(result, location)
                node = db.add_node(node_json)
                sensor_type_json = from_openaq_to_sensor_type_json(result)
                sensor_type = db.add_sensor_type(sensor_type_json)
                sensor_jsons = from_openaq_to_sensor_jsons(result, sensor_type, node)
                for sensor_json in sensor_jsons:
                    db.add_sensor(sensor_json)

        nodes = db.nodes()
        nodes_per_location = {x["location"]["location"]: x for x in nodes}
        page_size = api.page_size()
        for country in api.countries():
            results = api.measurements(country)
            page = 1
            results_count = len(results)
            while results_count:
                for result in results:
                    location = result["location"]
                    params = {"country": country}
                    node = find_node_for_location(
                        location,
                        nodes_per_location,
                        api,
                        params,
                    )
                    if node:
                        sensor_data_json = from_openaq_to_sensor_data_json(result)
                        if sensor_data_json:
                            measurement_parameter = result["parameter"].strip().lower()
                            pin = settings.OPENAQ_API_PARAMETERS_PIN_MAPPING[
                                measurement_parameter
                            ]
                            db.add_sensor_data(sensor_data_json, node["uid"], pin)
                            data_count += 1
                            if settings.SENSORSAFRICA_API_DELAY:
                                time.sleep(settings.SENSORSAFRICA_API_DELAY / 1000.0)
                        else:
                            app.log.warn(
                                "Missing SensorData for measurement %s", result
                            )
                    else:
                        app.log.warn("Missing Node for measurement %s", result)

                if results_count >= page_size:
                    page += 1
                    params = {"page": page}
                    results = api.measurements(country, params)
                    results_count = len(results)
                else:
                    results_count = 0

        api_parameters["start_date"] = (
            api_parameters.get("start_date") or DEFAULT_START_DATE
        )
        api_parameters["count"] = api_parameters["count"] + data_count
        api_parameters["last_end_date"] = start_time.isoformat()
        api_parameters["last_count"] = data_count
        sheet.save(api_parameters)
    else:
        app.log.warn("Missing API parameters")

    return data_count
