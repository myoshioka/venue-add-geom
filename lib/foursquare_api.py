import os
import foursquare
import requests
from lib.exception import DataNotFoundError
from lib.exception import FoursquareAPIError
from lib.exception import FoursquareAPIRateLimitExceeded


class FoursquareApi():

    client_id = os.environ.get('CLIENT_ID', '')
    client_secret = os.environ.get('CLIENT_SECRET', '')
    api_version = '20180327'

    @classmethod
    def get_foursquare_venue_details(cls, venue_id):
        client = cls.__foursquare_client()

        try:
            venue = client.venues(venue_id)
        except foursquare.ParamError:
            raise DataNotFoundError('foursquare-api Parameter Error!')
        except foursquare.RateLimitExceeded:
            raise FoursquareAPIRateLimitExceeded(
                'Rate limit for this hour exceeded')
        except foursquare.FoursquareException:
            raise FoursquareAPIError('Foursquare API Error')

        if venue is None:
            raise DataNotFoundError('Data Not Found!')

        return venue['venue']

    @classmethod
    def __foursquare_client(cls):
        client = foursquare.Foursquare(
            client_id=cls.client_id, client_secret=cls.client_secret, lang='ja')
        return client
