import requests

from chalicelib import settings

# from chalicelib.debunkbot import Claim


# def claim_from_json(claim_json):
#     claim_review = claim_json["claimReview"][0]
#     return Claim(
#         fact_checked_url=claim_review["url"],
#         claim_reviewed=claim_review.get("title"),
#         claim_date=claim_json.get("claimDate"),
#         claim_phrase=claim_json.get("text"),
#         claim_author=claim_json.get("claimant"),
#         textual_rating=claim_review.get("textualRating"),
#     )


class Api:
    def __init__(self):
        self._countries = [
            c.strip() for c in settings.OPENAQ_API_COUNTRIES.split(",") if c.strip()
        ]
        self._parameters = [
            p.strip() for p in settings.OPENAQ_API_PARAMETERS.split(",") if p.strip()
        ]
        self._url = settings.OPENAQ_API_URL

    def url(self):
        return self._url

    def locations(self, params):
        if len(self._countries) and len(self._parameters):
            payload = {**params}
            payload["country"] = self._countries
            payload["has_geo"] = True
            payload["parameter"] = self._parameters
            payload["metadata"] = True
            response = requests.get(
                f"{self._url}/locations",
                params=payload,
            )
            if not response.ok:
                raise Exception(response.reason)

            return response.json()["results"]

        return []

    def measurements(self, params):
        results = []
        if len(self._countries) and len(self._parameters):
            # Measurements have to be done by country
            for country in self._countries:
                payload = {**params}
                payload["country"] = country
                payload["has_geo"] = True
                payload["parameter"] = self._parameters
                response = requests.get(
                    f"{self._url}/measurements",
                    params=payload,
                )
                if not response.ok:
                    raise Exception(response.reason)

                response = response.json()
                results = [*results, *response["results"]]

        return results
