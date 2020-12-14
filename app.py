import logging
import sentry_sdk

from chalice import Chalice, IAMAuthorizer
from sentry_sdk.integrations.chalice import ChaliceIntegration

from chalicelib import main, settings

sentry_sdk.init(
    debug=settings.DEBUG,
    dsn=settings.SENTRY_DSN,
    integrations=[ChaliceIntegration()],
    traces_sample_rate=1.0,
)

app = Chalice(app_name="sensorsafrica-api-data-openaq")

if settings.DEBUG:
    app.log.setLevel(logging.DEBUG)

authorizer = IAMAuthorizer()


@app.route("/", methods=["GET"], authorizer=authorizer)
def run():
    app.log.debug("run")
    return main.run(app)


@app.schedule(settings.SCHEDULE_RATE)
def scheduled(event):
    app.log.debug(event.to_dict())
    return main.run(app)
