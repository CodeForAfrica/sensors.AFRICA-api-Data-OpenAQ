from chalicelib.openaq_api import Api
from chalicelib.sheets import ApiParametersSheet


def run(app):
    sheet = ApiParametersSheet()
    api_parameters = sheet.load()
    app.log.debug("PARAMETERS: {}\r\n", api_parameters)
    if api_parameters:
        api = Api()
        location_params = {}
        location_params["limit"] = api_parameters["limit"]
        locations = api.locations(location_params)
        app.log.debug("LOCATIONS: %s\r\n", locations)
        measurements_params = {}
        measurements_params["limit"] = api_parameters["limit"]
        measurements_params["date_from"] = api_parameters["date_from"]
        measuremens = api.measurements(measurements_params)
        app.log.debug("MEASUREMENTS: %s\r\n", measuremens)

        # for params in search_parameters:
        #     claims = api.search(params)
        #     db.track(claims=claims, timestamp=now.timestamp)
        #     claims_count += len(claims)

    return 0
