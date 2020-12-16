import requests

from chalicelib import settings

# OpenAQ allows data access via API only up to 2018-01-01
# see:https://openaq.medium.com/openaq-extends-api-and-download-tool-access-from-90-days-to-2-years-3697540c85a3
DEFAULT_START_DATE = "2018-01-01"


class Api:
    def __init__(self, paramemeters):
        self._countries = [
            c.strip() for c in settings.OPENAQ_API_COUNTRIES.split(",") if c.strip()
        ]
        self._measurement_parameters = [
            p.strip() for p in settings.OPENAQ_API_PARAMETERS.split(",") if p.strip()
        ]
        self._parameters = paramemeters
        self._url = settings.OPENAQ_API_URL

    def countries(self):
        return self._countries

    def page_size(self):
        return self._parameters["page_size"]

    def url(self):
        return self._url

    def location(self, location, params={}):
        if len(self._countries) and len(self._measurement_parameters):
            payload = {**params}
            payload["country"] = payload.get("country") or self._countries
            payload["has_geo"] = True
            payload["limit"] = payload.get("limit") or self._parameters["page_size"]
            payload["location"] = location
            payload["metadata"] = True
            payload["parameter"] = self._measurement_parameters
            response = requests.get(
                f"{self._url}/locations",
                params=payload,
            )
            if not response.ok:
                raise Exception(response.reason)

            return response.json()["results"]

        return []

    def locations(self, params={}):
        if len(self._countries) and len(self._measurement_parameters):
            payload = {**params}
            payload["country"] = payload.get("country") or self._countries
            payload["has_geo"] = True
            payload["limit"] = payload.get("limit") or self._parameters["page_size"]
            payload["metadata"] = True
            payload["parameter"] = self._measurement_parameters
            response = requests.get(
                f"{self._url}/locations",
                params=payload,
            )
            if not response.ok:
                raise Exception(response.reason)

            return response.json()["results"]

        return []

    # Measurements have to be done per country
    def measurements(self, country, params={}):
        if (
            len(self._countries)
            and len(self._measurement_parameters)
            and country in self._countries
        ):
            payload = {**params}
            payload["date_from"] = (
                payload.get("date_from")
                or self._parameters.get("last_end_date")
                or self._parameters.get("start_date")
                or DEFAULT_START_DATE
            )
            payload["limit"] = payload.get("limit") or self._parameters["page_size"]
            payload["has_geo"] = True
            payload["parameter"] = self._measurement_parameters
            payload["include_fields"] = "averagingPeriod"
            payload["country"] = country
            response = requests.get(
                f"{self._url}/measurements",
                params=payload,
            )
            if not response.ok:
                raise Exception(response.reason)

            return response.json()["results"]

        return []
