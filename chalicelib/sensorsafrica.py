from dataclasses import dataclass
from operator import itemgetter
from typing import Dict, List

import arrow
import requests

from chalicelib import settings


@dataclass
class Location:
    location: str
    longitude: str
    latitude: str
    city: str
    country: str
    id: int = None
    indoor: bool = False
    owner: int = None

    def __post_init__(self):
        self.owner = settings.SENSORSAFRICA_API_OWNER_ID


@dataclass
class Node:
    uid: str
    location: int
    id: int = None
    owner: int = None

    def __post_init__(self):
        self.owner = settings.SENSORSAFRICA_API_OWNER_ID


@dataclass
class Sensor:
    sensor_type: int
    node: int
    id: int = None
    pin: str = None
    public: bool = False


@dataclass
class SensorData:
    timestamp: str
    sensordatavalues: List[Dict]
    sampling_rate: str = None
    software_version: str = None

    def __post_init__(self):
        self.timestamp = arrow.get(self.timestamp).isoformat()


@dataclass
class SensorType:
    name: str
    manufacturer: str
    id: int = None


def from_location_json(location_json):
    id = location_json.get("id")
    indoor = location_json.get("indoor")
    city, country, latitude, location, longitude = itemgetter(
        "city", "country", "latitude", "location", "longitude"
    )(location_json)
    return Location(
        city=city,
        country=country,
        id=id,
        indoor=indoor,
        latitude=latitude,
        location=location,
        longitude=longitude,
    )


def from_node_json(json):
    id = json.get("id")
    location = json["location"]
    owner = json.get("owner")
    uid = json["uid"]
    return Node(
        id=id,
        location=location,
        owner=owner,
        uid=uid,
    )


def from_sensor_type_json(json):
    id = json.get("id")
    name = json.get("name")
    manufacturer = json.get("manufacturer")
    return SensorType(
        id=id,
        name=name,
        manufacturer=manufacturer,
    )


class DB:
    def __init__(self):
        self._url = settings.SENSORSAFRICA_API_URL
        self._authorization = f"Token {settings.SENSORSAFRICA_API_AUTHORIZATION_TOKEN}"

    def url(self):
        return self._url

    def add_location(self, location: Dict):
        response = requests.post(
            self._url + "/v2/locations/",
            json=location,
            headers={"Authorization": self._authorization},
        )
        if not response.ok:
            raise Exception(response.reason)

        return from_location_json(response.json())

    def add_node(self, node: Dict):
        response = requests.post(
            self._url + "/v2/nodes/",
            json=node,
            headers={"Authorization": self._authorization},
        )
        if not response.ok:
            raise Exception(response.reason)

        return from_node_json(response.json())

    def add_sensor(self, sensor: Dict):
        response = requests.post(
            self._url + "/v2/sensors/",
            json=sensor,
            headers={"Authorization": self._authorization},
        )
        if not response.ok:
            raise Exception(response.reason)

        return response.json()

    def add_sensor_type(self, sensor_type: Dict):
        response = requests.post(
            self._url + "/v2/sensor-types/",
            json=sensor_type,
            headers={"Authorization": self._authorization},
        )
        if not response.ok:
            raise Exception(response.reason)

        return from_sensor_type_json(response.json())

    def add_sensor_data(self, sensor_data: Dict, node: int, pin: str = None):
        headers = {
            "X-SENSOR": f"{node}",
        }
        if pin:
            headers["X-PIN"] = pin

        response = requests.post(
            self._url + "/v1/push-sensor-data/",
            json=sensor_data,
            headers=headers,
        )
        if not response.ok:
            raise Exception(response.reason)

        return response.json()

    def nodes(self):
        if hasattr(self, "_nodes"):
            return self._nodes

        response = requests.get(
            self._url + "/v1/node/",
            headers={"Authorization": self._authorization},
        )
        if not response.ok:
            raise Exception(response.reason)

        return response.json()
